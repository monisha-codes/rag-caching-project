import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg

from .rag_pipeline import rag_pipeline
from .models import QueryLog


@api_view(["POST"])
def ask_question(request):

    question = request.data.get("question")

    if not question:
        return Response({"error": "Question is required"}, status=400)

    start = time.time()

    try:
        answer, cache_hit = rag_pipeline(question)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    end = time.time()

    response_time = int((end - start) * 1000)

    QueryLog.objects.create(
        query=question,
        cache_hit=cache_hit,
        response_time_ms=response_time
    )

    return Response({
        "answer": answer,
        "cache_used": cache_hit,
        "response_time": response_time
    })


@api_view(["GET"])
def metrics(request):

    total = QueryLog.objects.count()
    hits = QueryLog.objects.filter(cache_hit=True).count()

    avg_time = QueryLog.objects.aggregate(
        Avg("response_time_ms")
    )["response_time_ms__avg"] or 0

    hit_rate = (hits / total) * 100 if total > 0 else 0

    return Response({
        "total_queries": total,
        "cache_hit_rate": hit_rate,
        "avg_response_time": avg_time
    })