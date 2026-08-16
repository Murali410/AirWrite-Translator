"""
Small persistence helpers used after each recognition pass.

Extracted from the end of the original `preprocess_and_run_ocr`, which
saved the processed canvas image and appended a line to a CSV log.
"""

import time

import cv2

from src.utils import config


def save_recognition_result(processed_image, recognized_text: str, translated_text: str):
    """Save the processed canvas as a timestamped PNG and log the result.

    Writes `canvas_<timestamp>.png` and appends a row to
    `recognized_log.csv`, exactly as the original script did.
    """
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"canvas_{timestamp}.png"
    cv2.imwrite(filename, processed_image)

    with open(config.RECOGNITION_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp},{recognized_text},{translated_text}\n")
