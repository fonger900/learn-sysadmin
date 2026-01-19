from django.db import models
from django.utils import timezone

class Topic(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="terminal", help_text="Icon name/code")

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='articles')
    body = models.TextField(help_text="Markdown content")
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
