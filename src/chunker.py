def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Split long text into overlapping chunks.

    Args:
        text: Article text.
        chunk_size: Maximum characters per chunk.
        overlap: Characters shared between consecutive chunks.

    Returns:
        List of text chunks.
    """

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Stop after reaching the end
        if end >= len(text):
            break

        start = end - overlap

    return chunks