from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM


class SummarizationError(Exception):
    """Custom exception for summarization errors."""

    pass


def summarize_text(
    text, model_name="facebook/bart-large-cnn", max_length=150, min_length=50
):
    """
    Summarizes the given text using a model from the Hugging Face transformers library.

    Args:
        text (str): The text to be summarized.
        model_name (str): The name of the model to use for summarization.
        max_length (int): The maximum length of the generated summary.
        min_length (int): The minimum length of the generated summary.

    Returns:
        str: The summarized text.

    Raises:
        SummarizationError: If the input text is empty, too short, or if summarization fails.
    """
    if not text:
        raise SummarizationError("Input text cannot be empty.")

    if len(text.split()) < 20:
        raise SummarizationError("Input text must be at least 20 words long.")

    try:
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Create summarization pipeline with the specified model
        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

        # Generate summary
        summary = summarizer(
            text, max_length=max_length, min_length=min_length, do_sample=False
        )

        # Check if summary generation was successful
        if not summary or not summary[0]["summary_text"]:
            raise SummarizationError(
                "Summarization failed, possibly due to insufficient content."
            )

        return summary[0]["summary_text"]

    except Exception as e:
        raise SummarizationError(f"An error occurred during summarization: {str(e)}")
