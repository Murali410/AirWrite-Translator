# Usage

## Starting the application

```bash
python main.py
```

This opens a single window, **AirCanvas**, split into two halves:

- **Left**: your live webcam feed, with hand landmarks and the toolbar drawn on top.
- **Right**: the virtual canvas, where your air-written strokes accumulate.

## The toolbar

Six buttons run across the top of both the webcam feed and the canvas:

| Button | Action |
|---|---|
| `CLEAR` | Erases all strokes and resets the canvas. |
| `BLUE` / `GREEN` / `RED` / `YELLOW` | Selects the ink color for new strokes. |
| `RECOGNIZE` | Runs handwriting recognition and translation on the current canvas. |

## Air writing

1. Hold your hand up so it's visible to the webcam.
2. **Raise your index finger** (straighten it upward) to start drawing — this is
   the "pen down" gesture. A **green** dot on your fingertip means drawing is
   active; **red** means it's lifted ("pen up").
3. Move your hand to draw strokes on the canvas in the currently selected color.
4. Lower your index finger, or move your hand out of frame, to stop the
   current stroke without drawing.
5. Move your fingertip over a toolbar button (top of the window) to trigger
   it — color buttons switch ink color, `CLEAR` wipes the canvas.

## Recognition and translation

Move your fingertip over the `RECOGNIZE` button once you've finished
writing:

1. The canvas is preprocessed (grayscaled, thresholded, dilated, and
   padded) to make the handwriting easier for the model to read.
2. If the canvas looks essentially empty, the app reports
   **"No handwriting detected"** and skips translation.
3. Otherwise, the fine-tuned TrOCR model recognizes the handwritten text.
4. The recognized text is translated (Tamil by default — see
   [`installation.md`](installation.md) / `src/utils/config.py` to change
   the target language) using Google Translate.
5. Both the recognized and translated text are displayed at the bottom of
   the webcam feed and canvas.

## Output and logs

Every time `RECOGNIZE` runs successfully:

- The processed (thresholded/padded) canvas image is saved as
  `canvas_<timestamp>.png` in the project's working directory.
- A row of `timestamp,recognized_text,translated_text` is appended to
  `recognized_log.csv` in the working directory.

Neither of these runtime files is tracked in git (see `.gitignore`); the
`output/` folder instead holds static demo screenshots — see
[`output/README.md`](../output/README.md).

## Exiting

With the **AirCanvas** window focused, press `q` to close the window and
release the camera.
