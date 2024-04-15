"""This script gives you feedback on your front squad technique."""
import argparse
import cv2
import numpy as np
from ai_trainer.properties import *
from ai_trainer.models import BlazePoseModel
from ai_trainer.drawing import draw_pose, draw_text, draw_rectangle
from ai_trainer.feedback.front_squat import give_feedback
from AudioCommSys import *
from ai_trainer.properties import *

def main():
    illustrate_exercise("frontalniye-prisedaniya.jpeg")
    # Инициализация модели BlazePose
    blazepose_model = BlazePoseModel(model_path="./models/blazepose_full.onnx")
    
    # Открытие видеопотока с веб-камеры
    cap = cv2.VideoCapture("assets/left_side_cut.mp4")
    
    # Инициализация счетчика и направления движения
    count = 0
    dirr = 1

    
    dCounter = DirectionCounter()
    
    while cap.isOpened():
        _, frame = cap.read()

        if not frame.any():
            break
        
        # Изменение размера кадра
        frame = cv2.resize(frame, (800, 700), interpolation=cv2.INTER_AREA)
        
        # Получение ключевых точек с помощью модели BlazePose
        kps = blazepose_model.predict([cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)])[0]
        
        # Проверка, что есть нормализованные ключевые точки
        probs = kps.T[3]
        if not all(probs<0):
            # Получение 3D координат ключевых точек
            x, y, z = kps.T[:3]
            pose_3d = np.column_stack((x, y, z))
            
            # Отрисовка скелета на изображении
            frame = draw_pose(
                image=frame,
                keypoints=pose_3d,
                disposition="mediapipe",
                thickness=2,
            )
            # frame = draw_rectangle(
            #     image=frame,
            #     origin=(100, 100),  # Ваша точка origin, например, (100, 100)
            #     width=100,  # Ширина прямоугольника
            #     height=200,  # Высота прямоугольника
            #     color=(0, 255, 0),  # Цвет прямоугольника в формате (R, G, B)
            #     thickness=3,  # Толщина линии прямоугольника
            # )
           

            # Получение обратной связи о выполнении упражнения
            feedback, possible_corrections, count = give_feedback(pose_3d, count)
            
            # Проверка наличия коррекций и вывод их на изображение
            for correction in possible_corrections:
                if correction in list(feedback.keys()):
                    frame = draw_text(
                        image=frame,
                        text=feedback[correction],
                        origin=(10, 100),
                        font_scale=0.8,
                        color=(50, 50, 250),
                        thickness=2,
                    )
                  
                    # print("1",count)
            # print(count)
            # Вывод значения счетчика на изображение
            cv2.putText(frame, f'Count: {count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
 
        # Отображение кадра
        cv2.imshow('Video', frame)
        
        # Обработка нажатия клавиши q для выхода из цикла
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Освобождение видеопотока и закрытие всех окон OpenCV
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
