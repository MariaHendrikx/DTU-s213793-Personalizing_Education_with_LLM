def chunk_document(document, chunk_size=500):
    """
    Splits a document into smaller parts each of up to `chunk_size` words.
    """
    words = document.split()  # Simple split by whitespace
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# Example usage
large_document = "Your very large document text here..."
chunks = chunk_document(large_document, chunk_size=500)

# Process each chunk independently
for chunk in chunks:
    # Apply NLP model, analysis, etc., on the chunk
    pass
