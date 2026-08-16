"""
Text translation using deep_translator's GoogleTranslator.

Extracted from the try/except translation block inside the original
`preprocess_and_run_ocr` function.
"""

from deep_translator import GoogleTranslator

from src.utils import config


def translate_text(
    text: str,
    source: str = config.SOURCE_LANGUAGE,
    target: str = config.TARGET_LANGUAGE,
) -> str:
    """Translate `text` from `source` to `target`.

    Returns "Translation error" on failure, matching the original
    except-block behavior, and logs the failure to stdout.
    """
    try:
        translated = GoogleTranslator(source=source, target=target).translate(text)
        print("Translated text:", translated)
        return translated
    except Exception as e:
        print("Translation failed:", e)
        return "Translation error"
