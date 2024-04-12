"""
Store the keypoints names and connections for each disposition.

There are multiple pose dispositions, each with its own keypoints names and
connections. This module stores the keypoints names and connections for each
disposition: MediaPipe, and COCO are the dispositions supported.
"""
from typing import Iterable, Tuple

__all__ = [
    "connections_to_indexes",
    "PoseDispositions",
    "PoseColorsCV2",
    "PoseColorsPLT",
    "KeypointsNames",
    "MEDIAPIPE_KEYPOINTS",
    "MEDIAPIPE_CONNECTIONS",
    "MEDIAPIPE_COLORS_CV2",
    "MEDIAPIPE_COLORS_PLT",
    "COCO_KEYPOINTS",
    "COCO_CONNECTIONS",
    "COCO_COLORS_CV2",
    "COCO_COLORS_PLT",
]


def connections_to_indexes(
    connections: Iterable[Tuple[str, str]],
    keypoints_names: Iterable[str],
) -> Iterable[Tuple[int, int]]:
    """
    Converts connections of strings to connections of indexes.

    Args:
        connections (Iterable[Tuple[str, str]]): list of connection names.
        keypoints_names (Iterable[str]): list of keypoints names.

    Returns:
        List[Tuple[int, int]]: list of connection indexes
    """
    return [
        (keypoints_names.index(connection[0]), keypoints_names.index(connection[1]))
        for connection in connections
    ]


class PoseDispositions:
    """
    Pose dispositions.
    """

    MEDIAPIPE = "mediapipe"
    COCO = "coco"
    MPII = "mpii"
    H36M = "h36m"
    THETHIS = "thethis"


class PoseColorsPLT:
    """
    Store colors for each connection in matplotlib format.
    """

    LEFT = "orange"
    RIGHT = "cyan"
    NEUTRAL = "lightgray"


class PoseColorsCV2:
    """
    Store colors for each connection in cv2 format.
    """

    LEFT = (255, 165, 0)
    RIGHT = (64, 224, 208)
    NEUTRAL = (220, 220, 220)


class KeypointsNames:
    """
    Keypoints names for each disposition.
    """

    HEAD = "head"
    NOSE = "nose"
    NECK = "neck"
    LEFT_EYE = "left_eye"
    LEFT_EYE_INNER = "left_eye_inner"
    LEFT_EYE_OUTER = "left_eye_outer"
    RIGHT_EYE = "right_eye"
    RIGHT_EYE_INNER = "right_eye_inner"
    RIGHT_EYE_OUTER = "right_eye_outer"
    LEFT_EAR = "left_ear"
    RIGHT_EAR = "right_ear"
    MOUTH_LEFT = "mouth_left"
    MOUTH_RIGHT = "mouth_right"
    LEFT_SHOULDER = "left_shoulder"
    RIGHT_SHOULDER = "right_shoulder"
    LEFT_ELBOW = "left_elbow"
    RIGHT_ELBOW = "right_elbow"
    LEFT_WRIST = "left_wrist"
    RIGHT_WRIST = "right_wrist"
    LEFT_PINKY = "left_pinky"
    RIGHT_PINKY = "right_pinky"
    LEFT_INDEX = "left_index"
    RIGHT_INDEX = "right_index"
    LEFT_THUMB = "left_thumb"
    RIGHT_THUMB = "right_thumb"
    THORAX = "thorax"
    PELVIS = "pelvis"
    LEFT_HIP = "left_hip"
    RIGHT_HIP = "right_hip"
    LEFT_KNEE = "left_knee"
    RIGHT_KNEE = "right_knee"
    LEFT_ANKLE = "left_ankle"
    RIGHT_ANKLE = "right_ankle"
    LEFT_HEEL = "left_heel"
    RIGHT_HEEL = "right_heel"
    LEFT_TIPTOE = "left_tiptoe"
    RIGHT_TIPTOE = "right_tiptoe"


