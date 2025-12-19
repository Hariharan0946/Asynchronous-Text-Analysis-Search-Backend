from rest_framework.views import APIView
# Base class for creating class-based REST API views

from rest_framework.permissions import IsAuthenticated
# Restricts access so that only authenticated users can call these APIs

from rest_framework.response import Response
from rest_framework import status
# Response helper and HTTP status codes for consistent API replies

from .models import Paragraph, WordFrequency
# Paragraph: stores raw user text
# WordFrequency: stores computed word counts per paragraph per user

from .tasks import compute_frequency
# Celery background task used to compute word frequency asynchronously

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Utilities to disable CSRF for API-only, session-based endpoints


@method_decorator(csrf_exempt, name="dispatch")
class Submit(APIView):
    # API endpoint responsible for accepting multiple paragraphs in one request
    permission_classes = [IsAuthenticated]
    # Only logged-in users are allowed to submit paragraphs

    def post(self, request):
        # Extract the list of paragraphs from the incoming request payload
        paragraphs = request.data.get("paragraphs", [])
        
        # Validate that paragraph data is provided
        if not paragraphs:
            return Response(
                {"error": "No paragraphs provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ensure the input is a list (not string, dict, etc.)
        if not isinstance(paragraphs, list):
            return Response(
                {"error": "Paragraphs must be a list"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_ids = []
        # Iterate through each paragraph submitted by the user
        for text in paragraphs:
            # Create records only for valid, non-empty string inputs
            if text and isinstance(text, str):
                p = Paragraph.objects.create(
                    user=request.user,   # Associate paragraph with authenticated user
                    content=text         # Store raw paragraph content
                )

                # Trigger background processing for word frequency computation
                # This runs asynchronously and does NOT block the API response
                compute_frequency.delay(p.id)

                # Store created paragraph IDs for response tracking
                created_ids.append(p.id)
        
        # Return immediately while background processing continues
        return Response(
            {
                "message": f"Processing {len(created_ids)} paragraphs",
                "paragraph_ids": created_ids,
                "processing": True
            },
            status=status.HTTP_202_ACCEPTED
            # 202 indicates request accepted but processing is not yet complete
        )


@method_decorator(csrf_exempt, name="dispatch")
class Search(APIView):
    # API endpoint for retrieving top paragraphs by word frequency
    permission_classes = [IsAuthenticated]
    # Only authenticated users can search their own data

    def get(self, request):
        # Extract search word from query parameters
        # Normalized to lowercase to ensure case-insensitive matching
        word = request.query_params.get("word", "").strip().lower()
        
        # Validate that a search word is provided
        if not word:
            return Response(
                {"error": "Word parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Query word frequency records scoped to the logged-in user
        # select_related is used to avoid extra database queries
        qs = (
            WordFrequency.objects
            .filter(user=request.user, word=word)  # User-specific search isolation
            .select_related('paragraph')            # Optimizes DB access
            .order_by("-count")[:10]                # Top 10 results by frequency
        )

        results = []
        # Build clean, concise response payload for each result
        for q in qs:
            results.append({
                "paragraph_id": q.paragraph.id,  # Reference to original paragraph
                "content": (
                    q.paragraph.content[:100] + "..."
                    if len(q.paragraph.content) > 100
                    else q.paragraph.content
                ),  # Content preview capped at 100 characters
                "count": q.count,                 # Frequency of searched word
                "created_at": q.paragraph.created_at.isoformat()
                # ISO format ensures consistent datetime representation
            })
        
        # Final structured response sent to the client
        return Response({
            "word": word,                         # Searched keyword
            "total_results": len(results),        # Number of matches returned
            "results": results                    # Top paragraphs by frequency
        })
