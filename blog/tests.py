from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Blog, Comment, Reaction
from django.contrib.auth.models import User
from .forms import BlogForm, CommentForm, UserForm
from django.core.exceptions import ValidationError
from blog.views import ListBlogView

# Create your tests here.
class AuthenticationTest(TestCase):
    def test_user_login_valid_credentials(self):
        """
        to test login with valid credentials
        """
        username = 'testusername'
        password = 'testpassword'
        user_credentials = {
            'username': username,
            'password': password,
        }
        User.objects.create_user(username=username, password=password)
        response = self.client.post('/login/', data=user_credentials)
        self.assertRedirects(response, '/')
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_login_invalid_credentials(self):
        """
        To test login with invalid credentials
        """
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

    def test_create_reaction(self):
        """
        to test the creation of reactions
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_login(self.user)
        self.blog = Blog.objects.create(posted_by=self.user, title='blog test title', content='blog test content')
        instance = Reaction.objects.create(post=self.blog, user=self.user, raection_type='upvote')
        saved_instance = Reaction.objects.get(pk=instance.pk)
        self.assertEqual(instance, saved_instance) # to check if the reaction is created
        # change reaction 
        instance_1 = Reaction.objects.create(post=self.blog, user=self.user, raection_type='downvote')
        saved_instance_1 = Reaction.objects.get(pk=instance_1.pk)
        self.assertEqual(instance_1.pk, saved_instance_1.pk)

    def test_create_wrong_reaction(self):
        """
        to test that wrong reaction_type will return ValidationError
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_login(self.user)
        self.blog = Blog.objects.create(posted_by=self.user, title='blog test title', content='blog test content')
        with self.assertRaises(ValidationError):
            Reaction.objects.create(post=self.blog, user=self.user, raection_type='up')


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

    def test_new_blog_authenticated_authorized(self):
        """
        This test is to check the `new_post` url for authenticated and authorized user
        """
        # this test is faling because of somehow it is making is_staff value for user False even tho i enetered it as True
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.client.force_login(self.user)
        post_blog = {
            'title': 'test title',
            'content': 'test content',
        }
        self.client.post(reverse('new_blog_post'), data=post_blog)
        self.assertEqual(Blog.objects.count(), 1)

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

    def test_account_unauthorized(self):
        """
        To test the `account` url unauthorized
        """
        response = self.client.get('/my_account/')
        self.assertRedirects(response, '/login/')

    def test_account_authorized(self):
        """
        to test 'account' url authorized
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.client.force_login(self.user)
        response = self.client.get('/my_account/')
        self.assertEqual(response.status_code, 200)
        
    def test_blog_detail_unauthorized(self):
        """
        To test the `blog_detail` url unauthorized
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.blog = Blog.objects.create(posted_by=self.user, title='blog test title', content='blog test content')
        response = self.client.get(f'/blog/{self.blog.pk}')
        self.assertRedirects(response, f'/blog/{self.blog.pk}/', status_code=301) # unauthorized users still can access blog detail

    def test_blog_detail_authorized(self):
        """
        To test the `blog_detail` url authorized
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.client.force_login(self.user)
        self.blog = Blog.objects.create(posted_by=self.user, title='blog test title', content='blog test content')
        response = self.client.get(f'/blog/{self.blog.pk}')
        self.assertRedirects(response, f'/blog/{self.blog.pk}/', status_code=301) # authorized users still can access blog detail

    def test_blog_detail_comment_creation_authorized(self):
        """
        to test comment creation for specific blog
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.client.force_login(self.user)
        self.blog = Blog.objects.create(posted_by=self.user, title='blog test title', content='blog test content')
        comment_data = {
            'content': "Test comment"
        }
        response = self.client.post(f'/blog/{self.blog.pk}/', data=comment_data)
        created_object = Comment.objects.get(posted_by=self.user, for_blog=self.blog)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(created_object.content, comment_data['content'])

    def test_blog_detail_comment_creation_unauthorized(self):
        """
        to test comment creation for specific blog unautorized
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.blog = Blog.objects.create(posted_by=self.user, title='blog test title', content='blog test content')
        comment_data = {
            'content': "Test comment"
        }
        response = self.client.post(f'/blog/{self.blog.pk}/', data=comment_data)
        self.assertRedirects(response, '/login/')

    def test_blog_detail_reaction_authorized(self):
        """
        to test reaction creation authorized
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.client.force_login(self.user)
        self.blog = Blog.objects.create(posted_by=self.user, title='blog test title', content='blog test content')
        vote_data = {
            'reaction_type':'upvote'
        }
        response = self.client.post(f'/blog/{self.blog.pk}/', data=vote_data)
        self.assertEqual(Reaction.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_blog_detail_reaction_unauthorized(self):
        """
        to test reaction creation unauthorized
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.blog = Blog.objects.create(posted_by=self.user, title='blog test title', content='blog test content')
        vote_data = {
            'reaction_type':'upvote'
        }
        response = self.client.post(f'/blog/{self.blog.pk}/', data=vote_data)
        self.assertRedirects(response, '/login/')

    def test_logout(self):
        """
        This test is to check the `logout` url
        """
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/')

    def test_search_functionality(self):
        """
        To test the search functionality for blog list
        """
        self.factory = RequestFactory()
        self.url = reverse('home')
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.client.force_login(self.user)
        Blog.objects.create(posted_by=self.user, title='blog test 1', content='blog test content item one')
        Blog.objects.create(posted_by=self.user, title='blog test 2', content='blog test content item two')
        Blog.objects.create(posted_by=self.user, title='blog test 3', content='blog test content item three')

        request = self.factory.get(reverse('home'), data={'search': 'one'})
        response = ListBlogView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'blog test 1') # this should appear in the search
        self.assertNotContains(response, 'blog test 2') # this should not appear the query
        self.assertNotContains(response, 'blog test 3') # this should not appear the query

    def test_blog_edit_authorized(self):
        """
        to test blog edit authorized by user
        """
        self.factory = RequestFactory()
        self.url = reverse('home')
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.client.force_login(self.user)
        test_blog = Blog.objects.create(posted_by=self.user, title='blog test 1', content='blog test content item one')
        edited_blog = {
            'title':'edited blog title',
            'content':'edited blog content'
        }
        # print("test_blog id", test_blog.id)
        response = self.client.post(f'/edit_blog/{test_blog.id}/', data=edited_blog)
        # print("response: ", response)
        edited_saved_blog = Blog.objects.get(id=test_blog.id)
        self.assertEqual(edited_saved_blog.title, edited_blog['title'])

    def test_blog_edit_unauthorized(self):
        """
        to test blog edit by unauthorized
        """
        self.factory = RequestFactory()
        self.url = reverse('home')
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.user_2 = User.objects.create_user(username="testuse_2", password="testpassword_2", is_staff=True)
        self.client.force_login(self.user_2)
        test_blog = Blog.objects.create(posted_by=self.user, title='blog test 1', content='blog test content item one')
        edited_blog = {
            'title':'edited blog title',
            'content':'edited blog content'
        }
        # print("test_blog id", test_blog.id)
        response = self.client.post(f'/edit_blog/{test_blog.id}/', data=edited_blog)
        # print("response: ", response)
        edited_saved_blog = Blog.objects.get(id=test_blog.id)
        self.assertNotEqual(edited_saved_blog.title, edited_blog['title'])


    def test_comment_delete_authorized(self):
        """
        to test comment deletion authorized
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.client.force_login(self.user)
        test_blog = Blog.objects.create(posted_by=self.user, title='blog test title', content='blog test content')

        test_comment = Comment.objects.create(posted_by=self.user, for_blog=test_blog, content='Test comment')
        self.client.get(f'/del_comment/{test_blog.pk}/{test_comment.pk}/')
        self.assertEqual(Comment.objects.count(), 0)


    def test_comment_delete_unauthorized(self):
        """
        to test comment deletion unauthorized
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_staff=True)
        self.user_2 = User.objects.create_user(username="testuse_2", password="testpassword_2", is_staff=True)
        self.client.force_login(self.user_2)
        test_blog = Blog.objects.create(posted_by=self.user, title='blog test title', content='blog test content')

        test_comment = Comment.objects.create(posted_by=self.user, for_blog=test_blog, content='Test comment')
        self.client.get(f'/del_comment/{test_blog.pk}/{test_comment.pk}/')
        self.assertEqual(Comment.objects.count(), 1) # the comment is not deleted since the user is not authorized(not the one that created the comment)
