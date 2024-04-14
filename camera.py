"""This script gives you feedback on your front squad technique."""
import argparse

import cv2
import numpy as np
from tqdm import tqdm

from ai_trainer.models import BlazePoseModel
from ai_trainer.drawing import draw_pose, draw_text
from ai_trainer.feedback.front_squat import give_feedback

def main():
    blazepose_model = BlazePoseModel(model_path="./models/blazepose_full.onnx")
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        _, frame = cap.read()
        # frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Get video configuration
        # nbr_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # frame_size = int(cap.get(3)), int(cap.get(4))  # frame_w, frame_h
        # img_w, img_h = frame_size
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        if frame is None:
            break
        # copy_frame = frame.copy()
        kps = blazepose_model.predict([
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ])[0]  # batch size is 1

        probs = kps.T[3]
        # if not any(probs<0):
        #     # denormalize keypoints:
        #     x, y, z = kps.T[:3]
        #     x_img = x * img_w
        #     y_img = y * img_h
        #     pose_3d = np.column_stack((x_img, y_img, z))
        #     pose_2d = np.column_stack((x_img, y_img))

        #     # plot keypoints on image
        #     copy_frame = draw_pose(
        #         image=copy_frame,
        #         keypoints=pose_2d,
        #         disposition="mediapipe", # blazepose keypoints are in mediapipe format
        #         thickness=2,
        #     )
        if not all(probs<0):
        # plot keypoints on image
        # denormalize keypoints to pixel values
            x, y, z = kps.T[:3]

            pose_3d = np.column_stack((x, y, z))
            frame = draw_pose(
                image=frame,
                keypoints=pose_3d,
                disposition="mediapipe", # blazepose keypoints are in mediapipe format
                thickness=2,
            )

            feedback, possible_corrections = give_feedback(pose_3d)

            y_text_pos = 0
            for correction in possible_corrections:
                y_text_pos+=25
                if correction in list(feedback.keys()):
                    copy_frame = draw_text(
                        image=frame,
                        text=feedback[correction],
                        origin=(10, y_text_pos),
                        font_scale=0.8,
                        color=(50, 50, 250),
                        thickness=2,
                    )
        # output.write(copy_frame)
        cv2.imshow('Video', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
