from django.db import models
from django.contrib.auth.models import User
from tracker.models import Task

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_like', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislike', blank=True)
    edited = models.BooleanField(default=False)
    media = models.FileField(upload_to="comments_media/", blank=True, null=True)

    def number_of_likes(self):
        return self.likes.count()

    def number_of_dislikes(self):
        return self.dislikes.count()

    def short_content(self):
        return str(self.content)[:20]
