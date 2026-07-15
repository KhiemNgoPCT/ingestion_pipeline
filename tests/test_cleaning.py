from cleaning import fix_encoding, remove_boilerplate

def test_fix_encoding_mojibake():
    text = "â€™"
    fixed = fix_encoding(text)
    assert fixed == "'"

def test_remove_boilerplate_page_numbers():
    text = "Page 1 of 5\nContent"
    cleaned = remove_boilerplate(text)
    assert "Content" in cleaned
    assert "Page 1 of 5" not in cleaned
