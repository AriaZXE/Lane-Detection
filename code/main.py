from image_transformation import ImageTransformation
from lane_detection import LaneDetector
import cv2

if __name__ == "__main__":
    transform = ImageTransformation()
    lanes = LaneDetector()

    def process_image(image):
        transformed_image = transform.binary_pipeline_image(
            image, (40, 60), (220, 255), (90, 100)
        )
        perspective_binary = transform.transform_pipeline_image(transformed_image)

        lane_image, curvature, lane_center = lanes.pipeline_image(perspective_binary)

        final_image = transform.untransform_pipeline_image(lane_image, image)

        cv2.putText(
            final_image, f"Curvature: {round(curvature, 2)} m",
            (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 0, 255), 2
        )

        actual_center = (image.shape[1] / 2) * (3.7 / image.shape[1])
        if (lane_center < actual_center):
            offset_text = f"Offset: {round(actual_center - lane_center, 2)} m to right"
        else:
            offset_text = f"Offset: {round(lane_center - actual_center, 2)} m to left"

        cv2.putText(
            final_image, offset_text,
            (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
            1, (255, 255, 255), 2
        )

        cv2.imshow("Video", final_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    video_file = cv2.VideoCapture("./../test_videos/project_video.mp4")

    while True:
        ret, frame = video_file.read()
        if not ret:
            break

        process_image(frame)

    video_file.release()