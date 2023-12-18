from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as login_auth, logout as logout_Auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from .forms import BlogForm, CommentForm, UserForm, UpdateUserForm
from .models import Blog, Comment, Reaction
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


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
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        print("search query: ", search_query)
        queryvalue = super().get_queryset()
        if search_query:
            queryvalue = Blog.objects.filter(Q(content__contains=search_query) | Q(title__contains=search_query))
        return queryvalue

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

def blog_detail(request, blog_id):
    blg = get_object_or_404(Blog, id=blog_id)
    comments = Comment.objects.filter(for_blog=blog_id)
    up_vote_reaction=Reaction.objects.all().filter(raection_type="upvote").filter(post=blog_id).count()
    down_vote_reaction=Reaction.objects.all().filter(raection_type="downvote").filter(post=blog_id).count()

    if request.method == 'POST':
        comment_val = request.POST.get('content')
        reaction_type_ = request.POST.get('reaction_type')
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            # content = form.cleaned_data["content"]
            isinstance = form.save(commit=False)
            isinstance.posted_by = request.user
            isinstance.for_blog = blg
            print("content created")
            form.save()
            # return redirect('blog_detail', blog_id=blog_id)

        # ---------------------------------------------------

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
        
    else:
        form = CommentForm()

    # if request.user.is_authenticated:
    return render(request, "blog/blog.html", {'blog': blg, 'form':form, 'comments': comments, 'up_vote_reaction':up_vote_reaction, 'down_vote_reaction':down_vote_reaction})

def edit_blog(request, blog_id):
    if not request.user.is_authenticated:
        return redirect('login')
    blg = get_object_or_404(Blog, pk=blog_id)
    print(blg.title)
    form = BlogForm(request.POST or None, instance=blg)
    if form.is_valid():
        form.save()
    return render(request, "blog/edit_blog.html", {"form":form})

def my_account(request):
    if not request.user.is_authenticated:
        return redirect('login')
    detail = get_object_or_404(User, pk=request.user.id)
    # User.objects.get(pk=request.user.id)
    form = UpdateUserForm(request.POST or None, instance=detail)
    if form.is_valid():
        form.save()
    return render(request, "blog/account.html", {"form":form})


def forgot_password(request):
    return render(request, "blog/forgot_password.html")