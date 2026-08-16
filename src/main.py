"""
AirWrite Translator — application entry point.

Pipeline (unchanged from the original single-file implementation):

    Camera -> Hand Detection -> Air Writing -> Air Canvas ->
    Character Recognition (TrOCR) -> Translation -> Display

Run with:
    python src/main.py
or, from the project root:
    python main.py
"""

import time

import cv2

from src.core.drawing_engine import DrawingCanvas
from src.core.hand_tracking import HandTracker
from src.recognition.ocr import HandwritingRecognizer
from src.translation.translator import translate_text
from src.ui import display
from src.utils import config
from src.utils.helpers import save_recognition_result


def run():
    recognizer = HandwritingRecognizer()
    tracker = HandTracker()
    canvas = DrawingCanvas()

    cap = cv2.VideoCapture(config.CAMERA_INDEX)

    prev_x, prev_y = 0, 0
    recognized_text = ""
    translated_text = ""
    was_drawing_enabled = False

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            display.draw_buttons(frame)

            result = tracker.process(frame_rgb)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    lm_list = tracker.landmark_pixel_coords(hand_landmarks, w, h)
                    tracker.draw_landmarks(frame, hand_landmarks)

                    cx, cy = tracker.fingertip_position(lm_list)
                    smooth_x = int(config.SMOOTHING_ALPHA * prev_x + (1 - config.SMOOTHING_ALPHA) * cx)
                    smooth_y = int(config.SMOOTHING_ALPHA * prev_y + (1 - config.SMOOTHING_ALPHA) * cy)
                    prev_x, prev_y = smooth_x, smooth_y

                    drawing_enabled = tracker.is_drawing_gesture(lm_list)

                    if drawing_enabled and not was_drawing_enabled:
                        canvas.start_new_stroke()
                    was_drawing_enabled = drawing_enabled

                    display.draw_fingertip_marker(frame, (smooth_x, smooth_y), drawing_enabled)

                    button = canvas.button_at(smooth_x, smooth_y)
                    if button is not None:
                        if button == "CLEAR":
                            canvas.clear()
                            recognized_text = ""
                            translated_text = ""
                        elif button == "BLUE":
                            canvas.select_color(0)
                        elif button == "GREEN":
                            canvas.select_color(1)
                        elif button == "RED":
                            canvas.select_color(2)
                        elif button == "YELLOW":
                            canvas.select_color(3)
                        elif button == "RECOGNIZE":
                            time.sleep(0.3)
                            recognized_text, processed = recognizer.recognize(canvas.canvas)
                            translated_text = (
                                translate_text(recognized_text)
                                if recognized_text != "No handwriting detected"
                                else ""
                            )
                            save_recognition_result(processed, recognized_text, translated_text)
                            time.sleep(0.5)
                    elif drawing_enabled:
                        canvas.add_point((smooth_x, smooth_y))
            else:
                canvas.start_new_stroke_if_needed_on_hand_lost()

            canvas.render_strokes(frame, canvas.canvas)

            display.draw_recognition_overlay(frame, canvas.canvas, recognized_text, translated_text)

            combined = display.combine_views(frame, canvas.canvas)
            cv2.imshow("AirCanvas", combined)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
