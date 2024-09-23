from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import torch


class SummarizationError(Exception):
    """Custom exception for summarization errors."""
    pass

def summarize_text(text, ratio=0.3, model_name="facebook/bart-large-cnn"):
    """
    Summarizes the given text using a model from the Hugging Face transformers library.
    """
    if not text:
        raise SummarizationError("Input text cannot be empty.")

    if len(text.split()) < 20:
        raise SummarizationError("Input text must be at least 20 words long.")

    # Calculate lengths dynamically based on input text
    input_length = len(text.split())
    max_length = min(int(input_length * ratio * 1.5), 250)  # Ensure it does not exceed a reasonable cap
    min_length = max(int(input_length * ratio), 30)  # Minimum length should be reasonable

    try:
        # Detect device (0 for GPU, -1 for CPU)
        device = 0 if torch.cuda.is_available() else -1

        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Create summarization pipeline with the specified model
        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, device=device)

        # Generate summary with adjusted lengths
        summary = summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
        )

        # Check if summary generation was successful
        if not summary or not summary[0]["summary_text"]:
            raise SummarizationError("Summarization failed, possibly due to insufficient content.")

        return summary[0]["summary_text"]

    except Exception as e:
        raise SummarizationError(f"An error occurred during summarization: {str(e)}")