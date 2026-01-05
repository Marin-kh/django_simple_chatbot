from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    tags = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

class Query(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.question