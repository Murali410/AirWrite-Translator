"""
Central configuration for AirWrite Translator.

All values here were previously hardcoded directly inside the original
single-file main.py. They are collected here so they can be tuned or
overridden (e.g. via environment variables) without touching the
application logic.
"""

import os

# ---------------------------------------------------------------------------
# TrOCR model
# ---------------------------------------------------------------------------
# The original script pointed directly at a fine-tuned model on the
# developer's machine:
#   MODEL_PATH = r"C:\new web\AirCanvas-Finetune\trocr-aircanvas-model"
#
# That path does not exist on other machines, so it is now read from the
# AIRWRITE_MODEL_PATH environment variable, falling back to the original
# value so behavior on the original machine is unchanged.
MODEL_PATH = os.environ.get(
    "AIRWRITE_MODEL_PATH",
    r"C:\new web\AirCanvas-Finetune\trocr-aircanvas-model",
)

# ---------------------------------------------------------------------------
# Translation
# ---------------------------------------------------------------------------
SOURCE_LANGUAGE = "auto"
TARGET_LANGUAGE = "ta"  # Tamil, as in the original implementation

# ---------------------------------------------------------------------------
# Camera / canvas
# ---------------------------------------------------------------------------
CAMERA_INDEX = 0
CANVAS_HEIGHT = 471
CANVAS_WIDTH = 740
MAX_POINTS_PER_STROKE = 1024

# Smoothing factor applied to the tracked fingertip position
SMOOTHING_ALPHA = 0.7

# Minimum non-zero pixels in the processed canvas before OCR is attempted
MIN_NONZERO_PIXELS_FOR_OCR = 1000

# ---------------------------------------------------------------------------
# Hand tracking
# ---------------------------------------------------------------------------
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.7

# ---------------------------------------------------------------------------
# Drawing colors (BGR, OpenCV convention) and on-screen buttons
# ---------------------------------------------------------------------------
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]  # Blue, Green, Red, Yellow

BUTTON_LABELS = ["CLEAR", "BLUE", "GREEN", "RED", "YELLOW", "RECOGNIZE"]
BUTTON_COLORS = [(0, 0, 0)] + COLORS + [(128, 0, 128)]
BUTTON_COORDS = [(40, 140), (160, 255), (275, 370), (390, 485), (505, 600), (620, 740)]
BUTTON_TOP = 1
BUTTON_BOTTOM = 65

# ---------------------------------------------------------------------------
# Logging / output files
# ---------------------------------------------------------------------------
RECOGNITION_LOG_FILE = "recognized_log.csv"
