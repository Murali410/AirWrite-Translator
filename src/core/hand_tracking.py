"""
Hand tracking using MediaPipe Hands.

This wraps the MediaPipe setup that was previously inline in main.py
(`mpHands = mp.solutions.hands`, etc.) and the finger-up gesture check
(`lmList[8][1] < lmList[6][1]`) that the original script used to decide
whether the user is "drawing" in the air.
"""

import cv2
import mediapipe as mp

from src.utils import config


class HandTracker:
    """Detects a single hand per frame and exposes its landmark positions."""

    # Landmark indices used by the original implementation
    INDEX_FINGER_TIP = 8
    INDEX_FINGER_PIP = 6

    def __init__(
        self,
        max_num_hands: int = config.MAX_NUM_HANDS,
        min_detection_confidence: float = config.MIN_DETECTION_CONFIDENCE,
    ):
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
        )
        self._mp_draw = mp.solutions.drawing_utils

    def process(self, frame_rgb):
        """Run hand detection on an RGB frame.

        Returns the raw MediaPipe result (`multi_hand_landmarks` etc.),
        exactly as `hands.process(...)` did in the original script.
        """
        return self._hands.process(frame_rgb)

    def landmark_pixel_coords(self, hand_landmarks, frame_width, frame_height):
        """Convert normalized landmarks to pixel coordinates (x, y)."""
        return [
            (int(lm.x * frame_width), int(lm.y * frame_height))
            for lm in hand_landmarks.landmark
        ]

    def draw_landmarks(self, frame, hand_landmarks):
        """Draw the hand skeleton on the frame, as the original did."""
        self._mp_draw.draw_landmarks(frame, hand_landmarks, self._mp_hands.HAND_CONNECTIONS)

    def is_drawing_gesture(self, landmark_points):
        """True when the index finger is raised (the original's drawing trigger).

        Mirrors the original condition exactly:
            drawing_enabled = lmList[8][1] < lmList[6][1]
        """
        tip_y = landmark_points[self.INDEX_FINGER_TIP][1]
        pip_y = landmark_points[self.INDEX_FINGER_PIP][1]
        return tip_y < pip_y

    def fingertip_position(self, landmark_points):
        """Pixel position of the index fingertip (landmark 8)."""
        return landmark_points[self.INDEX_FINGER_TIP]
