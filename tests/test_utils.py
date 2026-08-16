"""
Tests for the drawing engine and configuration values.
"""

from src.core.drawing_engine import DrawingCanvas
from src.utils import config


def test_button_at_returns_correct_label():
    canvas = DrawingCanvas()
    x1, x2 = config.BUTTON_COORDS[0]
    midpoint_x = (x1 + x2) // 2

    assert canvas.button_at(midpoint_x, 30) == "CLEAR"
    assert canvas.button_at(midpoint_x, config.BUTTON_BOTTOM + 10) is None


def test_add_point_and_clear():
    canvas = DrawingCanvas()
    canvas.start_new_stroke()
    canvas.add_point((10, 20))

    active_stroke = canvas.points[canvas.color_index][canvas.stroke_index[canvas.color_index]]
    assert (10, 20) in active_stroke

    canvas.clear()
    assert all(len(strokes) == 1 and len(strokes[0]) == 0 for strokes in canvas.points)


def test_select_color_changes_active_index():
    canvas = DrawingCanvas()
    canvas.select_color(2)
    assert canvas.color_index == 2
