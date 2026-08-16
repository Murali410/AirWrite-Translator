"""
Display helpers: drawing buttons/overlay text and combining the webcam
feed with the paint canvas into the single window the original script
showed via `cv2.imshow("AirCanvas", combined)`.
"""

import cv2
import numpy as np

from src.utils import config


def draw_buttons(frame):
    """Draw the toolbar buttons onto a frame (webcam view)."""
    for i, (x1, x2) in enumerate(config.BUTTON_COORDS):
        cv2.rectangle(
            frame, (x1, config.BUTTON_TOP), (x2, config.BUTTON_BOTTOM),
            config.BUTTON_COLORS[i], 2,
        )
        cv2.putText(
            frame, config.BUTTON_LABELS[i], (x1 + 9, 33),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2,
        )


def draw_fingertip_marker(frame, position, is_drawing):
    color = (0, 255, 0) if is_drawing else (0, 0, 255)
    cv2.circle(frame, position, 5, color, -1)


def draw_recognition_overlay(frame, canvas, recognized_text, translated_text):
    """Overlay recognized/translated text on both the frame and the canvas."""
    if not recognized_text:
        return

    cv2.putText(
        frame, f"Detected: {recognized_text}", (10, frame.shape[0] - 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2,
    )
    cv2.putText(
        frame, f"Translated: {translated_text}", (10, frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 0), 2,
    )
    cv2.putText(
        canvas, recognized_text, (10, 420),
        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2,
    )
    cv2.putText(
        canvas, translated_text, (10, 450),
        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2,
    )


def combine_views(frame, canvas):
    """Side-by-side combination of the webcam frame and the paint canvas."""
    resized_canvas = cv2.resize(canvas, (frame.shape[1], frame.shape[0]))
    return np.hstack((frame, resized_canvas))
