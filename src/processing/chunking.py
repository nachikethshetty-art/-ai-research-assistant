import re

def chunk_text(text, max_tokens=200):
    """
    Splits text into chunks of approximately max_tokens tokens.
    Ensures chunks do not split sentences.
    """
    sentences = re.split(r'(\.|\?|\!)', text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        tokens = sentence.split()
        if current_length + len(tokens) > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.extend(tokens)
        current_length += len(tokens)

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Example usage
if __name__ == "__main__":
    sample_text = """
    Lithium-ion batteries are widely used in modern electronics. However, their recycling
    remains a challenge. This paper explores the latest advancements in recycling technologies.
    """
    chunks = chunk_text(sample_text, max_tokens=20)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {chunk}")