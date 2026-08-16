"""
Tests for the image preprocessing used before OCR.

These cover `HandwritingRecognizer.enhance_image`, which is a pure
function (no camera, no model) and so is safe to test directly.
"""

import numpy as np

from src.recognition.ocr import HandwritingRecognizer


def test_enhance_image_pads_and_thresholds_blank_canvas():
    blank_canvas = np.ones((471, 740, 3), dtype=np.uint8) * 255

    result = HandwritingRecognizer.enhance_image(blank_canvas)

    # 20px border added on each side, single-channel thresholded output
    assert result.shape == (471 + 40, 740 + 40)
    # The interior (excluding the constant-255 padding border) should be
    # empty when nothing was drawn.
    interior = result[20:-20, 20:-20]
    assert np.count_nonzero(interior) == 0


def test_enhance_image_detects_drawn_content():
    canvas = np.ones((471, 740, 3), dtype=np.uint8) * 255
    canvas[100:400, 100:600] = 0  # simulate a large drawn stroke

    result = HandwritingRecognizer.enhance_image(canvas)
    interior = result[20:-20, 20:-20]

    assert np.count_nonzero(interior) > 1000
