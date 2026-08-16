# Installation

## Requirements

- Python 3.9–3.11 recommended (required by `mediapipe`'s prebuilt wheels;
  check [MediaPipe's supported versions](https://pypi.org/project/mediapipe/)
  if you're on a newer Python).
- A working webcam.
- The dependencies listed in [`requirements.txt`](../requirements.txt):
  - `opencv-python`
  - `numpy`
  - `mediapipe`
  - `Pillow`
  - `transformers`
  - `torch`
  - `deep-translator`
  - `sentencepiece`

## 1. Clone the repository

```bash
git clone <repository-url>
cd AirWrite-Translator
```

## 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

`torch` and `transformers` are large downloads; installation may take a
few minutes.

## 4. Provide the fine-tuned TrOCR model

The recognizer loads a **fine-tuned** TrOCR model (not the base
Hugging Face model) from a local folder. This model is not included in
the repository — you need your own fine-tuned model directory,
containing the standard Hugging Face `TrOCRProcessor` /
`VisionEncoderDecoderModel` files.

By default, the application looks for the model at the same path used
during original development:

```
C:\new web\AirCanvas-Finetune\trocr-aircanvas-model
```

To point at your own model location, set the `AIRWRITE_MODEL_PATH`
environment variable before running the app:

```bash
# Windows (PowerShell)
$env:AIRWRITE_MODEL_PATH = "C:\path\to\your\trocr-aircanvas-model"

# macOS / Linux
export AIRWRITE_MODEL_PATH=/path/to/your/trocr-aircanvas-model
```

See [`src/utils/config.py`](../src/utils/config.py) for how this is read.

## 5. Run the application

From the project root:

```bash
python main.py
```

or equivalently:

```bash
python src/main.py
```

A window titled **AirCanvas** should open, showing your webcam feed next
to the virtual canvas. Press `q` with that window focused to quit.

See [`usage.md`](usage.md) for how to interact with the app once it's
running.
