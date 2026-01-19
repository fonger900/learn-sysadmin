from django.shortcuts import render, get_object_or_404
from .models import Topic, Article

def topic_list(request):
    topics = Topic.objects.all()
    return render(request, 'content/topic_list.html', {'topics': topics})

def article_list(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    articles = topic.articles.filter(is_published=True)
    return render(request, 'content/article_list.html', {'topic': topic, 'articles': articles})

def article_detail(request, topic_slug, article_slug):
    article = get_object_or_404(Article, topic__slug=topic_slug, slug=article_slug)
    return render(request, 'content/article_detail.html', {'article': article})
