from typing import Tuple, Dict, List
import math
import numpy as np
from sklearn.metrics import euclidean_distances as dist
from ai_trainer.pac import PointAccumulator

left_elbow_accum = PointAccumulator(100, True, False, False)
right_elbow_accum = PointAccumulator(100, True, False, False)

from ai_trainer.direction_counter import TaskCounter

taskCounter = TaskCounter()

def counts_calculate_biceps(kps: np.ndarray, correct: int):
    # print(f"counts_calculate: {dirr} {count}")
    angle = get_angle(kps)
    per = np.interp(angle, (28, 165), (0, 100))
    taskCounter.Count(per, correct == 1)

    return [taskCounter.correctCount, taskCounter.ErrorAmount()]

def estimate_pose_angle(a, b, c) -> float:
    """
    Calculate the pose angle for object.

    Args:
        a (float) : The value of pose point a
        b (float): The value of pose point b
        c (float): The value o pose point c

    Returns:
        angle (degree): Degree value of angle between three points
    """
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def get_angle(kps: np.ndarray) -> float:
    right_shoulder = kps[6]
    left_shoulder = kps[5]
    right_elbow = kps[8]
    left_elbow = kps[7]
    right_wrist = kps[10]
    left_wrist = kps[9]

    right_hand = estimate_pose_angle(right_shoulder, right_elbow, right_wrist)
    left_hand = estimate_pose_angle(left_shoulder, left_elbow, left_wrist)
    avg_angle = (right_hand + left_hand) / 2
    # print("angle: ", avg_angle)
    return avg_angle

def are_feet_well_positioned(kps: np.ndarray) -> bool:
    right_ankle = kps[16]
    left_ankle = kps[15]
    right_shoulder = kps[6]
    left_shoulder = kps[5]

    ankles_width = dist([right_ankle], [left_ankle])[0][0]
    shoulders_width = dist([right_shoulder], [left_shoulder])[0][0]
    margin = 0.7 * shoulders_width
    return shoulders_width - margin < ankles_width < shoulders_width + margin

def elbow_position_first(kps: np.ndarray, initial_left_elbow, initial_right_elbow) -> bool:
    left_elbow = kps[7]
    right_elbow = kps[8]
    right_shoulder = kps[6]
    left_shoulder = kps[5]

    acc_left_elbow = left_elbow_accum.val()
    if not isinstance(acc_left_elbow, (np.ndarray)):
        acc_left_elbow = [0,0]

    acc_right_elbow = right_elbow_accum.val()
    if not isinstance(acc_right_elbow, (np.ndarray)):
        acc_right_elbow = [0,0]
    
     # Проверяем, если значение координаты Y локтя стало меньше начального значения
    left_elbow_moved_down = left_elbow[1] - acc_left_elbow[1] < -5 
    right_elbow_moved_down = right_elbow[1] - acc_right_elbow[1] < -5 
    # # Если хотя бы один из локтей двигается вниз, перезаписываем начальные позиции локтей
    # if left_elbow_moved_down or right_elbow_moved_down:
    #     initial_left_elbow = left_elbow.copy()
    #     initial_right_elbow = right_elbow.copy()

    # Проверяем, если значение координаты Y локтя стало больше начального значения
    left_elbow_moved_up = left_elbow[1] - acc_left_elbow[1] > 5
    right_elbow_moved_up = right_elbow[1] - acc_right_elbow[1] > 5
    # print('not: ', not_right)
    # print("right_elbow: ", right_elbow)
    # print("left_elbow: ", left_elbow)
    # print("initial_right_elbow: ", acc_right_elbow)
    # print("initial_left_elbow: ", acc_left_elbow)

    left_elbow_accum.store(left_elbow)
    right_elbow_accum.store(right_elbow)

    if left_elbow_moved_up or right_elbow_moved_up:
        return 1
    elif left_elbow_moved_down or right_elbow_moved_down:
        return 2
    else:
        return 0

# def elbow_position_first(kps: np.ndarray, initial_left_elbow, initial_right_elbow) -> bool:
#     left_elbow = kps[7]
#     right_elbow = kps[8]
#     right_shoulder = kps[6]
#     left_shoulder = kps[5]
#     print(initial_left_elbow, initial_right_elbow)
#     # Разница в координатах X и Y локтей относительно начальных значений
#     delta_x_left = left_elbow[0] - initial_left_elbow[0]
#     delta_y_left = left_elbow[1] - initial_left_elbow[1]

