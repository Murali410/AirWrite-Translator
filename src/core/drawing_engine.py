"""
Air-canvas drawing engine.

Holds the per-color stroke buffers (bpoints/gpoints/rpoints/ypoints in the
original script) and the logic for starting new strokes, adding points,
clearing the canvas, and rendering strokes onto a frame. This is a direct
extraction of that state and behavior into a reusable class.
"""

from collections import deque

import cv2
import numpy as np

from src.utils import config


class DrawingCanvas:
    """Manages the blank paint window and the colored strokes drawn onto it."""

    def __init__(
        self,
        width: int = config.CANVAS_WIDTH,
        height: int = config.CANVAS_HEIGHT,
        max_points_per_stroke: int = config.MAX_POINTS_PER_STROKE,
    ):
        self.width = width
        self.height = height
        self.max_points_per_stroke = max_points_per_stroke
        self.colors = config.COLORS

        # One list of strokes (deques of points) per color, same structure
        # as the original bpoints/gpoints/rpoints/ypoints lists.
        self.points = [
            [deque(maxlen=max_points_per_stroke)],  # blue
            [deque(maxlen=max_points_per_stroke)],  # green
            [deque(maxlen=max_points_per_stroke)],  # red
            [deque(maxlen=max_points_per_stroke)],  # yellow
        ]
        self.stroke_index = [0, 0, 0, 0]
        self.color_index = 0

        self.canvas = self._blank_canvas()

    def _blank_canvas(self):
        canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        self._draw_buttons(canvas)
        return canvas

    def _draw_buttons(self, image):
        for i, (x1, x2) in enumerate(config.BUTTON_COORDS):
            cv2.rectangle(
                image, (x1, config.BUTTON_TOP), (x2, config.BUTTON_BOTTOM),
                config.BUTTON_COLORS[i], 2,
            )
            cv2.putText(
                image, config.BUTTON_LABELS[i], (x1 + 9, 33),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2,
            )

    def start_new_stroke(self):
        """Begin a new stroke segment for the currently selected color.

        Mirrors the original behavior where lifting/re-raising the finger
        (or losing hand detection) appended a fresh deque.
        """
        strokes = self.points[self.color_index]
        strokes.append(deque(maxlen=self.max_points_per_stroke))
        self.stroke_index[self.color_index] += 1

    def start_new_stroke_if_needed_on_hand_lost(self):
        """Close off any in-progress strokes for all colors.

        Matches the original's `else` branch (no hand detected), which
        appended a new empty deque for every color whose last stroke had
        points in it.
        """
        for color_idx in range(len(self.points)):
            strokes = self.points[color_idx]
            if strokes and len(strokes[-1]) > 0:
                strokes.append(deque(maxlen=self.max_points_per_stroke))
                self.stroke_index[color_idx] += 1

    def add_point(self, point):
        """Append a point to the active stroke of the current color."""
        idx = self.stroke_index[self.color_index]
        self.points[self.color_index][idx].appendleft(point)

    def clear(self):
        """Reset all strokes and the canvas, as the CLEAR button did."""
        self.points = [
            [deque(maxlen=self.max_points_per_stroke)] for _ in range(4)
        ]
        self.stroke_index = [0, 0, 0, 0]
        self.canvas[config.BUTTON_BOTTOM + 2:, :, :] = 255

    def select_color(self, color_index: int):
        self.color_index = color_index

    def render_strokes(self, *targets):
        """Draw every stored stroke onto each provided image (frame/canvas)."""
        for color_idx, strokes in enumerate(self.points):
            for stroke in strokes:
                for k in range(1, len(stroke)):
                    if stroke[k - 1] is None or stroke[k] is None:
                        continue
                    for target in targets:
                        cv2.line(target, stroke[k - 1], stroke[k], self.colors[color_idx], 10)

    def button_at(self, x, y):
        """Return the button label under (x, y), or None."""
        if y > config.BUTTON_BOTTOM:
            return None
        for label, (x1, x2) in zip(config.BUTTON_LABELS, config.BUTTON_COORDS):
            if x1 <= x <= x2:
                return label
        return None
