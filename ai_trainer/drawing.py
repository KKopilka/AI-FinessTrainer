"""Utils used to draw pose estimation data on images."""

from typing import List, Optional, Tuple

import cv2
import numpy as np

from . import constants

__all__ = [
    "draw_circle",
    "draw_circle_with_border",
    "draw_rectangle",
    "draw_text",
    "draw_text_with_background",
    "draw_text_with_border",
    "draw_pose",
]


def draw_text(
    image: np.ndarray,
    text: str,
    origin: Tuple[int, int],
    color=(255, 0, 0),
    thickness: int = 1,
    font_scale: float = 0.5,
    font_face: str = cv2.FONT_HERSHEY_SIMPLEX,
) -> np.ndarray:
    """
    Write a text over an image.

    Args:
        image (np.ndarray): image to write on
        text (str): text to write
        origin (Tuple[int, int]): location where text will be added
        color (tuple, optional): text color. Defaults to (255, 0, 0).
        thickness (int, optional): text thickness. Defaults to 1.
        font_scale (float, optional): text size. Defaults to 0.5.
        font_face (str, optional): texxt font. Defaults to cv2.FONT_HERSHEY_SIMPLEX.

    Returns:
        np.ndarray: image with text written on it
    """
    x, y = origin  # pylint: disable=invalid-name
    return cv2.putText(
        img=image,
        text=text,
        org=(int(x), int(y)),  # force ints to opencv
        fontFace=font_face,
        fontScale=font_scale,
        color=color,
        thickness=thickness,
    )


def draw_text_with_border(
    image: np.ndarray,
    text: str,
    origin: Tuple[int, int],
    font_scale: float = 0.5,
    font_face: str = cv2.FONT_HERSHEY_SIMPLEX,
    color_in: Tuple[int, int, int] = (255, 255, 255),
    thickness_in: int = 1,
    color_out: Tuple[int, int, int] = (0, 0, 0),
    thickness_out: int = 3,
) -> np.ndarray:
    """
    Draw a text with a border around the letters.

    Default is white text with black borders so it improves readability.

    Args:
        image (np.ndarray): image to write on
        text (str): text to write
        origin (Tuple[int, int]): location where text will be added
        font_scale (float, optional): text size. Defaults to 0.5.
        font_face (str, optional): texxt font. Defaults to cv2.FONT_HERSHEY_SIMPLEX.
        color_in (Tuple[int, int, int], optional): color of the inner
            part of the letters. Defaults to (255, 255, 255).
        thickness_in (int, optional): thickness of the inner part of the letters.
            Defaults to 1.
        color_out (Tuple[int, int, int], optional): color of the border of the letters.
            Defaults to (0, 0, 0).
        thickness_out (int, optional): thickness of the border. Defaults to 3.

    Returns:
        np.ndarray: image with text written on it
    """
    for thickness, color in zip([thickness_out, thickness_in], [color_out, color_in]):
        image = draw_text(
            image=image,
            text=text,
            origin=origin,
            color=color,
            thickness=thickness,
            font_face=font_face,
            font_scale=font_scale,
        )

    return image


def draw_circle(
    image: np.ndarray,
    origin: Tuple[int, int],
    radius: int = 2,
    color: Tuple[int, int, int] = (0, 0, 0),
    thickness: int = 2,
) -> np.ndarray:
    """
    Draw a circle on the given position.

    Args:
        image (np.ndarray): Image to draw the circle on.
        origin (Tuple[int, int]): Position in pixels of circle center.
        radius (int, optional): Size of the circle. Defaults to 2.
        color (Tuple[int, int, int], optional): Color of the circle.
            Defaults to (0, 0, 0).
        thickness (int, optional): Thickness of the line conforming the circle.
            Defaults to 2.

    Returns:
        np.ndarray: Image with the circle drawn on it.
    """
    return cv2.circle(
        image,
        origin,
        radius=radius,
        color=color,
        thickness=thickness,
    )


