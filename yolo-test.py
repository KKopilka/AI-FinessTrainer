import cv2
from ultralytics import YOLO
import numpy as np
from ai_trainer.feedback.front_squat import give_feedback
from ai_trainer.drawing import *

# Load a pretrained YOLOv8n model
model = YOLO('models/yolo/best.pt')  # Загрузка модели

# Read an image using OpenCV
video_path = 'assets/left_side_cut.mp4'
cap = cv2.VideoCapture(video_path)
count = 0
dirr = 1
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    frame = cv2.resize(frame, (800, 650), interpolation=cv2.INTER_AREA)

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)
        kps = results[0].keypoints.data
        # print("keys: ", key)
        x, y, z = kps.T[:3].cpu().numpy()
        pose_3d = np.column_stack((x, y, z))
        # print("pose_3d: ", pose_3d)

        annotated_frame = results[0].plot()

        feedback, possible_corrections, count = give_feedback(pose_3d, count)
        for correction in possible_corrections:
                if correction in list(feedback.keys()):
                    annotated_frame = draw_text(
                        image=annotated_frame,
                        text=feedback[correction],
                        origin=(10, 100),
                        font_scale=0.8,
                        color=(50, 50, 250),
                        thickness=2,
                    )
                    print(possible_corrections)
        cv2.putText(annotated_frame, f'Count: {count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
 
        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()