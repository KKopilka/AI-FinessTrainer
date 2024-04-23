from pydantic import BaseModel
import cv2
from ultralytics import YOLO

class GetKeypoint(BaseModel):
    NOSE:           int = 0
    LEFT_EYE:       int = 1
    RIGHT_EYE:      int = 2
    LEFT_EAR:       int = 3
    RIGHT_EAR:      int = 4
    LEFT_SHOULDER:  int = 5
    RIGHT_SHOULDER: int = 6
    LEFT_ELBOW:     int = 7
    RIGHT_ELBOW:    int = 8
    LEFT_WRIST:     int = 9
    RIGHT_WRIST:    int = 10
    LEFT_HIP:       int = 11
    RIGHT_HIP:      int = 12
    LEFT_KNEE:      int = 13
    RIGHT_KNEE:     int = 14
    LEFT_ANKLE:     int = 15
    RIGHT_ANKLE:    int = 16

# example 
model = YOLO('models/yolo/best.pt')
results = model('assets/6.png')
get_keypoint = GetKeypoint()
nose_x, nose_y = results[get_keypoint.NOSE]
left_eye_x, left_eye_y = keypoint[get_keypoint.LEFT_EYE]