def draw_circle_with_border(
    image: np.ndarray,
    origin: Tuple[int, int],
    radius: int = 2,
    color_in: Tuple[int, int, int] = (255, 255, 255),
    color_out: Tuple[int, int, int] = (0, 0, 0),
    thickness: int = 2,
) -> np.ndarray:
    """
    Draw a circle with border on the given position.

    Args:
        image (np.ndarray): Image to draw the circle on.
        origin (Tuple[int, int]): Position in pixels of the circle center.
        radius (int, optional): Size of the circle. Defaults to 2.
        color_in (Tuple[int, int, int], optional): Color of the circle.
            Defaults to (255, 255, 255).
        color_out (Tuple[int, int, int], optional): Color of the circle.
            Defaults to (0, 0, 0).
        thickness (int, optional): Thickness of the line conforming the circle.
            Defaults to 2.

    Returns:
        np.ndarray: Image with the circle drawn on it.
    """
    radius_in = radius
    radius_out = radius_in + thickness
    for rad, color in zip([radius_out, radius_in], [color_out, color_in]):
        image = draw_circle(
            image,
            origin,
            radius=rad,
            color=color,
            thickness=thickness,
        )

    return image


def draw_rectangle(
    image: np.ndarray,
    origin: Tuple[int, int],
    width: int,
    height: int,
    color: Tuple[int, int, int] = (0, 0, 0),
    thickness: int = 3,
) -> np.ndarray:
    """
    Draw a rectangle over an RGB image.

    Args:
        image (np.ndarray): image array.
        origin (Tuple[int, int]): upper-left corner in pixel coordinates (x,y)
        width (int): pixel width of the rectangle.
        height (int): pixel height of the rectangle.
        color (Tuple[int, int, int]): color of the rectangle in (R, G, B) from [0-255]
        thickness (int, optional): rectangle thickness. Defaults to 3.

    Returns:
        np.ndarray: image with a rectangle drawn on it.
    """
    x1, y1 = origin  # pylint: disable=invalid-name
    x2, y2 = x1 + width, y1 + height  # pylint: disable=invalid-name
    image = cv2.rectangle(
        img=image,
        pt1=(int(x1), int(y1)),  # force ints to opencv
        pt2=(int(x2), int(y2)),  # force ints to opencv
        color=color,
        thickness=thickness,
    )
    return image


def draw_text_with_background(
    image: np.ndarray,
    text: str,
    origin: Tuple[int, int],
    text_color: Tuple[int, int, int] = (255, 255, 255),
    background_color: Tuple[int, int, int] = (0, 0, 0),
    font_scale: float = 0.5,
    font_thickness: int = 1,
    font_face: str = cv2.FONT_HERSHEY_SIMPLEX,
) -> np.ndarray:
    """
    Draw text with background over an RGB image.

    Args:
        image (np.ndarray): image array to draw text on.
        text (str): text to write on image
        origin (Tuple[int, int]): bottom left where text starts.
        text_color (Tuple[int, int, int], optional): text color.
            Defaults to (255, 255, 255).
        background_color (Tuple[int, int, int], optional): background color.
            Defaults to (0, 0, 0).
        font_scale (float, optional): text size. Defaults to 0.5.
        font_thickness (int, optional): text thickness in pixels. Defaults to 3.
        font_face (str, optional): text font. Defaults to cv2.FONT_HERSHEY_SIMPLEX.

    Returns:
        np.ndarray: image with text over background drawn on it.
    """
    # how many pixels do this text occupy
    text_size, _ = cv2.getTextSize(
        text=text,
        fontFace=font_face,
        fontScale=font_scale,
        thickness=font_thickness,
    )
    text_width, text_height = text_size

    # rectangle starts at upper-left corner
    x, y = origin  # pylint: disable=invalid-name
    rectangle_origin = x, y - text_height

    # draw background
    image = draw_rectangle(
        image=image,
        origin=rectangle_origin,
        width=text_width,
        height=text_height,
        color=background_color,
        thickness=-1,  # fill rectangle
    )

    # draw text over background
    image = draw_text(
        image=image,
        text=text,
        color=text_color,
        origin=origin,
        thickness=font_thickness,
        font_scale=font_scale,
    )

    return image


