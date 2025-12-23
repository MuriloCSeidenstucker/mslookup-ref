from src.ingest.normalizer import normalize_text


def test_normalize_text_basic():
    assert normalize_text("  MEDICAMENTO  ") == "medicamento"


def test_normalize_text_with_accents():
    assert normalize_text("Açúcar e Café") == "acucar e cafe"
    assert normalize_text("CONCEIÇÃO") == "conceicao"


def test_normalize_text_none():
    assert normalize_text(None) is None


def test_normalize_text_empty_or_whitespace():
    assert normalize_text("") is None
    assert normalize_text("   ") is None


def test_normalize_text_multiple_whitespaces():
    assert (
        normalize_text("Remédio    com   Muitos Espaços")
        == "remedio com muitos espacos"
    )
    assert normalize_text("texto\ncom\ttabs") == "texto com tabs"


def test_normalize_text_mixed_complex():
    input_text = "  Vovô viu a VOVÓ no SOFÁ...   "
    assert normalize_text(input_text) == "vovo viu a vovo no sofa..."
