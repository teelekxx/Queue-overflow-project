from django.db import models
from django.contrib.postgres.fields import ArrayField

class Answer(models.Model):
    questionId = models.IntegerField(blank=False)
    body = models.TextField(blank=False, default='')
    votes = models.IntegerField(default=0)
    writer = models.TextField(max_length=50, blank=False, default='')
    createdAt = models.DateTimeField(auto_now_add=True, blank=True)