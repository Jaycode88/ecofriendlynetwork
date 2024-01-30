from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Favorite
from .forms import PostForm

class TestPostModel(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create a test post
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user
        )

    def test_post_str(self):
        # Test the string representation of the Post model
        self.assertEqual(str(self.post), 'Test Post')

class TestFavoriteModel(TestCase):
    def setUp(self):
        # Create a test user and test post as in TestPostModel
        self.user = User.objects.create_user(username='testuser2', password='12345')
        self.post = Post.objects.create(
            title='Another Test Post',
            content='Another Test Content',
            author=self.user
        )
        # Create a Favorite instance
        self.favorite = Favorite.objects.create(user=self.user)
        self.favorite.posts.add(self.post)

    def test_favorite_str(self):
        # Test the string representation of the Favorite model
        self.assertEqual(str(self.favorite), "testuser2's favorite posts")

class TestBlogViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser3', email='test3@test.com', password='testpassword')
        self.post = Post.objects.create(
            title='View Test Post',
            content='View Test Content',
            author=self.user
        )

    def test_blog_list_view(self):
        # Test the blog list view
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')
        self.assertIn('posts', response.context)

    def test_blog_detail_view(self):
        # Test the blog detail view
        response = self.client.get(reverse('blog_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_detail.html')
        self.assertIn('post', response.context)

    def test_add_post_view_with_superuser(self):
            # Create and login as a superuser
            superuser = User.objects.create_superuser('superuser', 'superuser@test.com', 'superpassword')
            self.client.login(username='superuser', password='superpassword')

            # Test GET request (accessing the add post form)
            response = self.client.get(reverse('add_post'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/add_post.html')

            # Test POST request (submitting the form to add a new post)
            response = self.client.post(reverse('add_post'), {
                'title': 'New Superuser Post',
                'content': 'Superuser post content',
                'author': superuser
            })
            self.assertEqual(Post.objects.count(), 2) 
            self.assertRedirects(response, reverse('blog_list'))

    def test_edit_post_view_with_superuser(self):
        # Create and login as a superuser
        superuser = User.objects.create_superuser('editsuperuser', 'editsuperuser@test.com', 'editpassword')
        self.client.login(username='editsuperuser', password='editpassword')

        # Create a post to edit
        post_to_edit = Post.objects.create(
            title='Editable Post',
            content='Editable content',
            author=superuser
        )

        # Test GET request (accessing the edit post form)
        response = self.client.get(reverse('edit_post', args=[post_to_edit.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/edit_post.html')

        # Test POST request (submitting the form to edit the post)
        response = self.client.post(reverse('edit_post', args=[post_to_edit.pk]), {
            'title': 'Updated Post Title',
            'content': 'Updated content'
        })
        post_to_edit.refresh_from_db()
        self.assertEqual(post_to_edit.title, 'Updated Post Title')
        self.assertRedirects(response, reverse('blog_detail', args=[post_to_edit.pk]))


    def test_delete_post_view_with_superuser(self):
        # Create and login as a superuser
        superuser = User.objects.create_superuser('deletesuperuser', 'deletesuperuser@test.com', 'deletepassword')
        self.client.login(username='deletesuperuser', password='deletepassword')

        # Create a post to delete
        post_to_delete = Post.objects.create(
            title='Deletable Post',
            content='Deletable content',
            author=superuser
        )

        # Test POST request for deleting the post
        response = self.client.post(reverse('delete_post', args=[post_to_delete.pk]))
        self.assertEqual(Post.objects.count(), 1)  # The post created in setUp still exists
        self.assertRedirects(response, reverse('blog_list'))

    def test_add_to_favorite_posts(self):
        # Test adding a post to favorite posts
        self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(reverse('add_to_favorite_posts', args=[self.post.pk]))
        self.assertTrue(self.post in Favorite.objects.get(user=self.user).posts.all())
        self.assertRedirects(response, reverse('blog_detail', args=[self.post.pk]))

    def test_favorite_posts_list_view(self):
        # Test the favorite posts list view
        self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(reverse('favorite_posts_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/favorite_posts_list.html')

    def test_remove_from_favorite_posts(self):
        # Test removing a post from favorite posts
        self.client.login(username='testuser3', password='testpassword')
        # First, add a post to favorites
        favorite, created = Favorite.objects.get_or_create(user=self.user)
        favorite.posts.add(self.post)
        # Now, test removing it
        response = self.client.post(reverse('remove_from_favorite_posts', args=[self.post.pk]))
        self.assertFalse(self.post in Favorite.objects.get(user=self.user).posts.all())
        self.assertRedirects(response, reverse('blog_list'))

class TestPostForm(TestCase):
    def test_post_form_valid(self):
        # Test the PostForm with valid data
        form = PostForm(data={'title': 'Test Title', 'content': 'Test content'})
        self.assertTrue(form.is_valid())

    def test_post_form_invalid(self):
        # Test the PostForm with invalid data
        form = PostForm(data={})
        self.assertFalse(form.is_valid())

