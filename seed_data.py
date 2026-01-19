import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from content.models import Topic, Article

def seed():
    Topic.objects.all().delete()
    
    linux = Topic.objects.create(
        name="Linux Essentials",
        slug="linux-essentials",
        description="Master the kernel, shell, and core utilities.",
        icon="terminal"
    )
    
    Article.objects.create(
        title="Introduction to the Shell",
        slug="intro-to-shell",
        topic=linux,
        body="# Introduction to the Shell\n\nThe shell is a command-line interpreter..."
    )
    
    networking = Topic.objects.create(
        name="Networking",
        slug="networking",
        description="Understand the flow of data.",
        icon="network-wired"
    )

    print("Seeded data successfully.")

if __name__ == '__main__':
    seed()
