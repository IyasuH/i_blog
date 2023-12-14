from typing import Any
from django import http
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as login_auth, logout as logout_Auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import BlogForm, CommentForm, UserForm
from .models import Blog, Comment, Reaction
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class CreateUserView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'blog/signup.html'
    success_url ='/login/'
    # pass

class CreateBlogView(LoginRequiredMixin, CreateView):
    """
    In this class i inherited LoginRequiredMixin - to check the user is authenticated
    And inherited CreatView to since I am using Generic.view to create data
    """
    model = Blog
    form_class = BlogForm
    template_name = 'blog/new_post.html'
    success_url = '/'
    login_url = '/login/'
    def form_valid(self, form):
        """
        this method is overridden since posted_by value request.user value
        also to check if user is staff or not since only staff can create blog post
        """
        form.instance.posted_by = self.request.user
        print("\n is_staff: ", self.request.user.is_staff)
        if not self.request.user.is_staff:
            print("[INFO] user is not staff cannot creat a post")
            return redirect('home')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """
        this method is overriden to redirect to login_url if user is not authenticated
        """
        if not request.user.is_authenticated:
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)

class ListBlogView(ListView):
    model = Blog
    template_name = 'blog/index.html'
    paginate_by = 10
    context_object_name = 'posts'


# def index(request):
#     posts = Blog.objects.order_by("posted_at")
#     return render(request, "blog/index.html", {'posts': posts})

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        # handle login
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("Username: ", username)
        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None:
            login_auth(request, auth_user)
            print ("user is autheticated")
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, "blog/login.html")

def logout(request):
    logout_Auth(request)
    return redirect("home")

# def new_blog(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     elif not request.user.is_staff:
#         print("user is not staff cannot creat a post")
#         return redirect('home')
#     if request.method == 'POST' and request.user.is_authenticated:
#         form = BlogForm(request.POST)
#         if form.is_valid:
#             print("[INFO]: data validated")
#             isinstance = form.save(commit=False)
#             isinstance.posted_by = request.user 
#             form.save()
#             return HttpResponseRedirect(reverse("home"))
#         else:
#             print("[INFO]: Some how data is not validating")
#     else:
#         form = BlogForm()
#     return render(request, "blog/new_post.html", {'form': form})

# def signup(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid:
#             isinstance = form.save(commit=False)
#             isinstance.last_login = timezone.now()
#             isinstance.date_joined = timezone.now()
#             isinstance.is_superuser = False
#             isinstance.is_staff = False
#             isinstance.is_active = True
#             # isinstance.password = isinstance.set_password(request.POST.get("password"))
#             form.save()
#             return redirect("home")
#         else:
#             print("[INFO]: form does not validate")
#     else:
#         form = UserForm()
#     return render(request, "blog/signup.html", {'form':form})

def blog_detail(request, blog_id):
    blg = get_object_or_404(Blog, id=blog_id)
    comments = Comment.objects.filter(for_blog=blog_id)
    reactions = Reaction.objects.filter(post=blog_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            # content = form.cleaned_data["content"]
            isinstance = form.save(commit=False)
            isinstance.posted_by = request.user
            isinstance.for_blog = blg
            form.save()
            # return redirect('blog_detail', blog_id=blog_id)
    else:
        form = CommentForm()

    reaction_type_ = request.POST.get('reaction_type')
    if request.user.is_authenticated:
        existing_reaction = Reaction.objects.filter(post=blg, user=request.user).first()
        if reaction_type_:
            if existing_reaction:
                existing_reaction.raection_type = reaction_type_
                existing_reaction.save()
            else:
                reaction = Reaction.objects.create(
                    post = blg,
                    user = request.user,
                    raection_type = reaction_type_
                )
    return render(request, "blog/blog.html", {'blog': blg, 'form':form, 'comments': comments, 'reactions':reactions})

def my_account(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "blog/account.html")