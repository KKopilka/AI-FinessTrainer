"""Utility file.

It includes:
- canceling the keypoint overlay effect.
- normalize input image values to a specified range.
- resize an image to a specified size. 
"""
import numpy as np
import cv2
from typing import Any, Iterable, Optional, Tuple

def unpad_points(keypoints: np.ndarray, original_image_size: Tuple[int, int]) -> np.ndarray:
    """Undo the effect of padding applied to keypoints.

    Args:
        keypoints (np.ndarray): Keypoints array in the format (N, 5) where N is the number of keypoints
                                and each keypoint has 5 elements (x, y, z, probability, visibility).
        original_image_size (Tuple[int, int]): Size of the original image in the format (height, width).

    Returns:
        np.ndarray: Unpadded keypoints array.
    """
    # Extract height and width of the original image
    original_height, original_width = original_image_size

    # Perform unpadding
    keypoints[..., 0] *= original_width  # x-coordinate
    keypoints[..., 1] *= original_height  # y-coordinate

    return keypoints

def normalize(image: np.ndarray, floor: float, ceil: float) -> np.ndarray:
    """Normalize the input image values to the specified range.

    Args:
        image (np.ndarray): Input image.
        floor (float): Minimum value after normalization.
        ceil (float): Maximum value after normalization.

    Returns:
        np.ndarray: Normalized image.
    """
    # Ensure the image is in floating point format for accurate normalization
    image = image.astype(np.float32)

    # Normalize the image
    normalized_image = (image - np.min(image)) * (ceil - floor) / (np.max(image) - np.min(image)) + floor

    return normalized_image

def pad_image(image: np.ndarray, target_height: int, target_width: int) -> np.ndarray:
    """Pad image to the specified size.

    Args:
        image (np.ndarray): Input image.
        target_height (int): Target height after padding.
        target_width (int): Target width after padding.

    Returns:
        np.ndarray: Padded image.
    """
    height, width = image.shape[:2]
    pad_height = max(target_height - height, 0)
    pad_width = max(target_width - width, 0)
    padded_image = cv2.copyMakeBorder(
        image, 0, pad_height, 0, pad_width, cv2.BORDER_CONSTANT, value=0
    )

    return padded_image