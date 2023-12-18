from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from enumfields import Enum, EnumField

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

class REACTION_CHOICES(Enum):
    up_vote = 'upvote'
    down_vote = 'downvote'

class Reaction(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raection_type = EnumField(REACTION_CHOICES, max_length=8)
    created_at = models.DateField(auto_now_add=True)