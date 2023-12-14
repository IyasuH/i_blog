from django import forms
from .models import Blog, Comment
from django.contrib.auth.models import User

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('id', 'posted_by', 'title', 'content', 'posted_at', 'updated_at')
        exclude = ('posted_at', 'updated_at', 'posted_by')
        read_only_fields = ('id',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('id', 'posted_by', 'for_blog', 'content', 'posted_at', 'updated_at')
        exclude = ('posted_by', 'for_blog', 'posted_at', 'updated_at')
        read_only_fields = ('id',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined',)
        exclude = ('last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
        read_ponly_fields = ('id')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user