import cv2
from ultralytics import YOLO
import numpy as np
from ai_trainer.feedback.front_squat import give_feedback_front_squat, counts_calculate
from ai_trainer.feedback.push_up import give_feedback_push_up, counts_calculate
from ai_trainer.feedback.biceps import give_feedback_biceps, counts_calculate
from ai_trainer.drawing import *
from ai_trainer.properties import *
import argparse

class ExerciseAnalyzer:
    def __init__(self, exercise_name):
        self.exercise_name = exercise_name.lower()
        if self.exercise_name == 'front_squat':
            self.active_keypoints = [10, 8, 6, 12, 11, 5, 7, 9]
            self.exercise_feedback_func = give_feedback_front_squat
        elif self.exercise_name == 'push_up':
            self.active_keypoints = [9, 7, 5, 6, 8, 10]
            self.exercise_feedback_func = give_feedback_push_up 
        else:
            raise ValueError("Invalid exercise name provided.")

        self.model = YOLO('models/yolo2/best.pt')

    def analyze_video(self, frame):
        # cap = cv2.VideoCapture(frame)
        count = 0
        dirr = 1

        # while cap.isOpened():
            # success, frame = cap.read()
        # frame = cv2.resize(frame, (800, 650), interpolation=cv2.INTER_AREA)

        # if success:
        results = self.model(frame)
        kps = results[0].keypoints.data.cpu().numpy()[0]
        pose_3d = np.column_stack(kps.T[:3])

        frame = draw_pose(
            image=frame,
            keypoints=pose_3d,
            disposition="coco",
            thickness=2,
        )

        feedback, possible_corrections = self.exercise_feedback_func(pose_3d)
        offset = 0
        for correction in possible_corrections:
            if correction in list(feedback.keys()):
                frame = draw_text(
                    image=frame,
                    text=feedback[correction],
                    origin=(10, 100+offset*30),
                    font_scale=0.8,
                    color=(50, 50, 250),
                    thickness=2,
                )
                offset += 1
        count, dirr = counts_calculate(pose_3d, count, dirr)
        score_table(frame, count)

        
            # cv2.imshow("Video", frame)

    # if cv2.waitKey(1) & 0xFF == ord("q"):
    #     break
        # else:
        #     break
        return frame, count
        # cap.release()
        # cv2.destroyAllWindows()

