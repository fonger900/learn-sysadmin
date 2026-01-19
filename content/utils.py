import os
import frontmatter
from django.conf import settings
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class FileTopic:
    name: str
    slug: str
    description: str
    icon: str

@dataclass
class FileArticle:
    title: str
    slug: str
    topic_slug: str
    body: str
    published_date: datetime

class ContentLoader:
    CONTENT_DIR = os.path.join(settings.BASE_DIR, 'tutorials')

    @classmethod
    def get_all_topics(cls) -> List[FileTopic]:
        topics = []
        if not os.path.exists(cls.CONTENT_DIR):
            return []
            
        for topic_slug in os.listdir(cls.CONTENT_DIR):
            topic_path = os.path.join(cls.CONTENT_DIR, topic_slug)
            if not os.path.isdir(topic_path):
                continue
                
            metadata_path = os.path.join(topic_path, '_topic.md')
            if os.path.exists(metadata_path):
                data = frontmatter.load(metadata_path)
                topics.append(FileTopic(
                    name=data['name'],
                    slug=topic_slug,
                    description=data.get('description', ''),
                    icon=data.get('icon', 'terminal')
                ))
        return topics

    @classmethod
    def get_topic(cls, slug: str) -> Optional[FileTopic]:
        topics = cls.get_all_topics()
        for topic in topics:
            if topic.slug == slug:
                return topic
        return None

    @classmethod
    def get_articles_by_topic(cls, topic_slug: str) -> List[FileArticle]:
        topic_path = os.path.join(cls.CONTENT_DIR, topic_slug)
        if not os.path.exists(topic_path):
            return []
            
        articles = []
        for filename in os.listdir(topic_path):
            if filename.startswith('_') or not filename.endswith('.md'):
                continue
                
            file_path = os.path.join(topic_path, filename)
            data = frontmatter.load(file_path)
            article_slug = filename.replace('.md', '')
            
            articles.append(FileArticle(
                title=data['title'],
                slug=article_slug,
                topic_slug=topic_slug,
                body=data.content,
                published_date=data.get('date', datetime.now())
            ))
            
        # Sort by slug or date essentially (simple sort for now)
        return sorted(articles, key=lambda x: x.slug)

    @classmethod
    def get_article(cls, topic_slug: str, article_slug: str) -> Optional[FileArticle]:
        file_path = os.path.join(cls.CONTENT_DIR, topic_slug, f'{article_slug}.md')
        if not os.path.exists(file_path):
            return None
            
        data = frontmatter.load(file_path)
        return FileArticle(
            title=data['title'],
            slug=article_slug,
            topic_slug=topic_slug,
            body=data.content,
            published_date=data.get('date', datetime.now())
        )