def draw_pose_keypoints(
    image: np.ndarray,
    keypoints: np.ndarray,
    color_in: Tuple[int, int, int] = (255, 255, 255),
    color_out: Tuple[int, int, int] = (0, 0, 0),
    radius: int = 2,
    thickness: int = 3,
) -> np.ndarray:
    """
    Draw circles with borders on pose landmarks.

    Args:
        image (np.ndarray): image to paint poses on.
        keypoints (np.ndarray): pose estimation landmarks
            in pixel coordinates with shape (n_joints, n_dims).
        color_in (Tuple[int, int, int], optional): color of the inner
            part of the joint. Defaults to (255, 255, 255).
        color_out (Tuple[int, int, int], optional): color of the border
            of the joint. Defaults to (0, 0, 0).
        radius (int, optional): Radius of the keypoint. Defaults to 2.
        thickness (int, optional): thickness of the keypoint.
            Defaults to 3.

    Returns:
        np.ndarray: Image with pose joints drawn on it
    """
    # draw keypoints
    for point in keypoints:
        x, y = point[:2].astype(np.int16)  # pylint: disable=invalid-name

        image = draw_circle_with_border(
            image=image,
            origin=(x, y),
            radius=radius,
            color_in=color_in,
            color_out=color_out,
            thickness=thickness,
        )

    return image


def draw_pose_connections(
    image: np.ndarray,
    keypoints: np.ndarray,
    connections: List[Tuple[int, int]],
    colors: Optional[List[Tuple[int, int, int]]] = None,
    thickness: int = 3,
) -> np.ndarray:
    """
    Draws connections betoween pose keypoints over an image.

    If colors parameter is given, its length must be equal to the length of
    the keypoints.

    Args:
        image (np.ndarray): image to paint poses on
        keypoints (np.ndarray): pose estimation landmarks
            in pixel coordinates with shape (n_joints, n_dims).
        connections (List[Tuple[int, int]]): List of pairs of keypoints indexes
            (N, 2) to plot lines in between both points.
        colors (Optional[List[Tuple[int, int, int]]], optional): Plot connection
            lines with the given color. Defaults to (0,0,0).
        thickness (int, optional): skeleton lines thickness. Defaults to 3.


    Raises:
        ValueError: if len(colors) != len(connections)

    Returns:
        np.ndarray: Image with pose connections drawn on it
    """
    # if no color given draw all connections on black
    if colors is None:
        colors = [(0, 0, 0) for _ in range(len(connections))]

    # check every connection has its own color
    # if len(connections) != len(colors):
    #     raise ValueError(
    #         f"Every connection len=={len(connections)} " f"must have its color len=={len(colors)}"
    #     )

    # plot skeleton connections
    for connection, color in zip(connections, colors):
        # points forming connection
        pt1, pt2 = keypoints[list(connection)].astype(np.int16)

        # ignore not visible points
        if not pt1.any() or not pt2.any():
            continue

        image = cv2.line(
            image,
            pt1[:2],
            pt2[:2],
            color=color,
            thickness=thickness,
        )

    return image


