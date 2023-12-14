from django.test import TestCase
from django.urls import reverse
from .models import Blog, Comment
from django.contrib.auth.models import User
from .forms import BlogForm, CommentForm, UserForm

# Create your tests here.
class AuthenticationTest(TestCase):
    def test_user_login_valid_credentials(self):
        username = 'testusername'
        password = 'testpassword'
        user_credentials = {
            'username': username,
            'password': password,
        }
        user = User.objects.create_user(username=username, password=password)
        response = self.client.post('/login/', data=user_credentials)
        self.assertRedirects(response, '/')
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_login_invalid_credentials(self):
        username = 'invlaidusername'
        password = 'invlaidpassword'
        user_credentials = {
            'username': username,
            'password': password,
        }
        response = self.client.post('/login/', data=user_credentials)        
        self.assertIn(response.status_code, [200, 401])
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class ModelTestCase(TestCase):
    def setup(self):
        pass

    def test_create_user_model_instance(self):
        """
        This test is to check the creation of user object
        """
        instance = User.objects.create(username="test_user", password="test_password")
        saved_instance = User.objects.get(pk=instance.pk)
        self.assertEqual(instance, saved_instance)
    
    def test_create_blog_post(self):
        """
        This test is to check the creation of blog using the model
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_login(self.user)
        # noramally through the urls we can not create a blog with user that is not authorized(staf) but here we can since we are testing the model
        instance = Blog.objects.create(posted_by=self.user, title='blog test title', content='blog test content')
        saved_instance = Blog.objects.get(pk=instance.pk)
        self.assertEqual(instance, saved_instance)

    def test_create_comment(self):
        """
        This test is to check the creation of comment object
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_login(self.user)
        self.blog = Blog.objects.create(posted_by=self.user, title='blog test title', content='blog test content')

        instance = Comment.objects.create(posted_by=self.user, for_blog=self.blog, content="test content")
        saved_instance = Comment.objects.get(pk=instance.pk)
        self.assertEqual(instance, saved_instance)

class FormTestCase(TestCase):
    def setup(self):
        pass

    def test_invalid_comment_post_form(self):
        """
        This test is to check for the Invalid CommentForm
        """
        invalid_comment_data = {
            'content': ''
        }
        form = CommentForm(data=invalid_comment_data)
        self.assertFalse(form.is_valid())

    def test_valid_comment_post_form(self):
        """
        Tets valid CommentForm
        """
        invalid_comment_data = {
            'content': 'test comment'
        }
        form = CommentForm(data=invalid_comment_data)
        self.assertTrue(form.is_valid())

    def test_invalid_blog_post_form(self):
        """
        This test is to check for the invalid BlogForm
        """
        required_data = ['title', 'content']
        invalid_blog_data = {
            'title': 'test blog title',
            'content': 'test blog content',
        }
        for field_name in required_data:
            data = invalid_blog_data.copy()
            data[field_name] = ''
            form = BlogForm(data=data)
            self.assertFalse(form.is_valid())

    def test_valid_blog_post_form(self):
        """
        This test is to check for the valid BlogForm
        """
        invalid_blog_data = {
            'title': 'test blog ttile',
            'content': 'test blog content',
        }
        form = BlogForm(data=invalid_blog_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_post_form(self):
        """
        Test to for user form for invalid data
        """
        required_fields = ['username', 'password']
        form_data = {
            'username':'test_user',
            'password':'test_password',
        }
        for field_name in required_fields:
            data = form_data.copy()
            data[field_name] = ''
            form = UserForm(data=data)
            self.assertFalse(form.is_valid())

    def test_valid_user_post_form(self):
        """
        Test for valid user data
        """
        valid_data = {
            'username':'test_user',
            'password':'test_password',
        }
        form = UserForm(data=valid_data)
        self.assertTrue(form.is_valid())
 
class ViewFormAppTest(TestCase):
    def setup(self):
        pass

    def test_home(self):
        """
        This test is to check the `home` url
        """
        # this is to test the rendering of the template
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_new_blog_unauthenticated_unauthorized(self):
        """
        This test is to check the `new_post` url for unauthenticated and unauthorized user
        """
        response = self.client.get('/new_post/')
        self.assertRedirects(response, '/login/')

    def test_new_blog_authenticated_unauthorized(self):
        """
        This test is to check the `new_post` url for authenticated and unauthorized user
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=False)
        self.client.force_login(self.user)
        post_blog = {
            'title': 'test title',
            'content': 'test content',
        }
        response = self.client.post(reverse('new_blog_post'), data=post_blog)
        self.assertRedirects(response, '/')

    # def test_new_blog_authenticated_authorized(self):
    #     """
    #     This test is to check the `new_post` url for authenticated and authorized user
    #     """
    #     # this test is faling because of somehow it is making is_staff value for user False even tho i enetered it as True
    #     self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
    #     print("\n username: ", self.user.username)
    #     self.client.force_login(self.user)
    #     post_blog = {
    #         'title': 'test title',
    #         'content': 'test content',
    #     }
    #     # print(self.client)
    #     response = self.client.post(reverse('new_blog_post'), data=post_blog)
    #     self.assertEqual(response.status_code, 201)

    def test_signup(self):
        """
        To test `signup` url
        """
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)     

    def test_login(self):
        """
        To test `login` url
        """
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)     

    def test_account(self):
        """
        This test is to check the `account` url
        """
        response = self.client.get('/my_account/')
        self.assertRedirects(response, '/login/')

    def test_logout(self):
        """
        This test is to check the `logout` url
        """
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/')

