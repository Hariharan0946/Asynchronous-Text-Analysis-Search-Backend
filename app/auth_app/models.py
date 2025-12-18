from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    # Track consecutive failed logins to mitigate brute-force attacks
    failed_attempts = models.PositiveIntegerField(default=0)

    # Timestamp until which the account is locked after repeated failures
    lock_until = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        # Reuse Django's default auth_user table for compatibility
        db_table = 'auth_user'
    
    def is_locked(self):
        # Determine whether the account is currently locked
        return self.lock_until and timezone.now() < self.lock_until
    
    def reset_lock(self):
        # Clear lock state after successful authentication
        self.failed_attempts = 0
        self.lock_until = None
        self.save(update_fields=['failed_attempts', 'lock_until'])
    
    def increment_failed_attempts(self):
        # Increment failure count and temporarily lock account if threshold exceeded
        self.failed_attempts += 1
        if self.failed_attempts >= 5:
            self.lock_until = timezone.now() + timedelta(minutes=15)
        self.save(update_fields=['failed_attempts', 'lock_until'])