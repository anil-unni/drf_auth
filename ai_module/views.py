from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .summarization import summarize_text, SummarizationError
from .question_generation import generate_questions, QuestionGenerationError


@api_view(["POST"])
def summarize_view(request):
    text = request.data.get("text")
    ratio = request.data.get("ratio", 0.3)

    try:
        summary = summarize_text(text, ratio)
        return Response({"summary": summary}, status=status.HTTP_200_OK)
    except SummarizationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def question_generation_view(request):
    text = request.data.get("text")
    try:
        questions = generate_questions(text)
        return Response({"questions": questions}, status=status.HTTP_200_OK)
    except QuestionGenerationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