MEDIAPIPE_KEYPOINTS = (
    KeypointsNames.NOSE,
    KeypointsNames.LEFT_EYE_INNER,
    KeypointsNames.LEFT_EYE,
    KeypointsNames.LEFT_EYE_OUTER,
    KeypointsNames.RIGHT_EYE_INNER,
    KeypointsNames.RIGHT_EYE,
    KeypointsNames.RIGHT_EYE_OUTER,
    KeypointsNames.LEFT_EAR,
    KeypointsNames.RIGHT_EAR,
    KeypointsNames.MOUTH_LEFT,
    KeypointsNames.MOUTH_RIGHT,
    KeypointsNames.LEFT_SHOULDER,
    KeypointsNames.RIGHT_SHOULDER,
    KeypointsNames.LEFT_ELBOW,
    KeypointsNames.RIGHT_ELBOW,
    KeypointsNames.LEFT_WRIST,
    KeypointsNames.RIGHT_WRIST,
    KeypointsNames.LEFT_PINKY,
    KeypointsNames.RIGHT_PINKY,
    KeypointsNames.LEFT_INDEX,
    KeypointsNames.RIGHT_INDEX,
    KeypointsNames.LEFT_THUMB,
    KeypointsNames.RIGHT_THUMB,
    KeypointsNames.LEFT_HIP,
    KeypointsNames.RIGHT_HIP,
    KeypointsNames.LEFT_KNEE,
    KeypointsNames.RIGHT_KNEE,
    KeypointsNames.LEFT_ANKLE,
    KeypointsNames.RIGHT_ANKLE,
    KeypointsNames.LEFT_HEEL,
    KeypointsNames.RIGHT_HEEL,
    KeypointsNames.LEFT_TIPTOE,
    KeypointsNames.RIGHT_TIPTOE,
)


MEDIAPIPE_CONNECTIONS = (
    (KeypointsNames.NOSE, KeypointsNames.LEFT_EYE),
    (KeypointsNames.LEFT_EYE, KeypointsNames.LEFT_EAR),
    (KeypointsNames.NOSE, KeypointsNames.RIGHT_EYE),
    (KeypointsNames.RIGHT_EYE, KeypointsNames.RIGHT_EAR),
    (KeypointsNames.MOUTH_LEFT, KeypointsNames.MOUTH_RIGHT),
    (KeypointsNames.LEFT_SHOULDER, KeypointsNames.RIGHT_SHOULDER),
    (KeypointsNames.LEFT_HIP, KeypointsNames.RIGHT_HIP),
    (KeypointsNames.LEFT_SHOULDER, KeypointsNames.LEFT_HIP),
    (KeypointsNames.LEFT_SHOULDER, KeypointsNames.LEFT_ELBOW),
    (KeypointsNames.LEFT_ELBOW, KeypointsNames.LEFT_WRIST),
    (KeypointsNames.LEFT_WRIST, KeypointsNames.LEFT_PINKY),
    (KeypointsNames.LEFT_WRIST, KeypointsNames.LEFT_INDEX),
    (KeypointsNames.LEFT_WRIST, KeypointsNames.LEFT_THUMB),
    (KeypointsNames.LEFT_INDEX, KeypointsNames.LEFT_PINKY),
    (KeypointsNames.RIGHT_SHOULDER, KeypointsNames.RIGHT_HIP),
    (KeypointsNames.RIGHT_SHOULDER, KeypointsNames.RIGHT_ELBOW),
    (KeypointsNames.RIGHT_ELBOW, KeypointsNames.RIGHT_WRIST),
    (KeypointsNames.RIGHT_WRIST, KeypointsNames.RIGHT_PINKY),
    (KeypointsNames.RIGHT_WRIST, KeypointsNames.RIGHT_INDEX),
    (KeypointsNames.RIGHT_WRIST, KeypointsNames.RIGHT_THUMB),
    (KeypointsNames.RIGHT_INDEX, KeypointsNames.RIGHT_PINKY),
    (KeypointsNames.LEFT_HIP, KeypointsNames.LEFT_KNEE),
    (KeypointsNames.LEFT_KNEE, KeypointsNames.LEFT_ANKLE),
    (KeypointsNames.LEFT_ANKLE, KeypointsNames.LEFT_HEEL),
    (KeypointsNames.LEFT_ANKLE, KeypointsNames.LEFT_TIPTOE),
    (KeypointsNames.LEFT_HEEL, KeypointsNames.LEFT_TIPTOE),
    (KeypointsNames.RIGHT_HIP, KeypointsNames.RIGHT_KNEE),
    (KeypointsNames.RIGHT_KNEE, KeypointsNames.RIGHT_ANKLE),
    (KeypointsNames.RIGHT_ANKLE, KeypointsNames.RIGHT_HEEL),
    (KeypointsNames.RIGHT_ANKLE, KeypointsNames.RIGHT_TIPTOE),
    (KeypointsNames.RIGHT_HEEL, KeypointsNames.RIGHT_TIPTOE),
)


