from typing import Tuple, Dict, List
import math
import cv2
import cv2.text
import numpy as np
from sklearn.metrics import euclidean_distances as dist
from ai_trainer.properties import DirectionCounter


def calculate_angle1(point_a: np.ndarray, point_b: np.ndarray, point_c: np.ndarray) -> float:
    """Calculate the angle between three points."""
    ba = point_a - point_b
    bc = point_c - point_b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    angle = np.degrees(angle)
    return angle

def calculate_angle(a, b, c) -> float:
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

def right_angle(kps: np.ndarray) -> bool:
    right_shoulder = kps[6]
    left_shoulder = kps[5]
    right_elbow = kps[8]
    left_elbow = kps[7]
    right_wrist = kps[10]
    left_wrist = kps[9]

    right_hand = calculate_angle(right_shoulder, right_elbow, right_wrist)
    left_hand = calculate_angle(left_shoulder, left_elbow, left_wrist)
    print("r: ", right_hand)
    print("l: ", left_hand)
    return right_hand and left_hand


def is_in_start_position1(kps: np.ndarray) -> bool:
    # Получаем координаты точек носа, правого и левого плеча
    nose = kps[0]
    right_shoulder = kps[6]
    left_shoulder = kps[5]

    # Проверяем, что все точки видны на изображении (Z-координата больше 0)
    return all(coord[2] > 0 for coord in [nose, right_shoulder, left_shoulder])


def is_in_start_position(kps: np.ndarray) -> bool:
    right_shoulder = kps[6]
    right_elbow = kps[8]
    right_wrist = kps[10]

    left_shoulder = kps[5]
    left_elbow = kps[7]
    left_wrist = kps[9]

    # Calculate angles between elbows and wrists
    right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    

    # Define the threshold for straight arms
    threshold_angle = 170  # in degrees

    # Check if angles are greater than threshold (arms are straight)
    are_arms_straight = (right_angle > threshold_angle) and (left_angle > threshold_angle)

    # Check if wrists are slightly wider than shoulders
    wrist_shoulder_distance = np.linalg.norm(right_shoulder - right_wrist) + np.linalg.norm(left_shoulder - left_wrist)
    shoulder_distance = np.linalg.norm(right_shoulder - left_shoulder)
    are_wrists_wider_than_shoulders = wrist_shoulder_distance > 1.05 * shoulder_distance  # assuming 5% wider
    
    return are_arms_straight and are_wrists_wider_than_shoulders

def wrists_wider_than_shoulders(kps: np.ndarray) -> bool:
    right_shoulder = kps[6]
    left_shoulder = kps[5]
    right_wrist = kps[10]
    left_wrist = kps[9]

    shoulders_width = dist([right_shoulder], [left_shoulder])[0][0]
    wrists_width = dist([right_wrist], [left_wrist])[0][0]
    margin = 0.6 * shoulders_width
    print("s", shoulders_width)
    print("w", wrists_width)
    print("margin: ", margin)
    # return wrists_width < shoulders_width + margin
    return shoulders_width - margin < wrists_width < shoulders_width + margin


def give_feedback_push_up(kps: np.ndarray, count: int) -> Tuple[Dict, List, int]:
    feedback = {'is_in_position': False}
    possible_corrections = ['wrist_bad', 'start_position', "angle"]
    # if is_in_start_position1(kps):
    if is_in_start_position(kps):
        feedback['is_in_position'] = True
        if wrists_wider_than_shoulders(kps):
            feedback['wrist_bad'] = "Place your hands wider than your shoulders!!!"
        # if right_angle(kps):
        #     feedback['angle'] = "Right!!!"
    # else:
    #     feedback['is_in_position'] = False
    #     feedback['start_position'] = "Get into the starting position!!!"
          
        
                
                
    return (feedback, possible_corrections, count)
