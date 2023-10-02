import tensorflow as tf

def simple_summarizer(text):
    # This is a simple method that just truncates the text.
    # In a real-world scenario, you'd use a TensorFlow-based model for summarization.
    return text[:min(500, len(text))]
