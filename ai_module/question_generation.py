from transformers import pipeline


class QuestionGenerationError(Exception):
    pass


def generate_questions(text):
    if not text:
        raise QuestionGenerationError("Input text cannot be empty.")

    try:
        question_generator = pipeline("question-generation")
        questions = question_generator(text)
        return questions
    except Exception as e:
        raise QuestionGenerationError(
            f"An error occurred during question generation: {str(e)}"
        )
