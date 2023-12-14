from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here
# class User(models.Model):

class Blog(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING) # ususally admins but admins also has id
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    posted_at = models.DateTimeField("posted_date", default=timezone.now)
    updated_at = models.DateTimeField("updated_at", default=timezone.now)

    def __str__ (self):
        return self.title

class Comment(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    for_blog = models.ForeignKey(Blog, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=1000)
    posted_at = models.DateTimeField("posted_date", default=timezone.now)
    updated_at = models.DateTimeField("posted_date", default=timezone.now)

    def __str__(self):
        return self.content

class Reaction(models.Model):
    REACTION_CHOICES = (
        ('upvote', 'UpVote'),
        ('downvote', 'DownVote'),
    )
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raection_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateField(auto_now_add=True)