from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListBlogView.as_view(), name="home"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("new_post/", views.CreateBlogView.as_view(), name="new_blog_post"),
    path("signup/", views.CreateUserView.as_view(), name="signup"),
    path("blog/<int:blog_id>/", views.blog_detail, name="blog_detail"),
    path("my_account/", views.my_account, name="account"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("edit_blog/<int:blog_id>/", views.edit_blog, name="edit_blog"),
]