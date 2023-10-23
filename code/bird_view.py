import cv2
import numpy as np


src = np.float32([(550, 460),
                  (150, 720),
                  (1200, 720),
                  (770, 460)])

dst = np.float32([(100, 0),
                  (100, 720),
                  (1100, 720),
                  (1100, 0)])

m = cv2.getPerspectiveTransform(src, dst)
m_inv = cv2.getPerspectiveTransform(dst, src)

def bird_eye(img):
    size = (1280, 720)
    return cv2.warpPerspective(img, m, size)


video_path = './../test_videos/project_video.mp4'
output_path = 'output_video.mp4'


video = cv2.VideoCapture(video_path)


fps = video.get(cv2.CAP_PROP_FPS)
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

while True:

    ret, frame = video.read()

    if not ret:
 
        break


    bird_eye_frame = bird_eye(frame)


    cv2.imshow('Bird Eye View', bird_eye_frame)
    
  
    output_video.write(bird_eye_frame)

   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video.release()
output_video.release()
cv2.destroyAllWindows()