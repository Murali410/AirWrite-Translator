"""
Handwriting recognition using a fine-tuned TrOCR model.

This is a direct extraction of the model loading and
`preprocess_and_run_ocr` logic from the original main.py.
"""

import warnings

import cv2
import numpy as np
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

from src.utils import config

warnings.filterwarnings("ignore", category=UserWarning)


class HandwritingRecognizer:
    """Loads the fine-tuned TrOCR model and recognizes text from a canvas image."""

    def __init__(self, model_path: str = config.MODEL_PATH):
        self.processor = TrOCRProcessor.from_pretrained(model_path)
        self.model = VisionEncoderDecoderModel.from_pretrained(model_path)
        self.model.config.decoder_start_token_id = self.processor.tokenizer.bos_token_id

    @staticmethod
    def enhance_image(canvas):
        """Threshold, dilate, and pad the canvas to improve OCR accuracy.

        Identical steps to the original `enhance_image` function.
        """
        gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        padded = cv2.copyMakeBorder(dilated, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
        return padded

    def recognize(self, canvas, min_nonzero_pixels: int = config.MIN_NONZERO_PIXELS_FOR_OCR):
        """Run OCR on a canvas image.

        Returns a tuple `(recognized_text, processed_image)`. If the canvas
        looks empty (fewer than `min_nonzero_pixels` non-zero pixels after
        enhancement), returns "No handwriting detected" without running the
        model, matching the original behavior.
        """
        padded = self.enhance_image(canvas)
        nonzero = np.count_nonzero(padded)
        print("Canvas shape:", padded.shape)
        print("Non-zero pixels:", nonzero)

        if nonzero < min_nonzero_pixels:
            return "No handwriting detected", padded

        image = Image.fromarray(cv2.cvtColor(padded, cv2.COLOR_GRAY2RGB))
        pixel_values = self.processor(images=image, return_tensors="pt").pixel_values
        generated_ids = self.model.generate(pixel_values, max_length=64)
        recognized_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print("Recognized text:", recognized_text)

        return recognized_text, padded
