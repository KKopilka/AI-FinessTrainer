"""Root module for ai_trainer."""
from . import utils
from . import models
from . import drawing
from . import properties
# from . import plotting
from . import feedback
from .constants import (
    COCO_COLORS_CV2,
    COCO_COLORS_PLT,
    COCO_CONNECTIONS,
    COCO_KEYPOINTS,
    MEDIAPIPE_COLORS_CV2,
    MEDIAPIPE_COLORS_PLT,
    MEDIAPIPE_CONNECTIONS,
    MEDIAPIPE_KEYPOINTS,
    KeypointsNames,
    PoseColorsCV2,
    PoseColorsPLT,
    PoseDispositions,
    connections_to_indexes,
)

__all__ = [
    "utils",
    "models",
    "drawing",
    "plotting",
    "feedback",
]
