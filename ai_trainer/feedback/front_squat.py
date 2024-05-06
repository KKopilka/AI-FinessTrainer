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
    a = shoulder
    b = elbow
    # Calculate the angle using the arctangent function
    angle_radians = math.atan2(b[2] - a[2], b[0] - a[0])
    # Convert the angle from radians to degrees
    angle_degrees = math.degrees(angle_radians)
    angle_with_vertical_axis = np.abs(90 - np.abs(angle_degrees))
    # print("angle_with_vertical_axis: ", angle_with_vertical_axis)
    return angle_with_vertical_axis

def are_elbows_down(kps: np.ndarray)->bool:
    """Check if elbows are lower than they should be for a good form.

    Args:
        kps (np.ndarray): denormalized 3d pose keypoints.

    Returns:
        bool: True if the angle between the vertical and both humerus is bigger than 45 degrees.
    """
    right_shoulder = kps[6]
    right_elbow = kps[8]
    left_shoulder = kps[5]
    left_elbow = kps[7]

    angle_right = elbow_inclination(right_shoulder, right_elbow)
    angle_left = elbow_inclination(left_shoulder, left_elbow)
    # print("1", angle_right)
    # print("2", angle_left)
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

def find_angle2(p1, p2, p3, draw = True):
        # Get the landmarks
        x1, y1 = p1[1:]
        x2, y2 = p2[1:]
        x3, y3 = p3[1:]
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        # print("0: ", angle)
        if angle < 0:
            angle += 360
        # print("1: ", angle)
        return angle

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


def find_angle(p1, p2, ref_pt = np.array([0,0,0])):
    # print("p1: ", p1)
    # print("p2: ", p2)
    p1_ref = p1 - ref_pt
    p2_ref = p2 - ref_pt

    cos_theta = (np.dot(p1_ref,p2_ref)) / (1.0 * np.linalg.norm(p1_ref) * np.linalg.norm(p2_ref))
    theta = np.arccos(np.clip(cos_theta, -1.0, 1.0))
            
    degree = int(180 / np.pi) * theta

    return int(degree)

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
    avg_angle = (angle_l + angle_r) / 2
    # avg_angle = np.interp(angle_r, (20, 60), (0, 100))
    print("angle2: ", avg_angle)
    
    return avg_angle


def are_knees_bending(kps: np.ndarray)->bool:
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

    # right_leg_angle = get_bending_angle(right_hip, right_knee, right_ankle)
    # left_leg_angle = get_bending_angle(left_hip, left_knee, left_ankle)
    # right_leg_angle = estimate_pose_angle(right_hip, right_knee, right_ankle)
    # left_leg_angle = estimate_pose_angle(left_hip, left_knee, left_ankle)
    right_leg_angle = find_angle(right_hip, np.array([right_knee[0], 0, 0]), right_knee)
    left_leg_angle = find_angle(left_hip,  np.array([left_knee[0], 0, 0]), left_knee)
    # print(right_leg_angle, left_leg_angle)
    avg_angle = (left_leg_angle + right_leg_angle) / 2
    # print("avg_angle: ", avg_angle)
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
    right_knee = kps[14]
    right_ankle = kps[16]
    left_knee = kps[13]
    left_ankle = kps[15]

    ankles_width = dist([right_ankle], [left_ankle])[0][0]
    #ankles_width = dist([kps[11]], [kps[12]])[0][0]
    knees_width = dist([right_knee], [left_knee])[0][0]
    # print(ankles_width, knees_width)
    margin = 0.15 * ankles_width
    # print("margin: ", margin)
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
    right_shoulder = kps[6]
    right_elbow = kps[8]
    right_wrist = kps[10]

    left_shoulder = kps[5]
    left_elbow = kps[7]
    left_wrist = kps[9]

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
    right_ankle = kps[16]
    left_ankle = kps[15]
    right_shoulder = kps[6]
    left_shoulder = kps[5]

    ankles_width = dist([right_ankle], [left_ankle])[0][0]
    shoulders_width = dist([right_shoulder], [left_shoulder])[0][0]
    margin = 0.7 * shoulders_width
    return shoulders_width - margin < ankles_width < shoulders_width + margin
    
def is_in_right_direction(kps: np.ndarray)->bool:
    # Cropped Image
    if waist_x1 > shoulder_x1:
        return False
    
    return True

def counts_calculate_front_squat(kps: np.ndarray, count: int, dirr: int):
    print(f"counts_calculate: {dirr} {count}")
    angle = get_angle(kps)
    per = np.interp(angle, (85, 160), (0, 100))
    if per == 100:
        if dirr == 0:
            # count += 0.5
            dirr = 1
    # полное выполнение упражнения
    if per == 0:
        if dirr == 1:
            count += 1
            dirr = 0

    return [count, dirr]

def counts_calculate_front_squat_incorrect(kps: np.ndarray, incorrect_count: int, incorrect_dirr: int):
    print(f"counts_calculate: {incorrect_dirr} {incorrect_count}")
    angle = get_angle(kps)
    per = np.interp(angle, (85, 160), (0, 100))
    if per == 100:
        if incorrect_dirr == 0:
            # count += 0.5
            incorrect_dirr = 1
    # полное выполнение упражнения
    if per == 0:
        if incorrect_dirr == 1:
            incorrect_count += 1
            incorrect_dirr = 0

    return [incorrect_count, incorrect_dirr]
# def counts_calculate_front_squat(kps: np.ndarray, count_correct: int, count_attempts: int, dirr: int):
#     print(f"counts_calculate: {dirr} {count_correct} {count_attempts}")
#     angle = get_angle(kps)
#     per = np.interp(angle, (85, 160), (0, 100))
#     feedback_flag = False
    
#     if per == 100:
#         if dirr == 0:
#             dirr = 1
#     # полное выполнение упражнения
#     if per == 0:
#         if dirr == 1:
#             count_correct += 1
#             dirr = 0
#     else:
#         count_attempts += 1
#         feedback_flag = True

#     return count_correct, count_attempts, dirr, feedback_flag

def give_feedback_front_squat(kps: np.ndarray) -> Tuple[Dict, List, List]:
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
        count (int): current count of completed squats.
        dirr (int): direction flag for squat completion.

    Returns:
        feedback (Dict): feedback on the person's front squat technique.
        possible_corrections (List): possible corrections to the person's front squat technique.
        count (int): updated count of completed squats.
        dirr (int): updated direction flag for squat completion.
    """

    feedback = {'is_in_position': False}
    feedback_flag = False
    possible_corrections = ['knee_bend', 'feet_position', 'elbow_position', 'knee_position']
    if is_in_start_position(kps):
        feedback['is_in_position'] = True
        if not are_feet_well_positioned(kps):
            feedback['feet_position'] = "Feet should be at shoulder width!!!"
            feedback_flag = True
            
        if are_elbows_down(kps):
            feedback['elbow_position'] = "Rise your elbows!!!"
            feedback_flag = True
          
        if are_knees_bending(kps):
            if are_knees_caving(kps):
                feedback["knee_position"] = "Open your knees!!!"
                feedback_flag = True
                
    
    pointsofinterest = []
    return (feedback, possible_corrections, pointsofinterest, feedback_flag)