MEDIAPIPE_COLORS_CV2 = (
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.NEUTRAL,  # mouth
    PoseColorsCV2.NEUTRAL,  # shoulders
    PoseColorsCV2.NEUTRAL,  # hips
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
)


MEDIAPIPE_COLORS_PLT = (
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.NEUTRAL,  # mouth
    PoseColorsPLT.NEUTRAL,  # shoulders
    PoseColorsPLT.NEUTRAL,  # hips
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
)


COCO_KEYPOINTS = (
    KeypointsNames.NOSE,
    KeypointsNames.LEFT_EYE,
    KeypointsNames.RIGHT_EYE,
    KeypointsNames.LEFT_EAR,
    KeypointsNames.RIGHT_EAR,
    KeypointsNames.LEFT_SHOULDER,
    KeypointsNames.RIGHT_SHOULDER,
    KeypointsNames.LEFT_ELBOW,
    KeypointsNames.RIGHT_ELBOW,
    KeypointsNames.LEFT_WRIST,
    KeypointsNames.RIGHT_WRIST,
    KeypointsNames.LEFT_HIP,
    KeypointsNames.RIGHT_HIP,
    KeypointsNames.LEFT_KNEE,
    KeypointsNames.RIGHT_KNEE,
    KeypointsNames.LEFT_ANKLE,
    KeypointsNames.RIGHT_ANKLE,
)


COCO_CONNECTIONS = (
    (KeypointsNames.NOSE, KeypointsNames.LEFT_EYE),
    (KeypointsNames.LEFT_EYE, KeypointsNames.LEFT_EAR),
    (KeypointsNames.NOSE, KeypointsNames.RIGHT_EYE),
    (KeypointsNames.RIGHT_EYE, KeypointsNames.RIGHT_EAR),
    (KeypointsNames.LEFT_SHOULDER, KeypointsNames.RIGHT_SHOULDER),
    (KeypointsNames.LEFT_SHOULDER, KeypointsNames.LEFT_ELBOW),
    (KeypointsNames.LEFT_ELBOW, KeypointsNames.LEFT_WRIST),
    (KeypointsNames.RIGHT_SHOULDER, KeypointsNames.RIGHT_ELBOW),
    (KeypointsNames.RIGHT_ELBOW, KeypointsNames.RIGHT_WRIST),
    (KeypointsNames.LEFT_HIP, KeypointsNames.RIGHT_HIP),
    (KeypointsNames.LEFT_HIP, KeypointsNames.LEFT_SHOULDER),
    (KeypointsNames.RIGHT_HIP, KeypointsNames.RIGHT_SHOULDER),
    (KeypointsNames.LEFT_HIP, KeypointsNames.LEFT_KNEE),
    (KeypointsNames.LEFT_KNEE, KeypointsNames.LEFT_ANKLE),
    (KeypointsNames.RIGHT_HIP, KeypointsNames.RIGHT_KNEE),
    (KeypointsNames.RIGHT_KNEE, KeypointsNames.RIGHT_ANKLE),
)


COCO_COLORS_CV2 = (
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.NEUTRAL,  # shoulders
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.NEUTRAL,  # hips
    PoseColorsCV2.LEFT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.LEFT,
    PoseColorsCV2.RIGHT,
    PoseColorsCV2.RIGHT,
)


COCO_COLORS_PLT = (
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.NEUTRAL,  # shoulders
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.NEUTRAL,  # hips
    PoseColorsPLT.LEFT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.LEFT,
    PoseColorsPLT.RIGHT,
    PoseColorsPLT.RIGHT,
)
