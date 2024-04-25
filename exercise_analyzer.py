# import cv2
# from ultralytics import YOLO
# import numpy as np
# from ai_trainer.feedback.front_squat import give_feedback_front_squat, counts_calculate
# from ai_trainer.drawing import *
# from ai_trainer.properties import *
# import argparse
# from ai_trainer.feedback.push_up import give_feedback_push_up, counts_calculate


# parser = argparse.ArgumentParser(description='Run pose estimation on a video for a specific exercise')
# parser.add_argument('exercise', type=str, help='Name of the exercise to analyze')
# args = parser.parse_args()

# if args.exercise.lower() == 'front_squat':
#     illustrate_exercise("assets/frontalniye-prisedaniya.jpeg")
#     active_keypoints = [10,8,6,12,11,5,7,9]
#     exercise_feedback_func = give_feedback_front_squat
# elif args.exercise.lower() == 'push_up': 
#     # illustrate_exercise("other_exercise_image.jpeg")
#     active_keypoints = [9, 7, 5, 6, 8, 10]
#     exercise_feedback_func = give_feedback_push_up 
# else:
#     print("Invalid exercise name provided.")
#     exit()

# def main():

#     model = YOLO('models/yolo2/best.pt')
#     # video_path = 'assets/left_side_cut.mp4'
#     video_path = 'assets/push_up1.mp4'
#     cap = cv2.VideoCapture(video_path)
#     count = 0
#     dirr = 1

#     while cap.isOpened():
#         success, frame = cap.read()
#         # h, w, _ = frame.shape
#         # window_w = int(frame.shape[1] * w)
#         # window_h = int(frame.shape[0] * h)
#         # frame_size = int(cap.get(3)), int(cap.get(4))  # frame_w, frame_h
#         # img_w, img_h = frame_size
#         # cv2.resizeWindow("Video", window_w, window_h)
#         frame = cv2.resize(frame, (800, 650), interpolation=cv2.INTER_AREA)

#         if success:
#             results = model(frame)
#             kps = results[0].keypoints.data.cpu().numpy()[0]
#             # kps = results[0].keypoints.xy.cpu().numpy()[0]
#             x, y, z = kps.T[:3]
#             # x_img = x * img_w
#             # y_img = y * img_h
#             # pose_2d = np.column_stack((x_img, y_img))
#             pose_3d = np.column_stack((x, y, z))

#             frame = draw_pose(
#                 image=frame,
#                 keypoints=pose_3d,
#                 disposition="coco",
#                 thickness=2,
#             )

#             # annotated_frame = results[0].plot()
#             # for i in range(len(active_keypoints)-1):
#             #     pt1 = tuple(kps[active_keypoints[i][:2]].astype(int))
#             #     pt2 = tuple(kps[active_keypoints[i+1][:2]].astype(int))
#             #     cv2.line(frame, pt1, pt2, (255, 255, 255), 8)
#             #     cv2.circle(frame, pt1, 5, (0, 0, 0), 5)
#             feedback, possible_corrections = exercise_feedback_func(pose_3d)
#             offset = 0
#             for correction in possible_corrections:
#                 if correction in list(feedback.keys()):
#                     frame = draw_text(
#                         image=frame,
#                         text=feedback[correction],
#                         origin=(10, 100+offset*30),
#                         font_scale=0.8,
#                         color=(50, 50, 250),
#                         thickness=2,
#                     )
#                     offset += 1
#             count, dirr = counts_calculate(pose_3d, count, dirr)
#             score_table(frame, count)
#             cv2.imshow("Video", frame)

#             if cv2.waitKey(1) & 0xFF == ord("q"):
#                 break
#         else:
#             break

#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     main()
import cv2
from ultralytics import YOLO
import numpy as np
from ai_trainer.feedback.front_squat import give_feedback_front_squat, counts_calculate
from ai_trainer.feedback.push_up import give_feedback_push_up, counts_calculate
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

