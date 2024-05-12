from typing import Tuple, Dict, List
import math
import numpy as np
from sklearn.metrics import euclidean_distances as dist
from ai_trainer.direction_counter import TaskCounter

taskCounter = TaskCounter()

def counts_calculate_reverse_push_up(kps: np.ndarray, correct: int):
    # print(f"counts_calculate: {dirr} {count}")
    angle = get_angle(kps)
    per = np.interp(angle, (170, 100), (0, 100))
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
    if all(right_elbow[:2]) == 0 and all(right_wrist[:2]) == 0:
        avg_angle = left_hand
        print('1')

    elif all(left_elbow[:2]) == 0 and all(left_wrist[:2]) == 0:
        avg_angle = right_hand
        print('2')
 
    else:
        avg_angle = (right_hand + left_hand) / 2
        print('3')
        return avg_angle
    print("angle: ", avg_angle)
    return avg_angle

def elbow_inclination(shoulder: np.ndarray, elbow: np.ndarray) -> float:
    a = shoulder
    b = elbow

    angle_radians = math.atan2(b[1] - a[1], b[0] - a[0]) 
    angle_degrees = math.degrees(angle_radians)
    angle_with_vertical_axis = angle_degrees - 90
    if angle_with_vertical_axis < 0:
        angle_with_vertical_axis += 360

    if angle_with_vertical_axis > 180:
        angle_with_vertical_axis -= 360
        angle_with_vertical_axis = np.abs(angle_with_vertical_axis)

    return angle_with_vertical_axis

def hip_position(kps: np.ndarray) -> bool:
    right_hip = kps[12]
    right_shoulder = kps[6]
    right_wrist = kps[10]

    left_hip = kps[11]
    left_wrist = kps[9]
    left_shoulder = kps[5]

    right_knee = kps[14]
    right_ankle = kps[16]

    angle_right = elbow_inclination(right_shoulder, right_hip)
    angle_left = elbow_inclination(left_shoulder, left_hip)
    print("a: ", angle_right)
    # print("distance_r  ", distance_r)
    # threshold = 110
    return (angle_right > 17) and (angle_left > 17)
    # return distance_r > threshold 

def is_in_start_position(kps: np.ndarray) -> bool:
    right_hip = kps[12]
    right_shoulder = kps[6]
    right_wrist = kps[10]

    left_hip = kps[11]
    left_wrist = kps[9]
    left_shoulder = kps[5]

    right_knee = kps[14]
    right_ankle = kps[16]

    angle_right = elbow_inclination(right_shoulder, right_hip)
    angle_left = elbow_inclination(left_shoulder, left_hip)

    hip_position = ((angle_right < 17) and (angle_left < 17))

    angle = estimate_pose_angle(right_shoulder, right_hip, right_knee)
    print("111 ", angle)
    return hip_position and (90 <= angle < 130)


def give_feedback_reverse_push_up(kps: np.ndarray) -> Tuple[Dict, List, List]:
    feedback = {'is_in_position': False}
    feedback_flag = False
    possible_corrections = ['hip_position']

    if is_in_start_position(kps):
        feedback['is_in_position'] = True
        if hip_position(kps):
            feedback['hip_position'] = "The pelvis is too far away from the hands!!!"
            feedback_flag = True
      
                
    pointsofinterest = []         
    return (feedback, possible_corrections, pointsofinterest, feedback_flag)
