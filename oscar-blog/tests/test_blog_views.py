import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .factories.blogs import (CategoryFactory, PostFactory, CategoryGroupFactory)
from appblog.models import (Post, Category)
from .util import Util

util = Util()


class TestBlogPostView(TestCase):

    def setUp(self):
        upload_file = util.create_image()

        self.url_blog_post_view = reverse('appblog:posts-index-view')
        self.category_factory = CategoryFactory()
        self.post_factory = PostFactory(featured_image=SimpleUploadedFile(upload_file.name, upload_file.read()))
        CategoryGroupFactory(category=self.category_factory, post=self.post_factory)

        self.future_post_factory = PostFactory(
            title='future post',
            featured_image=SimpleUploadedFile(upload_file.name, upload_file.read()),
            post_date=datetime.date(2040, 10, 1))
        CategoryGroupFactory(category=self.category_factory, post=self.future_post_factory)

        self.category_use_to_future_post_factory = CategoryFactory(name='future category')
        CategoryGroupFactory(category=self.category_use_to_future_post_factory, post=self.future_post_factory)

    def test_blog_post_view_should_have_response_code_equal_200(self):
        response = self.client.get(self.url_blog_post_view)
        self.assertEqual(response.status_code, 200)

    def test_blog_post_view_should_have_data_expected(self):
        response = self.client.get(self.url_blog_post_view)
        self.assertEqual(response.status_code, 200)

        post_set = Post.objects.all().filter(post_date__lte=datetime.date.today())
        data_expected = []
        for post in post_set:
            data_expected.append('<Post: {}>'.format(post))

        self.assertQuerysetEqual(response.context['posts'], data_expected)

        category_set = Category.objects.all().filter(abstractpost__post_date__lte=datetime.date.today())
        expected_category_set = []
        for category in category_set:
            expected_category_set.append('<Category: {}>'.format(category))

        self.assertQuerysetEqual(response.context['categories'], expected_category_set)

    def test_blog_post_view_search_post_should_have_data_expected(self):
        response = self.client.get(
            self.url_blog_post_view + '?search={}&action=search'.format(self.post_factory.title))

        self.assertEqual(response.status_code, 200)

        post_set = Post.objects.all().filter(
            post_date__lte=datetime.date.today(), title__icontains=self.post_factory.title)
        data_expected = []
        for post in post_set:
            data_expected.append('<Post: {}>'.format(post))

        self.assertQuerysetEqual(response.context['posts'], data_expected)

    def test_blog_post_view_search_invalid_post_should_have_no_data(self):
        response = self.client.get(
            self.url_blog_post_view + '?search={}&action=search'.format('invalid post'))

        self.assertEqual(response.status_code, 200)

        queryset_post = []
        self.assertQuerysetEqual(response.context['posts'], queryset_post)


class TestCategoryView(TestCase):

    def setUp(self):
        upload_file = util.create_image()

        self.category_factory = CategoryFactory()
        self.post_factory = PostFactory(featured_image=SimpleUploadedFile(upload_file.name, upload_file.read()))
        CategoryGroupFactory(category=self.category_factory, post=self.post_factory)

        self.future_post_factory = PostFactory(
            title='future post',
            featured_image=SimpleUploadedFile(upload_file.name, upload_file.read()),
            post_date=datetime.date(2040, 10, 1))

        CategoryGroupFactory(category=self.category_factory, post=self.future_post_factory)

        self.url_category_view = reverse('appblog:category-view', kwargs={'slug': self.category_factory.slug})

        self.category_use_to_future_post_factory = CategoryFactory(name='future category')
        CategoryGroupFactory(category=self.category_use_to_future_post_factory, post=self.future_post_factory)

    def test_category_view_should_have_response_code_equal_200(self):
        response = self.client.get(self.url_category_view)
        self.assertEqual(response.status_code, 200)

    def test_category_view_should_have_data_expected(self):
        response = self.client.get(self.url_category_view)
        self.assertEqual(response.status_code, 200)

        post_set = Post.objects.all().filter(
            post_date__lte=datetime.date.today(), category__category__slug=self.category_factory.slug)
        expected_post_set = []
        for post in post_set:
            expected_post_set.append('<Post: {}>'.format(post))

        self.assertQuerysetEqual(response.context['posts'], expected_post_set)

        category_set = Category.objects.all().filter(abstractpost__post_date__lte=datetime.date.today())
        expected_category_set = []
        for category in category_set:
            expected_category_set.append('<Category: {}>'.format(category))

        self.assertQuerysetEqual(response.context['categories'], expected_category_set)

    def test_category_view_with_post_not_publish_should_not_found_category(self):
        url_category_view_future_post = reverse(
            'appblog:category-view', kwargs={'slug': self.category_use_to_future_post_factory.slug}
        )
        response = self.client.get(url_category_view_future_post)
        self.assertEqual(response.status_code, 200)

        expected_post_set = []

        self.assertQuerysetEqual(response.context['posts'], expected_post_set)

        category_set = Category.objects.all().filter(abstractpost__post_date__lte=datetime.date.today())
        expected_category_set = []
        for category in category_set:
            expected_category_set.append('<Category: {}>'.format(category))

        self.assertQuerysetEqual(response.context['categories'], expected_category_set)


class TestPostDetailView(TestCase):

    def setUp(self):
        upload_file = util.create_image()

        self.category_factory = CategoryFactory()
        self.post_factory = PostFactory(featured_image=SimpleUploadedFile(upload_file.name, upload_file.read()))
        CategoryGroupFactory(category=self.category_factory, post=self.post_factory)

        self.url_post_detail_view = reverse('appblog:post-detail-view', kwargs={'slug': self.post_factory.slug})

        self.future_post_factory = PostFactory(
            title='future post',
            featured_image=SimpleUploadedFile(upload_file.name, upload_file.read()),
            post_date=datetime.date(2040, 10, 1))

        CategoryGroupFactory(category=self.category_factory, post=self.future_post_factory)

    def test_post_detail_view_should_have_response_code_equal_200(self):
        response = self.client.get(self.url_post_detail_view)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_should_have_data_expected(self):
        response = self.client.get(self.url_post_detail_view)
        self.assertEqual(response.status_code, 200)

        content = response.context['post']
        data_expected = Post.objects.get(
            post_date__lte=datetime.date.today(), slug=self.post_factory.slug)
        self.assertEqual(content.title, data_expected.title)
        self.assertEqual(content.content, data_expected.content)
        self.assertEqual(content.excerpt, data_expected.excerpt)
        self.assertEqual(content.id, data_expected.id)

        category_set = Category.objects.all().filter(abstractpost__post_date__lte=datetime.date.today())
        expected_category_set = []
        for category in category_set:
            expected_category_set.append('<Category: {}>'.format(category))

        self.assertQuerysetEqual(response.context['categories'], expected_category_set)

    def test_post_detail_view_with_post_not_publish_should_not_found_post(self):
        url_post_detail_future_post = reverse(
            'appblog:post-detail-view', kwargs={'slug': self.future_post_factory.slug})

        response = self.client.get(url_post_detail_future_post)
        self.assertEqual(response.status_code, 200)

        self.assertTrue('post' not in response.context)

        category_set = Category.objects.all().filter(abstractpost__post_date__lte=datetime.date.today())
        expected_category_set = []
        for category in category_set:
            expected_category_set.append('<Category: {}>'.format(category))

        self.assertQuerysetEqual(response.context['categories'], expected_category_set)        
