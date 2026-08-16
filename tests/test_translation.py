"""
Tests for the translation wrapper.

A real call to GoogleTranslator requires network access, so these tests
monkeypatch it to exercise translate_text's success and failure paths
without depending on external services.
"""

import src.translation.translator as translator_module


class _FakeTranslator:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def translate(self, text):
        return f"[{self.target}] {text}"


class _FailingTranslator:
    def __init__(self, source, target):
        pass

    def translate(self, text):
        raise RuntimeError("network unavailable")


def test_translate_text_success(monkeypatch):
    monkeypatch.setattr(translator_module, "GoogleTranslator", _FakeTranslator)

    result = translator_module.translate_text("hello", source="auto", target="ta")

    assert result == "[ta] hello"


def test_translate_text_failure_returns_error_string(monkeypatch):
    monkeypatch.setattr(translator_module, "GoogleTranslator", _FailingTranslator)

    result = translator_module.translate_text("hello")

    assert result == "Translation error"
