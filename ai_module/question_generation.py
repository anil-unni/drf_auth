import spacy
import random

class QuestionGenerationError(Exception):
    pass

def generate_questions_and_answers(text):
    if not text:
        raise QuestionGenerationError("Input text cannot be empty.")

    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        qa_pairs = []

        for sent in doc.sents:
            nouns = [token.text for token in sent if token.pos_ == 'NOUN']
            if nouns:
                question = f"What is {nouns[0]}?"
                answer = sent.text
                qa_pairs.append({'question': question, 'answer': answer})

        random.shuffle(qa_pairs)
        return qa_pairs

    except Exception as e:
        raise QAGeneratorError(
            f"An error occurred during question generation: {str(e)}"
        )

