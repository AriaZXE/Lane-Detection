# Lane-Detection
This is a code for detecting the appropriate lane in a vehicle.

To start an accurate lane detection, several steps need to be performed:

1 . Camera Calibration: ( The default video used in this code is calibrated. )

This step involves calibrating the camera to correct for distortions and ensure accurate measurements of distances in the image. More detailed information about camera calibration can be found in the "camera calibration" section of the code.

2 . Perspective Transformation: In order to obtain a bird's eye view of the road, the perspective of the image needs to be transformed. This transformation allows for a better view of the lane lines and simplifies the detection process.

3 . Lane Detection and Curvature Calculation: Once the perspective is transformed, the lane lines can be detected using various techniques such as edge detection, color thresholding, or machine learning algorithms. After detecting the lane lines, the curvature of the lanes can be calculated using mathematical models such as polynomials

##Camera Calibration 
We won't delve into the calibration section in detail, but we'll briefly mention that camera calibration involves using images of a chessboard pattern.

By using functions like cv2.findChessboardCorners and cv2.drawChessboardCorners, the corners of the chessboard are identified. Then, with functions like cv2.calibrate and cv2.undistort, the distorted images are corrected and undistorted.

original version :
![img2](https://github.com/AriaZXE/Lane-Detection/assets/82224320/3f7b213d-456b-49ba-a343-cab3306c1f30)

calibrated version : 
![calibrated_img2](https://github.com/AriaZXE/Lane-Detection/assets/82224320/a4ad76d9-fa05-432b-8a64-a85076d537ef)

undisorted version :
![undistorted_img2](https://github.com/AriaZXE/Lane-Detection/assets/82224320/993ae64b-ce38-4a15-8a04-d2a6ffb7b40d)

## Perspective Transformation

In this section, we transform the perspective of the image using points that form a trapezoid in the first case and a rectangle in the second case.

![Screenshot (447)](https://github.com/AriaZXE/Lane-Detection/assets/82224320/1a20278b-c23d-49ae-8cb8-5425e5beddcb)

The steps of this process are as follows:

The BirdEyeTransformer class is defined, which handles the transformation of the perspective to a bird's eye view.
The constructor __init__ takes the source (src) and destination (dst) points defining the region of interest and initializes the transformation matrix (m) using cv2.getPerspectiveTransform.


The bird_eye method applies the perspective transformation to the input image using cv2.warpPerspective.
The process_video method processes the video specified by video_path. It reads each frame from the video, applies the bird's eye view transformation, and displays the transformed frame. It also saves the transformed frames into an output video file specified by output_path.


The if __name__ == '__main__': block sets up the source and destination points, video path, and output path. An instance of BirdEyeTransformer is created, and the process_video method is called to perform the transformation on the video.

![Screenshot (446)](https://github.com/AriaZXE/Lane-Detection/assets/82224320/6de0a5af-09b7-440b-ad75-a99a59a553cf)

## Lane Detection and Curvature Calculation

1 . The code defines two classes: Line and LaneDetector.

The Line class represents a lane line and stores information about the line's properties such as iterations, best fit coefficients, and curvature.
The LaneDetector class is responsible for detecting and tracking lane lines in an image.

2 . The LaneDetector class has several parameters that can be adjusted:

nwindows: Number of sliding windows used for lane line detection.
margin: Width of the windows for lane line detection.
minpix: Minimum number of pixels required to recenter the sliding windows.
recalculate_margin: Margin for recalculation of lane pixels after the initial detection.
smoothing_parameter: Number of iterations used for smoothing the lane line fits.

![Screenshot (448)](https://github.com/AriaZXE/Lane-Detection/assets/82224320/0454244f-0eba-4a20-99b6-6758c39f293c)

3 . The LaneDetector class provides two main methods: pipeline and pipeline_image.

The pipeline method takes an image file as input, performs the lane detection pipeline, and saves the output image and a plot of the fitted polynomials.
The pipeline_image method takes an image array as input, performs the lane detection pipeline, and returns the output image, curvature, and center position.

4 . The _calculate_lane_pixels method is used to identify lane pixels in the image by applying a sliding window technique.

It divides the bottom half of the image into a specified number of windows.
For each window, it identifies the nonzero pixels within the window boundaries for both the left and right lanes.
It keeps track of the indices of the lane pixels for further processing.

5 . The _recalculate_lane_pixels method is called when the lane lines have been detected previously.

It uses the previous lane line fits to narrow down the search for lane pixels within a margin around the previous fits.
It returns the recalculated lane pixels for both the left and right lanes.

6 . The _sanity_check method performs a sanity check on the detected lane pixels.

It checks if any of the lane pixel arrays are empty, indicating a failed detection.
It also compares the curvatures of the left and right lanes and returns True if the difference is too large, indicating an unreliable detection.

7 . The _fit_polynomial method fits a second-degree polynomial to the lane pixels and visualizes the detected lane region.

It uses the np.polyfit function to fit polynomials to the left and right lane pixels separately.
It calculates the x-coordinates of the fitted polynomials for plotting and visualization.
It creates an output image by overlaying the detected lane region on the original image and highlights the lane pixels.
It also plots the fitted polynomials on a separate plot for visualization.
It updates the current and best fit coefficients of the lane lines and performs smoothing if necessary.

8 . The _calculate_curvature method calculates the lane curvature and the vehicle's position within the lane.

It uses the fitted polynomial coefficients to calculate the curvature for both the left and right lanes.
It also calculates the x-coordinate of the lane lines at the bottom of the image to determine the vehicle's position.
The curvature values are averaged, and the center position is calculated based on the averaged lane line positions.

![Screenshot (449)](https://github.com/AriaZXE/Lane-Detection/assets/82224320/81c4645d-90e0-4d53-b713-db6c29b1739a)

# Sliding Windows

Sliding windows is a common technique in image processing used for object detection and tracking in images. This method involves systematically placing a rectangular window at various locations in the image to extract information about a specific region.

The functioning of sliding windows is as follows: First, a rectangular window with a specific size is placed at an initial point in the image. Then, starting from this point, the window is moved to the right and down by a fixed length and width (usually a constant size). At each step, the contents within the window (such as color, intensity, patterns, and other features) are used for analysis and processing.

By shifting the window by a fixed length and width and repeating this process at all points in the image, we can obtain information about all regions in the image. This method allows us to identify patterns, objects, and important features in the image.

The use of sliding windows is beneficial in many image processing applications, including face detection, road line detection, sign recognition, and many others. By selecting an appropriate window size and shape, considering the desired features, we can achieve more accurate results in object detection and tracking in images.
![line_curvature_example](https://github.com/AriaZXE/Lane-Detection/assets/82224320/05aeb21e-7654-476e-bb99-027e57df0d38)

To determine the position of the next square relative to the previous square in the sliding windows method, a commonly used approach is to utilize an objective function. This objective function calculates a value for each potential position based on desired features such as color similarity, pattern similarity, intensity similarity, and so on.

Typically, the value of the objective function is computed for each potential position in the proximity of the previous square. The square with the highest value of the objective function is selected as the next square, and the window is moved to that position.

For example, in a face detection application, the objective function may be based on the similarity of skin color and specific facial patterns. In this case, the next square might be located near the previous square and have a higher value of the objective function in that region.

There are various methods for calculating the objective function, and these methods depend on the application and the desired target features. These methods can be based on statistical approaches, machine learning techniques, pattern matching, and other image processing techniques. Additionally, parameters such as the size and shape of the window can also have an impact.

In summary, understanding the next square is based on an objective function that calculates the desired features for each potential position, and the position with the highest value of the objective function is chosen as the next position.


In this code, Windows sliding is used to find the continuation of the lines
We got the starting point using histogram
and find photo optical peaks using
np.argmax

# Histogram 

We use a histogram to detect the starting point of lines because one axis represents the x-values in the image, and the other axis represents the cumulative values of the y-values. As a result, the peak points in the histogram indicate our lines.

![histogram-lane-detection](https://github.com/AriaZXE/Lane-Detection/assets/82224320/8a179689-1db5-4a3a-8c16-ae7e0f5a7ff7)

Conversion to grayscale: First, the image is converted to grayscale, where each pixel represents a specific grayscale value.

Histogram computation: Using the grayscale image, the histogram of the image is computed. The histogram represents the distribution of the pixel intensities in the image.

Detection of bright and dark regions: By analyzing the histogram, we can identify the bright and dark regions in the image. Road lines typically appear as dark regions in the image.

Pixel detection: Using the histogram and the identified bright and dark regions, we can detect pixels that are likely to belong to road lines. These pixels are often concentrated in specific regions of the histogram.

Line highlighting: With the detected pixels, we can highlight the road lines by either drawing lines on the image or creating a mask to display only the road lines.
