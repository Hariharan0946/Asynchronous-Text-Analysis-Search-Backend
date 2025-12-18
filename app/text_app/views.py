from rest_framework.views import APIView
# Base class for building RESTful API endpoints

from rest_framework.permissions import IsAuthenticated
# Ensures only authenticated users can access these endpoints

from rest_framework.response import Response
from rest_framework import status
# Utilities for structured API responses and HTTP status codes

from .models import Paragraph, WordFrequency
# Models used for paragraph storage and frequency lookup

from .tasks import compute_frequency
# Background task responsible for word frequency computation

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# CSRF utilities for session-based API handling


@method_decorator(csrf_exempt, name="dispatch")
class Submit(APIView):
    # Endpoint for submitting multiple paragraphs in a single request
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract paragraph list from request payload
        paragraphs = request.data.get("paragraphs", [])
        
        # Validate presence of paragraph data
        if not paragraphs:
            return Response(
                {"error": "No paragraphs provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ensure payload format is a list
        if not isinstance(paragraphs, list):
            return Response(
                {"error": "Paragraphs must be a list"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_ids = []
        for text in paragraphs:
            # Create paragraph records only for valid text entries
            if text and isinstance(text, str):
                p = Paragraph.objects.create(
                    user=request.user,
                    content=text
                )

                # Trigger asynchronous word frequency computation
                compute_frequency.delay(p.id)

                created_ids.append(p.id)
        
        # Return immediate response while processing continues in background
        return Response(
            {
                "message": f"Processing {len(created_ids)} paragraphs",
                "paragraph_ids": created_ids,
                "processing": True
            },
            status=status.HTTP_202_ACCEPTED
        )


@method_decorator(csrf_exempt, name="dispatch")
class Search(APIView):
    # Endpoint for retrieving top paragraphs by word frequency
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Extract and normalize search word from query parameters
        word = request.query_params.get("word", "").strip().lower()
        
        # Validate required query parameter
        if not word:
            return Response(
                {"error": "Word parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Query word frequency data scoped to the authenticated user
        qs = (
            WordFrequency.objects
            .filter(user=request.user, word=word)
            .select_related('paragraph')
            .order_by("-count")[:10]
        )

        results = []
        for q in qs:
            # Build concise, user-facing response payload
            results.append({
                "paragraph_id": q.paragraph.id,
                "content": (
                    q.paragraph.content[:100] + "..."
                    if len(q.paragraph.content) > 100
                    else q.paragraph.content
                ),
                "count": q.count,
                "created_at": q.paragraph.created_at.isoformat()
            })
        
        return Response({
            "word": word,
            "total_results": len(results),
            "results": results
        })
