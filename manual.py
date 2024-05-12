import cv2
import onnxruntime
from ultralytics import YOLO
import numpy as np
from ai_trainer.drawing import *
from ai_trainer.properties import *
import argparse
from ai_trainer.feedback.front_squat import give_feedback_front_squat, counts_calculate_front_squat
from ai_trainer.feedback.push_up import give_feedback_push_up, counts_calculate_push_up
from ai_trainer.feedback.biceps import give_feedback_biceps, counts_calculate_biceps
from ai_trainer.feedback.barbell_pull import give_feedback_barbell_pull, counts_calculate_barbell_pull
from ai_trainer.feedback.reverse_push_up import give_feedback_reverse_push_up, counts_calculate_reverse_push_up
from ai_trainer.pac import PointAccumulator


parser = argparse.ArgumentParser(description='Run pose estimation on a video for a specific exercise')
parser.add_argument('exercise', type=str, help='Name of the exercise to analyze')
args = parser.parse_args()

if args.exercise.lower() == 'front_squat':
    # illustrate_exercise("assets/frontalniye-prisedaniya.jpeg")
    active_keypoints = [10,8,6,12,11,5,7,9]
    exercise_feedback_func = give_feedback_front_squat
    counts_calculate = counts_calculate_front_squat
elif args.exercise.lower() == 'push_up': 
    # illustrate_exercise("assets/push_up.jpg")
    active_keypoints = [9, 7, 5, 6, 8, 10]
    exercise_feedback_func = give_feedback_push_up 
    counts_calculate = counts_calculate_push_up
elif args.exercise.lower() == 'biceps': 
    # illustrate_exercise("assets/biceps.jpg")
    active_keypoints = []
    exercise_feedback_func = give_feedback_biceps
    counts_calculate = counts_calculate_biceps
elif args.exercise.lower() == 'reverse_push_up.jpg': 
    # illustrate_exercise("assets/biceps.jpg")
    active_keypoints = []
    exercise_feedback_func = give_feedback_reverse_push_up
    counts_calculate = counts_calculate_reverse_push_up
else:
    print("Invalid exercise name provided.")
    exit()

def main():
    model = YOLO('models/yolo3/best.pt', task='pose')
    # video_path = 'assets/left_side_cut.mp4'
    video_path = 'assets/reverse_push_up.mp4'
    # video_path = 'assets/push_up2.mp4'
    cap = cv2.VideoCapture(video_path)
    count = 0
    dirr = 1

    validFrames = {}

    while cap.isOpened():
        success, frame = cap.read()
        # h, w, _ = frame.shape
        # window_w = int(frame.shape[1] * w)
        # window_h = int(frame.shape[0] * h)
        # frame_size = int(cap.get(3)), int(cap.get(4))  # frame_w, frame_h
        # img_w, img_h = frame_size
        # cv2.resizeWindow("Video", window_w, window_h)
        frame = cv2.resize(frame, (900, 650), interpolation=cv2.INTER_AREA)

        if success:
            results = model.predict(frame)
            # kps = results[0].keypoints.xy.cpu().numpy()
            kps = results[0].keypoints.data.cpu().numpy()[0]
            # kps = results[0].keypoints.xy.cpu().numpy()[0]
            x, y, z = kps.T[:3]
            # x_img = x * img_w
            # y_img = y * img_h
            # pose_2d = np.column_stack((x_img, y_img))
            pose_3d = np.column_stack((x, y, z))
            if pose_3d.size <= 0:
                continue
            frame = draw_pose(
                image=frame,
                keypoints=pose_3d,
                disposition="coco",
                thickness=2,
            )

            # annotated_frame = results[0].plot()
            # for i in range(len(active_keypoints)-1):
            #     pt1 = tuple(kps[active_keypoints[i][:2]].astype(int))
            #     pt2 = tuple(kps[active_keypoints[i+1][:2]].astype(int))
            #     cv2.line(frame, pt1, pt2, (255, 255, 255), 8)
            #     cv2.circle(frame, pt1, 5, (0, 0, 0), 5)
            feedback, possible_corrections, pointsofinterest, feedback_flag = exercise_feedback_func(pose_3d)
            offset = 0

            for correction in possible_corrections:
                # print(feedback_flag)
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

            correctCount, incorrectCount = counts_calculate(pose_3d, correct)
    

            score_table(frame, correctCount)
            score_table_2(frame, incorrectCount)
            # count_correct_attempts, dirr = counts_calculate(pose_3d, count_correct_attempts, dirr)
            # # count, dirr = counts_calculate(pose_3d, count, dirr)
            # score_table(frame, count)
            
            # Разбираем пришедшие точки интереса
            for poi in pointsofinterest:
                # получаем координаты кружка
                coords = poi['coords']
                # если координаты (0,0), то пропускаем, т.к. отрисовывать нет смысла
                if coords[0] == 0 and coords[1] == 0:
                    continue
                # цвет успешного попадания в зону кружка
                color = (0,255,0) # зеленый
                # проверяем содержит ли метка флаг ошибки valid = False
                if not poi['valid']:
                    color = (0,0,255) # меняем цвет на красный
                
                # По умолчанию метка отрисовывается. Мы проверяем условия, при которых метку нужно скрыть
                visible = True
                # Если метка положительная, то мы записываем счетчик фреймов validFrames, в котором подсчитываем
                # количество фреймов с положительным результатом.
                # При достижении счетчика порога в 10 положительных фреймов, метка скрывается - visible становится False
                if poi['valid']:
                    # если не было счетчика с ключем `id`, то создаем
                    if poi['id'] not in validFrames:
                        validFrames[poi['id']] = 0
                    
                    validFrames[poi['id']] += 1
                    if validFrames[poi['id']] > 10:
                        visible = False
                else:
                    # Если метка неудачная, то сбрасываем счётчик
                    validFrames[poi['id']] = 0
                
                # отрисовываем включенные метки
                if visible:
                    frame = draw_circle(frame, (int(coords[0]), int(coords[1])), 10, color, 2)
             
            cv2.imshow("Video", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()