#     delta_x_right = right_elbow[0] - initial_right_elbow[0]
#     delta_y_right = right_elbow[1] - initial_right_elbow[1]

#     # Вычисление относительного положения локтя относительно плеч
#     distance_from_left_shoulder = abs(left_elbow[0] - left_shoulder[0])
#     distance_from_right_shoulder = abs(right_elbow[0] - right_shoulder[0])

#     # Проверяем, если локти движутся вперед относительно начального положения
#     if delta_y_left > 0 or delta_y_right > 0:
#         # Проверяем, если локти находятся ближе к плечам, чем в начальном положении
#         if distance_from_left_shoulder < abs(initial_left_elbow[0] - left_shoulder[0]) or \
#                 distance_from_right_shoulder < abs(initial_right_elbow[0] - right_shoulder[0]):
#             print("Elbow moving forward")
#             return True
#     print("Elbow not moving forward")
#     return False

initial_left_elbow = [0, 0, 0]
initial_right_elbow = [0, 0, 0]
initial_position_set = False

def is_in_start_position(kps: np.ndarray) -> bool:
    global initial_left_elbow, initial_right_elbow, initial_position_set

    right_ankle = kps[16]
    left_ankle = kps[15]
    left_shoulder = kps[5]
    right_shoulder = kps[6]
    left_elbow = kps[7]
    right_elbow = kps[8]
    left_wrist = kps[9]
    right_wrist = kps[10]

    # Условие для проверки положения рук: руки должны быть вдоль тела
    hands_down = (left_elbow[1] > left_wrist[1]) and (right_elbow[1] > right_wrist[1])

    ankles_width = dist([right_ankle], [left_ankle])[0][0]
    shoulders_width = dist([right_shoulder], [left_shoulder])[0][0]
    margin = 0.7 * shoulders_width
    legs_correct = shoulders_width - margin < ankles_width < shoulders_width + margin

    # legs_correct = True

    if hands_down and legs_correct and not initial_position_set:
        initial_left_elbow = left_elbow
        initial_right_elbow = right_elbow
        initial_position_set = True  # Устанавливаем флаг, что начальная позиция сохранена
        print(f"Initial positions set: Left Elbow: {initial_left_elbow}, Right Elbow: {initial_right_elbow}")
        return True
    elif initial_position_set:
        print("Initial position already set.")
        return True
    return False


def give_feedback_biceps(kps: np.ndarray) -> Tuple[Dict, List, List]:
    feedback = {'is_in_position': False}
    
    feedback_flag = False
    possible_corrections = ['feet_position', 'elbow_position', 'elbow_position_second']
    if is_in_start_position(kps):
        feedback['is_in_position'] = True
        if not are_feet_well_positioned(kps):
            feedback['feet_position'] = "Feet should be at shoulder width!!!"
            feedback_flag = True
        elbowPosition = elbow_position_first(kps, initial_left_elbow, initial_right_elbow)
        if elbowPosition == 1:
            feedback['elbow_position'] = "Put your elbows up!!!"
            feedback_flag = True
        elif elbowPosition == 2:
            feedback['elbow_position'] = "Put your elbows down!!!"
            feedback_flag = True
        
    acc_left_elbow = left_elbow_accum.val()
    if not isinstance(acc_left_elbow, (np.ndarray)):
        acc_left_elbow = [0,0]
    acc_right_elbow = right_elbow_accum.val()
    if not isinstance(acc_right_elbow, (np.ndarray)):
        acc_right_elbow = [0,0] 
          
    pointsofinterest = [
        {
            'valid': True,
            'coords': np.rint(acc_left_elbow[:2]),
            'id': 1,
        },
        {
            'valid': True,
            'coords': np.rint(acc_right_elbow[:2]),
            'id': 2,
        },
        #np.rint(acc_left_elbow[:2]),
        #np.rint(acc_right_elbow[:2])
    ]
    if 'elbow_position' in feedback:
        pointsofinterest[0]['valid'] = False
        pointsofinterest[1]['valid'] = False
        # pointsofinterest.append(np.rint(acc_left_elbow[:2]))
        # pointsofinterest.append(np.rint(acc_right_elbow[:2]))
                
                
    return (feedback, possible_corrections, pointsofinterest, feedback_flag)