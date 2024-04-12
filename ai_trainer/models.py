"""Contains the PoseEstimationModel class."""
# pylint: disable=unexpected-keyword-arg
import os
from pathlib import Path
from typing import Any, Iterable, Optional, Tuple

import cv2
import numpy as np
import onnxruntime

from . import utils


class BaseONNXModel:
    """Loads a ONNX model for image processing and runs inference on it."""

    def __init__(
        self,
        model_path: os.PathLike,
        providers: Optional[Iterable[str]] = None,
        provider_options: Optional[Iterable[str]] = None,
        sess_options: Optional[onnxruntime.SessionOptions] = None,
        **kwargs,
    ) -> None:
        """Initialize the ONNX model.

        For more information on the providers, provider options and session
        options, see the ONNX Runtime documentation:
        https://https://onnxruntime.ai/docs/execution-providers/

        Args:
            model_path (os.PathLike): path to the ONNX model.
            providers (Optional[Iterable[str]], optional): list of providers.
                Defaults to None.
            provider_options (Optional[Iterable[str]], optional): list of
                provider options. Defaults to None.
            sess_options (Optional[onnxruntime.SessionOptions], optional):
                session options. Defaults to None.
            **kwargs: additional keyword arguments.
        """
        # check if model file exists
        self.model_path = Path(model_path)  # force to be a Path object
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file {self.model_path} does not exist")

        # Load the ONNX model
        self._session = onnxruntime.InferenceSession(
            model_path,
            providers=providers,
            provider_options=provider_options,
            sess_options=sess_options,
            **kwargs,
        )

        # get model parameters
        self._input_name = self._session.get_inputs()[0].name
        self._output_name = self._session.get_outputs()[0].name
        self.input_shape = self._session.get_inputs()[0].shape
        sorted_shape = np.argsort(self.input_shape)
        width_index = sorted_shape[-2]
        height_index = sorted_shape[-1]
        channels_index = sorted_shape[-3]
        self._channels_index = channels_index
        self.batch_len = self.input_shape[0]
        self.height = self.input_shape[height_index]
        self.width = self.input_shape[width_index]
        tensor_type = self._session.get_inputs()[0].type
        if "tensor(float)" in tensor_type:
            self.tensor_type = np.float32
        elif "tensor(float16)" in tensor_type:
            self.tensor_type = np.float16
        elif "tensor(uint8)" in tensor_type:
            self.tensor_type = np.uint8

    def predict(self, batch: np.ndarray, *args, **kwargs) -> Any:
        """Run inference on the ONNX model with the given image batch.

        Args:
            batch (np.ndarray): batch of image frames, shape should be
                (batch, height, width, channels).
            *args: additional arguments.
            **kwargs: additional keyword arguments.

        Returns:
            Any: the output of the model.
        """
        raise NotImplementedError(
            "method 'predict' must be implemented in a subclass of BaseONNXModel"
        )

    def preprocess_batch(
        self,
        images: Iterable[np.ndarray],
        padding: bool = False,
        normalize: Optional[Tuple[float, float]] = None,
    ) -> np.ndarray:
        """Convert a list of images to a batch.

        Args:
            images (Iterable[np.ndarray]): list of images.
            padding (bool): whether to pad the images to the
                size of the model's input.
            normalize (Optional[Tuple[float, float]]): tuple of
                (floor, ceil) to normalize the image values to.

        Returns:
            np.ndarray: batch of images resized to the expected
                size of the model and the type of the model's input tensor.
        """
        if len(images) != self.batch_len:
            raise ValueError(f"Batch size of the model is {self.batch_len}, but got {len(images)}")

        # resize images to the size of the model input
        processed_images_list = []
        for image in images:
            if padding:
                image = utils.pad_image(image, 300, 300)
            image = cv2.resize(image, (self.width, self.height))
            # print(normalize)
            if normalize:
                image = utils.normalize(image, *normalize)
                # print(utils.normalize(image, *normalize))
            # convert HWC to CHW if needed
            if self._channels_index == 1:
                image = image.transpose(2, 0, 1)
            processed_images_list.append(image)

        # convert list of images to a numpy array batch
        return np.array(processed_images_list, dtype=self.tensor_type)


class BlazePoseModel(BaseONNXModel):
    """Load a Blaze Pose model and runs inference on it.

    BlazePose is a real-time, single-shot single-person pose estimation model
    that detects 33 keypoints and their corresponding visibility scores.
    It is included in the MediaPipe framework.

    Weights and model card can be found here:
    https://google.github.io/mediapipe/solutions/models.html#pose
    """
    def predict(self, batch: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Run inference on the ONNX model with the given image batch.

        Args:
            batch (np.ndarray): batch of image frames, shape should be
                (batch, height, width, channels).

        Returns:
            Tuple[np.ndarray, np.ndarray]: a tuple containing the keypoints in
                    the shape (B,33,5) where B is the batch size, each keypoint has
                    5 elements (x, y, z, probability and visibility).
                    Visibility is in the range of [min_float, max_float] and after
                    user-applied sigmoid denotes the probability that a keypoint is located
                    within the frame and not occluded by another bigger body part or
                    another object. Presence is in the range of [min_float, max_float]
                    and after user-applied sigmoid denotes the probability that a
                    keypoint is located within the frame.

        Raises:
            ValueError: If the shape of the batch does not match the shape
                of the model's input tensor.
        """
        # preprocess frames
        batch_processed = self.preprocess_batch(batch, padding=True, normalize=(0, 1))

        # Perform inference
        keypoints = self._session.run([self._output_name], {self._input_name: batch_processed})
        keypoints = np.array(keypoints, dtype=np.float32)

        # last 6 keypoints are not used
        keypoints = keypoints.reshape(-1, 39, 5)  # (B, 195) to (B, 39, 5)
        keypoints = keypoints[:, :-6, :]  # remove last 6 kps: (B, 39, 5) to (B, 33, 5)

        # normalize keypoints coordinates to [0, 1]
        keypoints[..., 0] /= self.width
        keypoints[..., 1] /= self.height

        # undo padding from keypoint coordinates
        unpad_keypoints = []
        for orig_img, crop_kps in zip(batch, keypoints):
            orig_img_size = orig_img.shape[:2]
            crop_unpad_kps = utils.unpad_points(crop_kps, orig_img_size)
            unpad_keypoints.append(crop_unpad_kps)

        return np.array(unpad_keypoints, dtype=np.float32)
