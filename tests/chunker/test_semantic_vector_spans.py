from lightrag.chunker.semantic_vector import _sentence_spans


def test_sentence_spans_cursor_monotonicity():
    # Scenario: Document has repeating phrases. Sentence 4 has a normalized form
    # matching the top of text, but not present after current cursor position.
    text = (
        "The quick brown fox jumps over the lazy dog. "
        "The quick brown fox jumps again. "
        "Something else here. "
        "End of document."
    )
    sentences = [
        "The quick brown fox jumps over the lazy dog.",
        "The quick brown fox jumps again.",
        "Something else here.",
        "The quick brown fox",  # Exists at start of text (idx 0), but not after cursor (idx 99)
        "End of document.",
    ]

    spans = _sentence_spans(text, sentences)

    # Verify that sentence spans move monotonically forward and cursor never regresses backwards
    prev_end = 0
    for start, end in spans:
        assert start >= prev_end, f"Span start {start} regressed behind previous end {prev_end}"
        prev_end = end
