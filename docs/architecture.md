# Architecture

## Pipeline

```
Camera
  ↓
Hand Detection (MediaPipe Hands)
  ↓
Hand Landmark Processing (fingertip position, gesture check)
  ↓
Air Canvas (stroke buffers, buttons, rendering)
  ↓
Character Recognition (TrOCR)
  ↓
Translation (Google Translate)
  ↓
Output (combined display + saved snapshot/log)
```

## Module Map

Each pipeline stage above corresponds to a specific module. This mirrors
exactly what the original single-file `main.py` did — the logic has been
separated by responsibility, not rewritten.

| Stage | Module | Responsibility |
|---|---|---|
| Entry point | `src/main.py` | Owns the camera capture loop and wires every other module together, frame by frame. |
| Hand detection & gesture | `src/core/hand_tracking.py` | Wraps MediaPipe Hands; converts landmarks to pixel coordinates; determines whether the index finger is raised (the "pen down" gesture). |
| Air canvas | `src/core/drawing_engine.py` | Owns the per-color stroke buffers, the blank paint window, button hit-testing, and rendering strokes onto a frame. |
| Recognition | `src/recognition/ocr.py` | Loads the fine-tuned TrOCR model, preprocesses the canvas (threshold/dilate/pad), and runs inference. |
| Translation | `src/translation/translator.py` | Wraps `deep_translator.GoogleTranslator` with the same error handling as the original script. |
| Display | `src/ui/display.py` | Draws buttons, the fingertip marker, and recognition/translation text overlays; combines the webcam frame and canvas into one image. |
| Configuration | `src/utils/config.py` | All constants that were previously hardcoded inline: model path, colors, button layout, thresholds, camera index. |
| Persistence | `src/utils/helpers.py` | Saves the processed canvas snapshot and appends to the recognition CSV log. |

## Data Flow Per Frame

1. `main.py` reads a frame from the webcam and flips it horizontally.
2. `HandTracker.process()` runs MediaPipe hand detection on the frame.
3. If a hand is found, `HandTracker` extracts pixel-space landmarks and
   checks the drawing gesture (index fingertip above its lower joint).
4. Fingertip position is smoothed (exponential moving average) and, if
   it's over a toolbar button, triggers that button's action
   (clear / select color / recognize). Otherwise, if drawing is active,
   the point is added to the current stroke in `DrawingCanvas`.
5. `DrawingCanvas.render_strokes()` draws all accumulated strokes onto
   both the live frame and the paint canvas.
6. On **RECOGNIZE**, `HandwritingRecognizer.recognize()` preprocesses the
   canvas and runs the TrOCR model; if text was found, it's passed to
   `translate_text()`, and both results are persisted via
   `save_recognition_result()`.
7. `display.combine_views()` stacks the annotated frame and the canvas
   side by side and the result is shown in the `AirCanvas` window.

## Why This Structure

- **`core/`** holds the real-time, per-frame processing (hand tracking,
  canvas state) — the parts that run continuously.
- **`recognition/`** and **`translation/`** are only invoked on demand
  (when the RECOGNIZE button is pressed), and are kept separate because
  they depend on different, heavier libraries (transformers/torch vs.
  deep-translator).
- **`ui/`** isolates all `cv2.putText`/`cv2.rectangle`/layout code, so
  visual changes don't require touching tracking or recognition logic.
- **`utils/`** centralizes configuration and small persistence helpers
  that don't belong to any single pipeline stage.

No functionality was added or removed during this reorganization — every
function here is a direct extraction of logic that existed in the
original `main.py`.
