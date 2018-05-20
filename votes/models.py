from django.db import models
from django.utils import timezone


class Vote(models.Model):
    subject = models.CharField(max_length=512)
    vote_taken = models.DateTimeField(default=timezone.now)
    ayes = models.IntegerField(blank=True, null=True)
    nays = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return f"{self.subject} - {self.ayes}/{self.nays} on {self.vote_taken.strftime('%c')}"