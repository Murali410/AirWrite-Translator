# Output / Demo Images

This folder contains sample screenshots of AirWrite Translator in action.

| File | Description |
|---|---|
| `airtrans.png` | Screenshot of the air-writing / hand-tracking interface, showing the live webcam feed, the on-screen color and action buttons, and the drawn air-canvas strokes. |
| `translation.png` | Screenshot of the recognition and translation output, showing recognized handwritten text alongside its Tamil translation. |

These are static reference images kept for documentation purposes. At
runtime the application additionally writes timestamped canvas snapshots
(`canvas_<timestamp>.png`) and a `recognized_log.csv` file to the working
directory each time the **RECOGNIZE** button is used; those generated
files are not tracked in this folder and are ignored by `.gitignore`.
