import tempfile
from PIL import Image

from oscar.core.loading import get_model

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .factories.post import PostFactory
from .factories.category import CategoryFactory

Post = get_model('appblog', 'Post')
Category = get_model('appblog', 'Category')


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
        user = User.objects.create(username='post_test')
        user.set_password('post12345')
        user.save()
        self.post_factory = PostFactory(author=user)

    def test_response_status_code_blogspost_should_equal_200(self):
        self.login()
        response = self.client.get('/dashboard/blogs/post/')
        self.assertEqual(response.status_code, 200)

    def test_blog_post_have_not_queryset(self):
        self.login()
        response = self.client.get('/dashboard/blogs/post/')
        data_context = response.context['posts']    
        self.assertQuerysetEqual(data_context, ['<Post: {}>'.format(self.post_factory.title)])

    def test_search_blog_post_from_title_should_have_expected_data(self):
        self.login()

        response = self.client.get(
            '/dashboard/blogs/post/?title={}&author=&action=search'.format(self.post_factory.title))

        expected_data = ['<Post: {}>'.format(self.post_factory.title)]
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], expected_data)

    def test_search_blog_post_from_author_should_have_expected_data(self):
        self.login()

        response = self.client.get(
            '/dashboard/blogs/post/?title=&author={}&action=search'.format(self.post_factory.author))

        expected_data = ['<Post: {}>'.format(self.post_factory.title)]
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], expected_data)


class TestDashboardPostDetailCreateView(WebTestCase):

    def setUp(self):
        self.category_factory = CategoryFactory()
        self.url_post_create_detail_view = reverse('blog-dashboard:blog-post-create-detail')

    def test_response_status_code_blogspost_create_detail_should_equal_200(self):
        self.login()
        response_client = self.client.get(self.url_post_create_detail_view)
        self.assertEqual(response_client.status_code, 200)

    def test_create_data(self):
        self.login()
        data = {
            'title': 'Test create new post',
            'content': 'example content',
            'author': self.user.id,
            'excerpt': 'example excerpt',
            'post_date': '2018-03-12',
            'featured_image': self.create_image(),
            'categorygroup_set-TOTAL_FORMS': '2',
            'categorygroup_set-INITIAL_FORMS': '0',
            'categorygroup_set-MIN_NUM_FORMS': '1',
            'categorygroup_set-0-category': self.category_factory.id,
        }

        response = self.client.post(self.url_post_create_detail_view, data=data)
        self.assertEqual(response.status_code, 302)


class TestDashboardPostDetailUpdateView(WebTestCase):

    def setUp(self):
        self.post_factory = PostFactory()
        self.category_factory = CategoryFactory()
        self.url_post_detail_view = reverse(
            'blog-dashboard:blog-post-detail',
            kwargs={'id': self.post_factory.id}
        )

    def test_response_status_code_blogspost_detail_should_equal_200(self):
        self.login()
        response_client = self.client.get(self.url_post_detail_view)
        self.assertEqual(response_client.status_code, 200)

    def test_blogspost_detail_should_have_data_we_expect(self):
        self.login()
        response_client = self.client.get(self.url_post_detail_view)
        self.assertEqual(response_client.context['post'], self.post_factory)

    def test_update_data(self):
        self.login()
        data = {
            'title': 'Test Blog',
            'content': 'example content',
            'author': self.user.id,
            'excerpt': 'example excerpt',
            'post_date': '2018-03-12',
            'featured_image': self.create_image(),
            'categorygroup_set-TOTAL_FORMS': '2',
            'categorygroup_set-INITIAL_FORMS': '0',
            'categorygroup_set-MIN_NUM_FORMS': '1',
            'categorygroup_set-0-category': self.category_factory.id
        }

        response = self.client.post(self.url_post_detail_view, data=data)
        self.assertEqual(response.status_code, 302)

        expect_data = Post.objects.get(title=data['title'])
        self.assertEqual(expect_data.content, data['content'])
        self.assertEqual(expect_data.author, self.user)
        self.assertEqual(expect_data.excerpt, data['excerpt'])


class TestDashboardPostDetailDeleteView(WebTestCase):

    def test_delete_data(self):
        self.login()
        post_factory = PostFactory()

        url_post_delete_view = reverse(
            'blog-dashboard:blog-post-delete-detail',
            kwargs={'pk': post_factory.id}
        )
        response = self.client.post(url_post_delete_view)
        self.assertEqual(response.status_code, 302)


class TestDashboardCategoryListView(WebTestCase):

    def setUp(self):
        self.category_factory = CategoryFactory()
        self.url_category_list_view = reverse('blog-dashboard:blog-category-list')

    def test_response_status_code_category_list_view_should_equal_200(self):
        self.login()
        response = self.client.get(self.url_category_list_view)
        self.assertEqual(response.status_code, 200)

    def test_search_blog_category_from_name_should_have_expected_data(self):
        self.login()

        response = self.client.get(
            self.url_category_list_view + '?name={}&action=search'.format(self.category_factory.name))

        expected_data = ['<Category: {}>'.format(self.category_factory.name)]
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['categoires'], expected_data)


class TestDashboardCategoryCreateView(WebTestCase):

    def setUp(self):
        self.url_category_create_view = reverse('blog-dashboard:blog-category-detail-create')

    def test_response_status_code_category_create_view_should_equal_200(self):
        self.login()
        response = self.client.get(self.url_category_create_view)
        self.assertEqual(response.status_code, 200)

    def test_create_data(self):
        data = {
            'name': 'category name',
            'action': 'save'
        }
        response = self.client.post(self.url_category_create_view, data=data)
        self.assertEqual(response.status_code, 302)


class TestDashboardCategoryUpdateView(WebTestCase):

    def setUp(self):
        self.category_factory = CategoryFactory()
        self.url_category_update_view = reverse(
            'blog-dashboard:blog-category-detail-update', kwargs={'pk': self.category_factory.id})

    def test_response_status_code_category_update_view_should_equal_200(self):
        self.login()
        response = self.client.get(self.url_category_update_view)
        self.assertEqual(response.status_code, 200)

    def test_update_data(self):
        data = {
            'name': 'category name',
            'action': 'save'
        }
        response = self.client.post(self.url_category_update_view, data=data)
        self.assertEqual(response.status_code, 302)


class TestDashboardCategoryDeleteView(WebTestCase):

    def setUp(self):
        self.category_factory = CategoryFactory()
        self.url_category_delete_view = reverse(
            'blog-dashboard:blog-category-detail-delete', kwargs={'pk': self.category_factory.id})

    def test_response_status_code_category_delete_view_should_equal_200(self):
        self.login()
        response = self.client.get(self.url_category_delete_view)
        self.assertEqual(response.status_code, 200)

    def test_delete_data(self):
        response = self.client.post(self.url_category_delete_view)
        self.assertEqual(response.status_code, 302)
