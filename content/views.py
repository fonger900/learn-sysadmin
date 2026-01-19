from django.shortcuts import render, Http404
from .utils import ContentLoader

def topic_list(request):
    topics = ContentLoader.get_all_topics()
    return render(request, 'content/topic_list.html', {'topics': topics})

def article_list(request, topic_slug):
    topic = ContentLoader.get_topic(topic_slug)
    if not topic:
        raise Http404("Topic not found")
    articles = ContentLoader.get_articles_by_topic(topic_slug)
    return render(request, 'content/article_list.html', {'topic': topic, 'articles': articles})

def article_detail(request, topic_slug, article_slug):
    article = ContentLoader.get_article(topic_slug, article_slug)
    if not article:
        raise Http404("Article not found")
    # Fetch topic for breadcrumbs
    article.topic = ContentLoader.get_topic(topic_slug) 
    return render(request, 'content/article_detail.html', {'article': article})
