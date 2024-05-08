from typing import Tuple, Dict, List
import math
import numpy as np
import cv2
from sklearn.metrics import euclidean_distances as dist


def are_lunges_proper_left(kps: np.ndarray) -> bool:
    left_hip = kps[11]
    left_knee = kps[13]
    left_ankle = kps[15]
    left_foot = kps[32]

    left_leg_angle = get_bending_angle(left_hip, left_knee, left_ankle)

    print("l", left_leg_angle)
    if (left_knee[0] < left_foot[0]) and (left_leg_angle < 100):
        return False
    if (left_knee[0] > left_foot[0]) and (left_leg_angle < 100):
        return True

def are_lunges_proper_right(kps: np.ndarray) -> bool:
    right_hip = kps[23]
    right_knee = kps[25]
    right_ankle = kps[27]
    right_foot = kps[31]

    right_leg_angle = get_bending_angle(right_hip, right_knee, right_ankle)

    print("r", right_leg_angle)

    if (right_knee[0] > right_foot[0]) and (right_leg_angle < 100):
        return False
    if (right_knee[0] < right_foot[0]) and (right_leg_angle < 100):
        return True


def find_angle_back(p1, p2, ref_pt = np.array([0,0,0])):
    p1_ref = p1 - ref_pt
    p2_ref = p2 - ref_pt

    cos_theta = (np.dot(p1_ref,p2_ref)) / (1.0 * np.linalg.norm(p1_ref) * np.linalg.norm(p2_ref))
    theta = np.arccos(np.clip(cos_theta, -1.0, 1.0))
            
    degree = int(180 / np.pi) * theta

    return int(degree)

def position_back(kps: np.ndarray) -> bool:
    right_shoulder = kps[6]
    right_hip = kps[12]

    left_shoulder = kps[5]
    left_hip = kps[11]

    hip_vertical_angle_right = find_angle_back(right_shoulder, np.array([right_hip[0], 0, 0]), right_hip)
    hip_vertical_angle_left = find_angle_back(left_shoulder, np.array([left_hip[0], 0, 0]), left_hip)

    print("l", hip_vertical_angle_left, "r", hip_vertical_angle_right)
    if (50 > hip_vertical_angle_right > 20) and \
         (50 > hip_vertical_angle_left > 20): 
        return True
    else:
        return False

def is_lunge_start_position(kps: np.ndarray) -> bool:
    """Check if the person is in the start position of the lunge exercise.

    Args:
        kps (np.ndarray): denormalized 3d pose keypoints.

    Returns:
        bool: True if one of the legs is stepped back, not too far, and the back is slightly leaned forward.
              False otherwise.
    """
    right_hip = kps[12]
    left_hip = kps[11]

    # Check if one of the legs is stepped back
    is_one_leg_stepped_back = (right_hip[1] < 0.95) or (left_hip[1] < 0.95)

    # Check if the back is slightly leaned forward
    is_back_leaned_forward = position_back(kps)

    return is_one_leg_stepped_back and is_back_leaned_forward

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

def get_angle(kps: np.ndarray)->float:
    """Check if knees are bending of if the legs are straight.

    Args:
        kps (np.ndarray): denormalized 3d pose keypoints.

    Returns:
        bool: True if knees are bending. False if legs are straight. Knees are considered
            to be bending if the bending angle is bigger than 50 degrees. The bending angle
            is the angle between the femur and the tibia, in degrees.
    """
    
    right_hip = kps[12]
    right_knee = kps[14]
    right_ankle = kps[16]

    left_hip = kps[11]
    left_knee = kps[13]
    left_ankle = kps[15]
    angle_l = estimate_pose_angle(left_hip, left_knee, left_ankle)
    angle_r = estimate_pose_angle(right_hip, right_knee, right_ankle)
    # print("1111111111", angle_r)
    # knee_vertical_angle_right = find_angle(right_hip, np.array([right_knee[0], 0, 0]), right_knee)
    # knee_vertical_angle_left = find_angle(left_hip, np.array([left_knee[0], 0, 0]), left_knee)
    # print(knee_vertical_angle_right, knee_vertical_angle_left)
    # print("angle: ", angle_r)
    # avg_angle = (angle_l + angle_r) / 2
    # avg_angle = np.interp(angle_r, (20, 60), (0, 100))
    print("angle2: ", angle_l, angle_r)
    
    return angle_l, angle_r

from ai_trainer.direction_counter import TaskCounter

taskCounter = TaskCounter()

def counts_calculate_lunges(kps: np.ndarray, correct: int):
    print(f"counts_calculate: {correct}")
    angle_l, angle_r = get_angle(kps)
    per = np.interp(angle_l, (85, 160), (0, 100))
    taskCounter.Count(per, correct == 1)

    return [taskCounter.correctCount, taskCounter.ErrorAmount()]

def give_feedback_lunges(kps: np.ndarray)->Tuple[Dict, List]:
    """Give feedback on the person's front squat technique.
    
    The feedback is given in the form of a dictionary with the following keys:
        - is_in_position: True if the person is in the start position of the front squat.
            False otherwise.
        - feet_position: "Your feet should be at shoulder width!!!" if the person's feet
            are not at shoulder width. None otherwise.
        - elbow_position: "Rise your elbows!!!" if the person's elbows are lower than they
            should be. None otherwise.
        - knee_position: "Open your knees!!!" if the person's knees are caving inwards.
            None otherwise.

    Args:
        kps (np.ndarray): denormalized 3d pose keypoints.

    Returns:
        feedback (Dict): feedback on the person's front squat technique.
        possible_corrections (List): possible corrections to the person's front squat technique.
    """
    feedback = {'is_in_position': False}
    feedback_flag = False
    possible_corrections = ['knee_bend', 'feet_position', 'elbow_position', 'knee_position']
    if position_back(kps):
        feedback["knee_position"] = "Right"
        feedback_flag = True
    else:
        feedback["knee_position"] = "Bad"
        feedback_flag = True
    # if are_lunges_proper_right(kps):
    #     feedback["knee_position"] = "Right"
        
    # else:
    #     feedback["knee_position"] = "The knee angle is not 90 degrees"
    pointsofinterest = []
    return (feedback, possible_corrections, pointsofinterest, feedback_flag)
