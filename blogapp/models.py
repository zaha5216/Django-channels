from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_filename(instance, filename):
    filename = instance.slug + '.jpg'
    return "{0}/{1}".format(instance, filename)


class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def get_post_title(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "Comment by {user} to post {post}".format(user=self.author.username, post=self.post.title)

    def get_comment_text(self):
        return self.comment_text
