from celery import shared_task
# Marks this function as a Celery task for asynchronous execution

from collections import Counter
# Efficient utility for counting word frequencies

import re
# Regular expressions used for text normalization and tokenization

from django.db import transaction
# Ensures database operations execute atomically

from .models import Paragraph, WordFrequency
# Models used for paragraph storage and frequency indexing


@shared_task(bind=True, max_retries=3)
# bind=True allows access to task instance for retries and metadata
def compute_frequency(self, paragraph_id):
    try:
        # Execute all database operations atomically to maintain consistency
        with transaction.atomic():
            # Lock the paragraph row to prevent concurrent frequency updates
            paragraph = Paragraph.objects.select_for_update().get(id=paragraph_id)
            
            # Normalize text and extract alphabetic words only
            words = re.findall(r'\b[a-zA-Z]+\b', paragraph.content.lower())
            
            # Compute word occurrence counts efficiently
            freq = Counter(words)
            
            # Remove any previously stored frequencies for this paragraph
            WordFrequency.objects.filter(paragraph=paragraph).delete()
            
            # Prepare new frequency records for bulk insertion
            word_frequencies = [
                WordFrequency(
                    user=paragraph.user,
                    paragraph=paragraph,
                    word=word,
                    count=count
                )
                for word, count in freq.items() if word.strip()
            ]
            
            # Bulk insert for performance when processing large paragraphs
            if word_frequencies:
                WordFrequency.objects.bulk_create(word_frequencies)
            
            # Return structured task result for observability and debugging
            return {
                'paragraph_id': paragraph_id,
                'total_words': len(words),
                'unique_words': len(freq),
                'status': 'completed'
            }
    
    except Paragraph.DoesNotExist:
        # Retry task if paragraph is not yet committed or temporarily unavailable
        self.retry(countdown=5, max_retries=3)
        return {
            'paragraph_id': paragraph_id,
            'status': 'retrying',
            'error': 'Paragraph not found'
        }
    
    except Exception as e:
        # Retry on unexpected failures with backoff for resilience
        self.retry(countdown=10, max_retries=3, exc=e)
        return {
            'paragraph_id': paragraph_id,
            'status': 'error',
            'error': str(e)
        }