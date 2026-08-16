# Project Overview

## Purpose

AirWrite Translator lets a user handwrite text in the air, using nothing
but a webcam and a raised index finger, and get that handwriting
recognized and translated in real time.

## Problem Statement

Touch-based or pen-based handwriting input requires dedicated hardware
(touchscreens, styluses, or paper) and isn't always convenient — for
example, when quickly jotting down a word to translate, or in contexts
where touching a shared surface is undesirable. There's no lightweight,
camera-only way to write a word in the air and immediately see it
recognized and translated.

## Proposed Solution

AirWrite Translator uses a standard webcam and hand-landmark tracking
(MediaPipe) to follow the user's index fingertip. Raising the index
finger acts as a "pen down" gesture, letting the user draw strokes on a
virtual canvas that is rendered alongside the live camera feed. A
fine-tuned TrOCR (Transformer OCR) model reads the handwriting from the
canvas, and the recognized text is translated (by default into Tamil)
and displayed back to the user.

## Key Features

- Touchless, gesture-based air writing (no stylus or touchscreen needed)
- Real-time hand and fingertip tracking via MediaPipe
- Multi-color virtual canvas with an on-screen toolbar (clear, 4 colors, recognize)
- Handwriting recognition using a fine-tuned TrOCR model
- Automatic translation of recognized text (Tamil by default, configurable)
- Combined live view: webcam feed and canvas shown side by side
- Recognition logging: each recognized/translated pair, plus a snapshot
  image of the processed canvas, is saved automatically

## Workflow

```
Camera Input
    ↓
Hand Detection (MediaPipe)
    ↓
Fingertip Tracking / Gesture Detection
    ↓
Air Writing (Virtual Canvas)
    ↓
Image Preprocessing (threshold, dilate, pad)
    ↓
Character Recognition (TrOCR)
    ↓
Translation (Google Translate via deep-translator)
    ↓
Display + Logging
```

See [`architecture.md`](architecture.md) for how this maps onto the
codebase, [`installation.md`](installation.md) for setup, and
[`usage.md`](usage.md) for how to operate the application.
