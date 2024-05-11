import cv2
from ultralytics import YOLO
import numpy as np
from ai_trainer.feedback.front_squat import give_feedback_front_squat, counts_calculate_front_squat
from ai_trainer.feedback.push_up import give_feedback_push_up, counts_calculate_push_up
from ai_trainer.feedback.biceps import give_feedback_biceps, counts_calculate_biceps
from ai_trainer.drawing import *
from ai_trainer.properties import *
import argparse
from ai_trainer.pac import PointAccumulator
from ai_trainer.direction_counter import TaskCounter

class ExerciseAnalyzer:
    def __init__(self, exercise_name):
        self.model = YOLO('models/yolo3/best.pt')
        self.validFrames = {}
        self.exercise_name = exercise_name.lower()
        if self.exercise_name == 'front_squat':
            self.active_keypoints = [10, 8, 6, 12, 11, 5, 7, 9]
            self.exercise_feedback_func = give_feedback_front_squat
            self.counts_calculate = counts_calculate_front_squat
        elif self.exercise_name == 'push_up':
            self.active_keypoints = [9, 7, 5, 6, 8, 10]
            self.exercise_feedback_func = give_feedback_push_up 
            self.counts_calculate = counts_calculate_push_up
        elif self.exercise_name == 'biceps':
            self.active_keypoints = []
            self.exercise_feedback_func = give_feedback_biceps 
            self.counts_calculate = counts_calculate_biceps
        else:
            raise ValueError("Invalid exercise name provided.")

    def analyze_video(self, frame):

        results = self.model.predict(frame)
        kps = results[0].keypoints.data.cpu().numpy()[0]
        pose_3d = np.column_stack(kps.T[:3])

        frame = draw_pose(
            image=frame,
            keypoints=pose_3d,
            disposition="coco",
            thickness=2,
        )

        feedback, possible_corrections, pointsofinterest, feedback_flag = self.exercise_feedback_func(pose_3d)
        offset = 0
        for correction in possible_corrections:
            if correction in list(feedback.keys()):
                frame = draw_text(
                    image=frame,
                    text=feedback[correction],
                    origin=(10, 150+offset*30),
                    font_scale=0.8,
                    color=(50, 50, 250),
                    thickness=2,
                )
                offset += 1
        correct = 1
        if  feedback_flag == True:
                correct = 0
        correctCount, incorrectCount = self.counts_calculate(pose_3d, correct)
        score_table(frame, correctCount)
        score_table_2(frame, incorrectCount)

        for poi in pointsofinterest:
            coords = poi['coords']

            if coords[0] == 0 and coords[1] == 0:
                continue

            color = (0,255,0)

            if not poi['valid']:
                color = (0,0,255)
            
            visible = True
     
            if poi['valid']:
            
                if poi['id'] not in self.validFrames:
                    self.validFrames[poi['id']] = 0
                
                self.validFrames[poi['id']] += 1
                if self.validFrames[poi['id']] > 10:
                    visible = False
            else:
           
                self.validFrames[poi['id']] = 0
            
            if visible:
                frame = draw_circle(frame, (int(coords[0]), int(coords[1])), 10, color, 2)

        return frame, correctCount, incorrectCount


