import tensorflow as tf

def simple_summarizer(text):
    # this is a simple method that just truncates the text.you would use a TensorFlow-based model for summarization in practical use cases
    return text[:min(500, len(text))]
