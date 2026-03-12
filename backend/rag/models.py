from django.db import models


class Document(models.Model):
    content = models.TextField()
    embedding = models.JSONField()

    def __str__(self):
        return self.content[:50]


class QueryLog(models.Model):
    query = models.TextField()
    cache_hit = models.BooleanField()
    response_time_ms = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query