from django.urls import path
from .views import ask_question,metrics

urlpatterns = [
    path("ask", ask_question),
    path("metrics", metrics)
]