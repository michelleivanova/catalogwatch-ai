from catalogwatch.nlp.parser import parse_ownership_notes


def test_parse_basic_signals():
    text = "Reverted to artist; exclusive license in place; ambiguous legacy contract"
    parsed = parse_ownership_notes(text)
    assert parsed["signals"]["reversion"]
    assert parsed["signals"]["exclusive_license"]
    assert parsed["signals"]["ambiguous"]
    assert parsed["confidence"] > 0
