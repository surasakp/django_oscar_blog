from django.test import TestCase, Client
from django.contrib.auth.models import User
from .factories.post import PostFactory
from django.core.urlresolvers import reverse
from oscar.core.loading import get_class, get_model

import tempfile
from PIL import Image

Post = get_model('web_blog', 'Post')


class WebTestCase(TestCase):
    username = 'admin'
    password = 'top12345'

    def login(self):
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        self.client = Client()
        self.client.login(
            username=self.username,
            password=self.password
        )

    def create_image(self):
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')

        return open(f.name, mode='rb')


class TestDashboardPostView(WebTestCase):

    def setUp(self):
        self.login()
        self.postFactory = PostFactory()
        self.response = self.client.get('/dashboard/blogs/post/')

    def test_response_status_code_blogspost_should_equql_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_queryset(self):
        data_context = self.response.context['posts']
        self.assertQuerysetEqual(data_context, ['<Post: title : test_post>'])


class TestDashboardPostDetailCreateView(WebTestCase):

    def setUp(self):
        self.login()
        self.url_post_create_detail_view = reverse(
            'blog-dashboard:blog-post-create-detail')
        self.form = get_class('web_blog.dashboard.views', 'BlogPostDetailCreateView')

    def test_response_status_code_blogspost_create_detail_should_equql_200(self):
        response_client = self.client.get(self.url_post_create_detail_view)
        self.assertEqual(response_client.status_code, 200)

    def test_create_data(self):

        data = {
            'title': 'Test create new post',
            'content': 'example content',
            'authour': self.user.id,
            'excerpt': 'example excerpt',
            'post_date': '2018-03-12',
            'featured_image': self.create_image()
        }
        self.client.post(self.url_post_create_detail_view, data)
        expect_data = Post.objects.get(title=data['title'])
        self.assertEqual(expect_data.title, data['title'])
        # self.assertEqual(expect_data.featured_image, data['featured_image'].name)



class TestDashboardPostDetailUpdateView(WebTestCase):

    def setUp(self):
        self.login()
        self.postFactory = PostFactory()
        self.url_post_detail_view = reverse(
            'blog-dashboard:blog-post-detail',
            kwargs={'post_id': self.postFactory.id}
        )
        self.response_client = self.client.get(self.url_post_detail_view)
        self.form = get_class('web_blog.dashboard.forms', 'PostForm')

    def test_response_status_code_blogspost_detail_should_equql_200(self):
        self.assertEqual(self.response_client.status_code, 200)

    def test_blogspost_detail_should_have_data_we_expect(self):
        self.assertEqual(self.response_client.context['post'], self.postFactory)

    def test_update_data(self):

        data = {
            'title': 'Test Blog',
            'content': 'example content',
            'authour': self.user.id,
            'excerpt': 'example excerpt',
            'post_date': '2018-03-12',
            'featured_image': self.create_image()
        }
        response = self.client.post(self.url_post_detail_view, data=data, follow=True)
        expect_data = Post.objects.get(title=data['title'])
        print('image : ', expect_data.featured_image, response.status_code)
        self.assertEqual(expect_data.title, data['title'])