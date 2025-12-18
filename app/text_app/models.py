from django.db import models
# Django ORM base for defining database models

from django.conf import settings
# Access project settings to reference the configured user model


class Paragraph(models.Model):
    # Each paragraph belongs to a specific authenticated user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='paragraphs'
    )

    # Stores the raw paragraph text submitted by the user
    content = models.TextField()

    # Timestamp used for ordering and audit purposes
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Return most recent paragraphs first by default
        ordering = ['-created_at']

        # Index to optimize user-specific paragraph queries
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        # Human-readable representation for debugging and admin views
        return f"Paragraph {self.id} by {self.user.username}"


class WordFrequency(models.Model):
    # Associate word frequency entries with the owning user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='word_frequencies'
    )

    # Link frequency data back to the source paragraph
    paragraph = models.ForeignKey(
        Paragraph,
        on_delete=models.CASCADE,
        related_name='word_frequencies'
    )

    # Normalized word token used for search and indexing
    word = models.CharField(max_length=100, db_index=True)

    # Number of occurrences of the word within the paragraph
    count = models.IntegerField(default=0)

    # Timestamp for record creation and potential audit usage
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Improve readability in admin interfaces
        verbose_name_plural = 'Word Frequencies'

        # Default ordering to support top-frequency queries
        ordering = ['-count']

        # Composite indexes to efficiently support user-scoped word searches
        indexes = [
            models.Index(fields=['user', 'word', '-count']),
            models.Index(fields=['word']),
        ]

        # Ensure a word is stored only once per paragraph
        unique_together = ['paragraph', 'word']
    
    def __str__(self):
        # Readable string for logging and debugging
        return f"{self.word}: {self.count} in paragraph {self.paragraph.id}"