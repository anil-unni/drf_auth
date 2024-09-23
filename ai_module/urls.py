# summarizer/urls.py

from django.urls import path
from .views import summarize_view, question_generation_view

urlpatterns = [
    path("summarize/", summarize_view, name="summarize"),
    path("generate-questions/", question_generation_view, name="generate_questions"),
]
