import numpy as np
import matplotlib.pyplot as plt
import cv2


class Line:
    def __init__(self):

        self.iterations = 0
        self.best_fit = np.array([0, 0, 0])
        self.current_fit = np.array([0, 0, 0])
        self.curvature = 0

class LaneDetector:
    def __init__(self, nwindows = 10, margin = 100, minpix = 100, 
                 recalculate_margin = 150, smoothing_parameter = 10):
        self.nwindows = nwindows
        self.margin = margin
        self.minpix = minpix
        self.recalculate_margin = recalculate_margin
        self.smoothing_parameter = smoothing_parameter

        self.left_line = Line()
        self.right_line = Line()

    def pipeline(self, image_file, output_file, output_file_poly):

        image = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)
        leftx, lefty, rightx, righty = self._calculate_lane_pixels(image)

        output_image, ploty, left_fit, right_fit = self._fit_polynomial(image, leftx, lefty, rightx, righty)

        cv2.imwrite(output_file, output_image)

        plt.imshow(output_image)
        plt.savefig(output_file_poly)
        plt.clf()

        self.left_line.iterations = 0
        self.right_line.iterations = 0
        curvature, center = self._calculate_curvature(ploty, left_fit, right_fit, image.shape)

    def pipeline_image(self, image):
        if self.left_line.iterations == 0:
            leftx, lefty, rightx, righty = self._calculate_lane_pixels(image)
        else:
            leftx, lefty, rightx, righty = self._recalculate_lane_pixels(image)
            if self._sanity_check(leftx, lefty, rightx, righty):
                self.left_line.iterations = 0
                self.right_line.iterations = 0
                leftx, lefty, rightx, righty = self._calculate_lane_pixels(image)

        output_image, ploty, left_fit, right_fit = self._fit_polynomial(image, leftx, lefty, rightx, righty)

        curvature, center = self._calculate_curvature(ploty, left_fit, right_fit, image.shape)

        return output_image, curvature, center

    def _calculate_lane_pixels(self, image):
        self.left_line = Line()
        self.right_line = Line()

        bottom_half = image[3 * image.shape[0] // 5:, :]
        histogram = np.sum(bottom_half, axis = 0)

        midpoint = np.int32(histogram.shape[0] // 2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint

        window_height = np.int32(image.shape[0] // self.nwindows)

        nonzero = image.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        leftx_current = leftx_base
        rightx_current = rightx_base

        left_lane_indices = []
        right_lane_indices = []

        for window in range(self.nwindows):

            win_y_low = image.shape[0] - (window + 1) * window_height
            win_y_high = image.shape[0] - window * window_height
            win_xleft_low = leftx_current - self.margin
            win_xleft_high = leftx_current + self.margin
            win_xright_low = rightx_current - self.margin
            win_xright_high = rightx_current + self.margin

            good_left_indices = ((nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high) \
                & (nonzeroy >= win_y_low) & (nonzeroy < win_y_high)).nonzero()[0]
            good_right_indices = ((nonzerox >= win_xright_low) & (nonzerox < win_xright_high) \
                & (nonzeroy >= win_y_low) & (nonzeroy < win_y_high)).nonzero()[0]

            left_lane_indices.append(good_left_indices)
            right_lane_indices.append(good_right_indices)


            if len(good_left_indices) > self.minpix:
                leftx_current = np.int32(np.mean(nonzerox[good_left_indices]))
            if len(good_right_indices) > self.minpix:
                rightx_current = np.int32(np.mean(nonzerox[good_right_indices]))

        try:
            left_lane_indices = np.concatenate(left_lane_indices)
            right_lane_indices = np.concatenate(right_lane_indices)
        except:
            pass

        leftx = nonzerox[left_lane_indices]
        lefty = nonzeroy[left_lane_indices]
        rightx = nonzerox[right_lane_indices]
        righty = nonzeroy[right_lane_indices]

        return leftx, lefty, rightx, righty

    def _recalculate_lane_pixels(self, image):
        nonzero = image.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        left_fit = self.left_line.current_fit
        right_fit = self.right_line.current_fit

        left_lane_indices = \
            ((nonzerox > (left_fit[0] * nonzeroy ** 2 + left_fit[1] * nonzeroy + left_fit[2] - self.recalculate_margin)) \
            & (nonzerox < (left_fit[0] * nonzeroy ** 2 + left_fit[1] * nonzeroy + left_fit[2] + self.recalculate_margin)))
        right_lane_indices = \
            ((nonzerox > (right_fit[0] * nonzeroy ** 2 + right_fit[1] * nonzeroy + right_fit[2] - self.recalculate_margin)) \
            & (nonzerox < (right_fit[0] * nonzeroy ** 2 + right_fit[1] * nonzeroy + right_fit[2] + self.recalculate_margin)))

        leftx = nonzerox[left_lane_indices]
        lefty = nonzeroy[left_lane_indices]
        rightx = nonzerox[right_lane_indices]
        righty = nonzeroy[right_lane_indices]

        return leftx, lefty, rightx, righty

    def _sanity_check(self, leftx, lefty, rightx, righty):

        if leftx.size == 0 or lefty.size == 0 or rightx.size == 0 or righty.size == 0:
            return True

        if self.left_line.curvature / self.right_line.curvature >= 3:
            return True

        return False

    def _fit_polynomial(self, image, leftx, lefty, rightx, righty):
       
        left_fit = np.polyfit(lefty, leftx, 2) 
        right_fit = np.polyfit(righty, rightx, 2)

        if self.left_line.iterations != 0:
            left_fit = left_fit * 0.75 + self.left_line.best_fit * 0.25
            right_fit = right_fit * 0.75 + self.right_line.best_fit * 0.25

        ploty = np.linspace(0, image.shape[0] - 1, image.shape[0])
        try:
            left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
            right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]
        except TypeError:
            left_fitx = ploty ** 2 + ploty
            right_fitx = ploty ** 2 + ploty

        output_image = np.dstack((image, image, image))

        points1 = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
        points2 = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
        points = np.hstack((points1, points2))
        cv2.fillPoly(output_image, np.int_([points]), color = [0, 127, 0])
        
        output_image[lefty, leftx] = [255, 0, 0]
        output_image[righty, rightx] = [0, 0, 255]

        plt.plot(left_fitx, ploty, color = 'yellow')
        plt.plot(right_fitx, ploty, color = 'yellow')

        self.left_line.current_fit = left_fit
        self.right_line.current_fit = right_fit
        self.left_line.iterations += 1
        self.right_line.iterations += 1

        if self.left_line.iterations == self.smoothing_parameter:
            self.left_line.iterations = 1
            self.right_line.iterations = 1

            self.left_line.best_fit = np.array([0, 0, 0])
            self.right_line.best_fit = np.array([0, 0, 0])

        self.left_line.best_fit = (self.left_line.best_fit * (self.left_line.iterations - 1) + self.left_line.current_fit) / self.left_line.iterations
        self.right_line.best_fit = (self.right_line.best_fit * (self.left_line.iterations - 1) + self.right_line.current_fit) / self.right_line.iterations
        
        return output_image, ploty, left_fit, right_fit

    def _calculate_curvature(self, points, left_fit, right_fit, shape):

        ym_per_pix = 30 / shape[0] 
        xm_per_pix = 3.7 / shape[1]

        y_eval = np.max(points)
        left_curvature = (np.power(1 + (2 * left_fit[0] * y_eval * ym_per_pix + left_fit[1]) ** 2, 1.5)) / np.absolute(2 * left_fit[0])
        right_curvature = (np.power(1 + (2 * right_fit[0] * y_eval * ym_per_pix + right_fit[1]) ** 2, 1.5)) / np.absolute(2 * right_fit[0])
        
        left_fitx = left_fit[0] * y_eval ** 2 + left_fit[1] * y_eval + left_fit[2]
        right_fitx = right_fit[0] * y_eval ** 2 + right_fit[1] * y_eval + right_fit[2]
        center = (right_fitx + left_fitx) * xm_per_pix / 2

        self.left_line.curvature = left_curvature
        self.right_line.curvature = right_curvature

        return (left_curvature + right_curvature) / 2, center





    