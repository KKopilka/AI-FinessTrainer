"""This script gives you feedback on your front squad technique."""
import argparse

import cv2
import numpy as np
from tqdm import tqdm

from ai_trainer.models import BlazePoseModel
from ai_trainer.drawing import draw_pose, draw_text
from ai_trainer.feedback.front_squat import give_feedback

def main(video_path):
    """Analyse a video and give feedback on the person's front squat technique.

    Args:
        video_path (str): path to the input video file.
    """
    save_video_path = video_path[:-4] + "_processed.mp4"
    blazepose_model = BlazePoseModel(model_path="./models/blazepose_full.onnx")

    # Read video:
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened() is False:
        print("Error reading the video file")

    # Get video configuration
    nbr_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_size = int(cap.get(3)), int(cap.get(4))  # frame_w, frame_h
    img_w, img_h = frame_size
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Create video writer
    # Get video codec
    if video_path[-4:] == ".mp4" or video_path[-4:] == ".MOV":
        fourcc = cv2.VideoWriter_fourcc(*"MP4V")
    elif video_path[-4:] == ".avi":
        fourcc = cv2.VideoWriter_fourcc(*"XVID")

    output = cv2.VideoWriter(save_video_path,
                            fourcc,
                            fps, frame_size)

    # Iterate through frames
    print("💪 Evaluating your front squat technique...")
    for i in tqdm(range(int(nbr_frames))):
        # Read the video file
        __, frame = cap.read()

        # Check we have frames:
        if frame is None:
            break
        copy_frame = frame.copy()
        kps = blazepose_model.predict([
            cv2.cvtColor(copy_frame, cv2.COLOR_BGR2RGB)
            ])[0]  # batch size is 1

        probs = kps.T[3]
        if not any(probs<0):
            # denormalize keypoints:
            x, y, z = kps.T[:3]
            x_img = x * img_w
            y_img = y * img_h
            pose_3d = np.column_stack((x_img, y_img, z))
            pose_2d = np.column_stack((x_img, y_img))

            # plot keypoints on image
            copy_frame = draw_pose(
                image=copy_frame,
                keypoints=pose_2d,
                disposition="mediapipe", # blazepose keypoints are in mediapipe format
                thickness=2,
            )

            feedback, possible_corrections = give_feedback(pose_3d)

            y_text_pos = 0
            for correction in possible_corrections:
                y_text_pos+=25
                if correction in list(feedback.keys()):
                    copy_frame = draw_text(
                        image=copy_frame,
                        text=feedback[correction],
                        origin=(10, y_text_pos),
                        font_scale=0.8,
                        color=(50, 50, 250),
                        thickness=2,
                    )
        output.write(copy_frame)

    cap.release()
    output.release()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'AI Trainer: Form evaluation')
    parser.add_argument('--input_video', help='path to the input video file')
    args = parser.parse_args()
    main(args.input_video)
