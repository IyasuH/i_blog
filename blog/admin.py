from django.contrib import admin
from .models import Comment, Blog

# Register your models here.
admin.site.register(Comment)
admin.site.register(Blog)
