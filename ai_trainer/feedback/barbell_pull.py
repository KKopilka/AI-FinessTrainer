from typing import Tuple, Dict, List
import math
import numpy as np
from sklearn.metrics import euclidean_distances as dist
from ai_trainer.direction_counter import TaskCounter

taskCounter = TaskCounter()

def counts_calculate_barbell_pull(kps: np.ndarray, correct: int):
    print(f"counts_calculate: {correct}")
    angle = get_angle(kps)
    per = np.interp(angle, (30, 80), (0, 100))
    taskCounter.Count(per, correct == 1)

    return [taskCounter.correctCount, taskCounter.ErrorAmount()]

def estimate_pose_angle(a, b, c):
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
    # print("angle: ", angle)
    return angle

def get_angle(kps: np.ndarray) -> float: 
    right_shoulder = kps[6]
    right_elbow = kps[8]
    right_hip = kps[12]

    left_hip = kps[11]
    left_shoulder = kps[5]
    left_elbow = kps[7]
    angle_l = estimate_pose_angle(left_elbow, left_shoulder, left_hip)
    angle_r = estimate_pose_angle(right_elbow, right_shoulder, right_hip)
    # print("1111111111", angle_r)
    # knee_vertical_angle_right = find_angle(right_hip, np.array([right_knee[0], 0, 0]), right_knee)
    # knee_vertical_angle_left = find_angle(left_hip, np.array([left_knee[0], 0, 0]), left_knee)
    # print(knee_vertical_angle_right, knee_vertical_angle_left)
    # print("angle: ", angle_r)
    avg_angle = (angle_l + angle_r) / 2
    print("angle2: ", avg_angle)
    
    return avg_angle

def are_elbow_bending(kps: np.ndarray) -> bool:
    right_shoulder = kps[6]
    right_elbow = kps[8]
    right_hip = kps[12]

    left_hip = kps[11]
    left_shoulder = kps[5]
    left_elbow = kps[7]

    angle_l = estimate_pose_angle(left_elbow, left_shoulder, left_hip)
    angle_r = estimate_pose_angle(right_elbow, right_shoulder, right_hip)
    avg_angle = (angle_l + angle_r) / 2
    
    return avg_angle > 70

initial_left_elbow = [0, 0, 0]
initial_right_elbow = [0, 0, 0]

def elbows_higher_than_shoulders(kps: np.ndarray) -> bool:
    global initial_left_elbow, initial_right_elbow
    right_shoulder = kps[6]
    right_elbow = kps[8]

    left_shoulder = kps[5]
    left_elbow = kps[7]
    
    print(right_elbow, right_shoulder)
    if int(right_elbow[1]) == int(right_shoulder[1]):
        initial_right_elbow = right_elbow

    if int(left_elbow[1]) == int(left_shoulder[1]):
        initial_left_elbow = left_elbow

    print("l ", initial_left_elbow)
    print("r ", initial_right_elbow)
    are_elbows_higher_than_shoulders = (
        (right_elbow[1] < initial_right_elbow[1]) and (left_elbow[1] < initial_left_elbow[1])
    )

    return are_elbows_higher_than_shoulders

def is_in_start_position(kps: np.ndarray) -> bool:
    right_shoulder = kps[6]
    right_elbow = kps[8]
    right_wrist = kps[10]

    left_shoulder = kps[5]
    left_elbow = kps[7]
    left_wrist = kps[9]

    are_elbows_higher_than_wrists = (
        (right_elbow[1] < right_wrist[1]) and (left_elbow[1] < left_wrist[1])
    )
    # dist_wrists_shoulder = (dist([right_wrist], [right_shoulder])[0][0] + dist([left_wrist], [left_shoulder])[0][0]) / 2
    # dist_elbows_shoulder = (dist([right_elbow], [right_shoulder])[0][0] + dist([left_elbow], [left_shoulder])[0][0]) / 2
    # margin = 0.4 * dist_elbows_shoulder
    # are_wrists_closer_2_shoulders_than_elbows = dist_wrists_shoulder < dist_elbows_shoulder + margin
    return are_elbows_higher_than_wrists

def give_feedback_barbell_pull(kps: np.ndarray) -> Tuple[Dict, List, List]:
    feedback = {'is_in_position': False}
    feedback_flag = False
    possible_corrections = ['elbows_position']
               
    if is_in_start_position(kps):
        feedback['is_in_position'] = True
        # if are_elbow_bending(kps):

        if elbows_higher_than_shoulders(kps):
            feedback["elbows_position"] = "Elbows should be above the shoulders!!!"
            feedback_flag = True
                


    pointsofinterest = []
    return (feedback, possible_corrections, pointsofinterest, feedback_flag)