def draw_pose_keypoints_and_connections(
    image: np.ndarray,
    keypoints: np.ndarray,
    connections: List[Tuple[int, int]],
    thickness: int = 3,
    connections_colors: Optional[List[Tuple[int, int, int]]] = None,
    keypoint_inner_color: Tuple[int, int, int] = (255, 255, 255),
    keypoint_outer_color: Tuple[int, int, int] = (0, 0, 0),
    keypoint_radius: int = 2,
) -> np.ndarray:
    """
    Draw pose connections and keypoints over an image.

    Keypoints are drawn as a circle with border so they are easily visible.
    Any keypoint with value (0, 0) won't be plotted as it means it has not been
    recogniced by the model.

    Args:
        image (np.ndarray): image to paint the pose on.
        keypoints (np.ndarray): pose estimation landmarks
            in pixel coordinates with shape (n_joints, n_dims).
        connections (List[Tuple[int, int]]): List of pairs of keypoints indexes
            (N, 2) to plot lines in between both points.
        thickness (int, optional): pose connections and keypoints thickness.
            Defaults to 3.
        connections_colors (Optional[List[Tuple[int, int, int]]], optional): Plot
            connection lines with the given color. Defaults to None.
        keypoint_inner_color (Tuple[int, int, int], optional): color of the inner
            part of the joint. Defaults to (255, 255, 255).
        keypoint_outer_color (Tuple[int, int, int], optional): color of the border
            of the joint. Defaults to (0, 0, 0).
        keypoint_radius (int, optional): Keypoint radius. Defaults to 2.

    Returns:
        np.ndarray: image with pose connections and keypoints plotted over it.
    """
    # plot skeleton lines between keypoints
    image = draw_pose_connections(
        image=image,
        keypoints=keypoints,
        connections=connections,
        colors=connections_colors,
        thickness=thickness,
    )

    # plot skeleton joints
    image = draw_pose_keypoints(
        image=image,
        keypoints=keypoints,
        color_in=keypoint_inner_color,
        color_out=keypoint_outer_color,
        radius=keypoint_radius,
        thickness=thickness,
    )

    return image


def draw_pose(
    image: np.ndarray,
    keypoints: np.ndarray,
    disposition: str,
    color: Optional[Tuple[int, int, int]] = None,
    thickness: int = 3,
) -> np.ndarray:
    """
    Draws pose over image following dataset disposition.

    Allowed dispositions are: "mediapipe"

    Args:
        image (np.ndarray): image to draw on
        keypoints (np.ndarray): pose estimation landmarks
            in pixel (x, y) coordinates with shape (n_joints, n_dims).
        disposition (str): dataset keypoint positioning.
        color (Optional[Tuple[int, int, int]], optional): color to plot pose.
            Defaults to None.
        thickness (int, optional): pose connections and keypoints thickness.

    Raises:
        ValueError: If given disposition is not found one
            the allowed dispositions. Read function description.

    Returns:
        np.ndarray: image with pose plotted on it
    """
    if disposition == constants.PoseDispositions.MEDIAPIPE:
        connections = constants.MEDIAPIPE_CONNECTIONS
        keypoints_names = constants.MEDIAPIPE_KEYPOINTS
        connections_colors = constants.MEDIAPIPE_COLORS_CV2

    elif disposition == constants.PoseDispositions.COCO:
        connections = constants.COCO_CONNECTIONS
        keypoints_names = constants.COCO_KEYPOINTS
        connections_colors = constants.COCO_COLORS_CV2

    else:
        allowed_dispositions = [
            constants.PoseDispositions.MEDIAPIPE,
            constants.PoseDispositions.COCO,
        ]
        raise ValueError(
            (
                f"Keypoints disposition '{disposition}' not found in "
                f"allowed dispositions: {allowed_dispositions}"
            )
        )

    # convert connections from str:str to int:int
    connections_indexes = constants.connections_to_indexes(
        connections=connections,
        keypoints_names=keypoints_names,
    )

    # if color is given paint all connections with the same color
    if color:
        connections_colors = [color for _ in range(len(connections))]

    return draw_pose_keypoints_and_connections(
        image=image,
        keypoints=keypoints,
        connections=connections_indexes,
        connections_colors=connections_colors,
        thickness=thickness,
        keypoint_radius=thickness // 2,
    )

def draw_dotted_line(frame, lm_coord, start, end, line_color):
    pix_step = 0

    for i in range(start, end+1, 8):
        cv2.circle(frame, (lm_coord[0], i+pix_step), 2, line_color, -1, lineType=cv2.LINE_AA)   