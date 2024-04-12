"""This script gives you feedback on your Front Squad technique.

It includes fucntions to check three things:
    - Are your feet at shoulder width?
    - Are your elbows up?
    - Are your knees strong or caving inwards?
    
And gives you feedback on how to correct them if needed.
"""
from typing import Tuple, Dict, List
import math
import numpy as np
from sklearn.metrics import euclidean_distances as dist

def elbow_inclination(shoulder: np.ndarray, elbow: np.ndarray)->float:
    """Calculate the anle between the vertical and the humerus.
    
    The humerus is defined as the line between the shoulder and the elbow joints
    of the same arm.

    Args:
        shoulder (np.ndarray): shoulder joint x, y, z coordinates. 
        elbow (np.ndarray): elbow joint x, y, z coordinates.

    Returns:
        angle_with_vertical_axis(float): angle between the vertical and the humerus expressed
            in degrees.
    """
    x1, __, z1 = shoulder
    x2, __, z2 = elbow
    # Calculate the angle using the arctangent function
    angle_radians = math.atan2(x2 - x1, z2 - z1)
    # Convert the angle from radians to degrees
    angle_degrees = math.degrees(angle_radians)
    angle_with_vertical_axis = np.abs(90 - np.abs(angle_degrees))

    return angle_with_vertical_axis

def are_elbows_down(kps: np.ndarray)->bool:
    """Check if elbows are lower than they should be for a good form.

    Args:
        kps (np.ndarray): denormalized 3d pose keypoints.

    Returns:
        bool: True if the angle between the vertical and both humerus is bigger than 45 degrees.
    """
    right_shoulder = kps[11]
    right_elbow = kps[13]
    left_shoulder = kps[12]
    left_elbow = kps[14]

    angle_right = elbow_inclination(right_shoulder, right_elbow)
    angle_left = elbow_inclination(left_shoulder, left_elbow)
    return (angle_right > 45) and (angle_left > 45)

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
    #femur
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

def are_knees_bending(kps: np.ndarray)->bool:
    """Check if knees are bending of if the legs are straight.

    Args:
        kps (np.ndarray): denormalized 3d pose keypoints.

    Returns:
        bool: True if knees are bending. False if legs are straight. Knees are considered
            to be bending if the bending angle is bigger than 50 degrees. The bending angle
            is the angle between the femur and the tibia, in degrees.
    """
    right_hip = kps[23]
    right_knee = kps[25]
    right_ankle = kps[27]

    left_hip = kps[24]
    left_knee = kps[26]
    left_ankle = kps[28]

    right_leg_angle = get_bending_angle(right_hip, right_knee, right_ankle)
    left_leg_angle = get_bending_angle(left_hip, left_knee, left_ankle)
    avg_angle = (left_leg_angle + right_leg_angle) / 2

    return avg_angle > 50

def are_knees_caving(kps: np.ndarray)->bool:
    """Check if knees are caving inwards.

    Args:
        kps (np.ndarray): denormalized 3d pose keypoints.

    Returns:
        bool: True if knees are caving inwards. False if knees are not caving inwards.
            knees are considered to be caving inwards if the distance between the knees
            is smaller than the distance between the ankles.
    """
    # si las rodillas estan más juntas que los tobillos, están caving
    right_knee = kps[25]
    right_ankle = kps[27]
    left_knee = kps[26]
    left_ankle = kps[28]

    ankles_width = dist([right_ankle], [left_ankle])[0][0]
    #ankles_width = dist([kps[11]], [kps[12]])[0][0]
    knees_width = dist([right_knee], [left_knee])[0][0]

    margin = 0.15 * ankles_width
    return knees_width < ankles_width - margin

def is_in_start_position(kps: np.ndarray)->bool:
    """Check if the person is in the start position of the front squat.

    Args:
        kps (np.ndarray): denormalized 3d pose keypoints.

    Returns:
        bool: True if the person's wrists are above the shoulders. In other words,
            the person is in the start position of the front squat. False otherwise.
    """
    # wrists higher than elbows and closer to the sholders than the elbows are
    right_shoulder = kps[11]
    right_elbow = kps[13]
    right_wrist = kps[15]

    left_shoulder = kps[12]
    left_elbow = kps[14]
    left_wrist = kps[16]

    are_wrists_higher_than_elbows = (
        (right_wrist[1] < right_elbow[1]) and (left_wrist[1] < left_elbow[1])
    )

    dist_wrists_shoulder = (dist([right_wrist], [right_shoulder])[0][0] + dist([left_wrist], [left_shoulder])[0][0]) / 2
    dist_elbows_shoulder = (dist([right_elbow], [right_shoulder])[0][0] + dist([left_elbow], [left_shoulder])[0][0]) / 2
    margin = 0.4 * dist_elbows_shoulder
    are_wrists_closer_2_shoulders_than_elbows = dist_wrists_shoulder < dist_elbows_shoulder + margin
    return are_wrists_higher_than_elbows and are_wrists_closer_2_shoulders_than_elbows

def are_feet_well_positioned(kps: np.ndarray)->bool:
    """Check if the person's feet are well positioned for doing a front squat.

    Check if the person's feet are at shoulder width.

    Args:
        kps (np.ndarray): denormalized 3d pose keypoints.

    Returns:
        bool: True if the person's feet are at shoulder width. False otherwise.
    """
    # feet at approximately shoulder width
    right_ankle = kps[27]
    left_ankle = kps[28]
    right_shoulder = kps[11]
    left_shoulder = kps[12]

    ankles_width = dist([right_ankle], [left_ankle])[0][0]
    shoulders_width = dist([right_shoulder], [left_shoulder])[0][0]
    margin = 0.8 * shoulders_width
    return shoulders_width - margin < ankles_width < shoulders_width + margin

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

    if is_in_start_position(kps):
        feedback['is_in_position'] = True
        if not are_feet_well_positioned(kps):
            feedback['feet_position'] = "Feet should be at shoulder width!!!"
        if are_elbows_down(kps):
            feedback['elbow_position'] = "Rise your elbows!!!"
        if are_knees_bending(kps):
            if are_knees_caving(kps):
                feedback["knee_position"] = "Open your knees!!!"
    return (feedback, possible_corrections)
