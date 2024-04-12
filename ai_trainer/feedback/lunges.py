"""This script gives you feedback on your Lunges technique.

It includes fucntions to check three things:
    - Are your feet at shoulder width?
    - Are your elbows up?
    - Are your knees strong or caving inwards?
    
And gives you feedback on how to correct them if needed.
"""
from typing import Tuple, Dict, List
import math
import numpy as np
import cv2
from sklearn.metrics import euclidean_distances as dist

def get_bending_angle(hip: np.ndarray, knee: np.ndarray, ankle: np.ndarray)->float:
    """Get the bending angle of the leg/knee.
    
    Note: all keypoints must be not normalized and from the same leg.

    Args:
        hip (np.ndarray): not normalized hip keypoint.
        knee (np.ndarray): not normalized knee keypoint.
        ankle (np.ndarray): not normalized ankle keypoint.

    Returns:
        angle_degrees(float): knee bending angle in degrees.
    """
    # получаем координаты точек
    # _, x1, y1 = hip
    # _, x2, y2 = knee
    # _, x3, y3 = ankle

    # angle_degrees = math.degrees(math.atan2(y3 - y2, x3 - x2) -
    #                         math.atan2(y1 - y2, x1 - x2))
    # if angle_degrees < 0:
    #         angle_degrees += 180

    # return angle_degrees
    # femur
    line1 = ((hip[2], hip[1]), (knee[2], knee[1])) # 2=z, 1=y
    #tibia
    line2 = ((knee[2], knee[1]), (ankle[2], ankle[1]))

    # Calculate the direction vectors of the lines
    vector1 = (line1[1][0] - line1[0][0], line1[1][1] - line1[0][1])
    vector2 = (line2[1][0] - line2[0][0], line2[1][1] - line2[0][1])

    # Calculate the dot product of the two direction vectors
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

    # Calculate the magnitudes of the vectors
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

    # Calculate the cosine of the angle between the lines
    cosine_theta = dot_product / (magnitude1 * magnitude2)

    # Calculate the angle in radians
    angle_radians = math.acos(cosine_theta)

    # Convert the angle to degrees
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def are_lunges_proper_left(kps: np.ndarray) -> bool:
    left_hip = kps[24]
    left_knee = kps[26]
    left_ankle = kps[28]
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
    
    right_shoulder = kps[11]
    right_hip = kps[23]

    left_shoulder = kps[12]
    left_hip = kps[24]

    hip_vertical_angle_right = find_angle_back(right_shoulder, np.array([right_hip[0], 0, 0]), right_hip)
    hip_vertical_angle_left = find_angle_back(left_shoulder, np.array([left_hip[0], 0, 0]), left_hip)

    print("l", hip_vertical_angle_left, "r", hip_vertical_angle_right)
    if (50 > hip_vertical_angle_right > 20) and \
         (50 > hip_vertical_angle_left > 20): 
        return True
    else:
        return False


def give_feedback(kps: np.ndarray)->Tuple[Dict, List]:
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
    possible_corrections = ['knee_bend', 'feet_position', 'elbow_position', 'knee_position']

   
 
    if position_back(kps):
        feedback["knee_position"] = "Right"
    else:
        feedback["knee_position"] = "Bad"
    # if are_lunges_proper_right(kps):
    #     feedback["knee_position"] = "Right"
        
    # else:
    #     feedback["knee_position"] = "The knee angle is not 90 degrees"
    return (feedback, possible_corrections)