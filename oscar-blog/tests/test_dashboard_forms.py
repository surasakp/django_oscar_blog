from django.test import TestCase
from oscar.core.loading import get_model, get_class


Post = get_model('appblog', 'Post')
PostForm = get_class('appblog.dashboard.forms', 'PostForm')
Category = get_model('appblog', 'Category')
CategoryGroup = get_model('appblog', 'CategoryGroup')

CategoryGroupForm = get_class('appblog.dashboard.forms', 'CategoryGroupForm')
PostSearchForm = get_class('appblog.dashboard.forms', 'PostSearchForm')
CategoryForm = get_class('appblog.dashboard.forms', 'CategoryForm')
CategorySearchForm = get_class('appblog.dashboard.forms', 'CategorySearchForm')

CategoryGroupFormSet = get_class('appblog.dashboard.formsets', 'CategoryGroupFormSet')


class TestDashboardPostForm(TestCase):
    def setUp(self):
        self.form = PostForm

    def test_form_model_should_equal_Post(self):
        self.assertEquals(self.form.Meta.model, Post)

    def test_should_have_fields_that_we_expect(self):
        expected_fields = ['title', 'content', 'featured_image', 'post_date', 'author', 'excerpt']
        self.assertEquals(expected_fields, self.form.Meta.fields)

    def test_required_fields_have_not_data(self):
        data = {}

        form = self.form(data=data)
        self.assertFalse(form.is_valid())

        expected_errors = {
            'title': ['This field is required.'],
            'featured_image': ['This field is required.'],
            'post_date': ['This field is required.'],
        }

        self.assertDictEqual(form.errors, expected_errors)


class TestDashboardCategoryGroupForm(TestCase):
    def setUp(self):
        self.form = CategoryGroupForm

    def test_form_model_should_equal_CategoryGroup(self):
        self.assertEquals(self.form.Meta.model, CategoryGroup)

    def test_form_fields_should_have_expected_fields(self):
        expected_fields = ['category', 'post']
        self.assertEqual(self.form.Meta.fields, expected_fields)


class TestDashboardCategoryGroupFormSet(TestCase):
    def setUp(self):
        self.formset = CategoryGroupFormSet

    def test_formset_should_have_canable_delete(self):
        self.assertTrue(self.formset.can_delete)

    def test_formset_model_should_equal_CategoryGroup(self):
        self.assertEquals(self.formset.form.Meta.model, CategoryGroup)

    def test_formset_should_have_expected_fields(self):
        expected_fields = ['category', 'post']
        self.assertEqual(self.formset.form.Meta.fields, expected_fields)

    def test_formset_required_fields_have_not_data(self):

        data = {
            'categorygroup_set-TOTAL_FORMS': '2',
            'categorygroup_set-INITIAL_FORMS': '0',
            'categorygroup_set-MIN_NUM_FORMS': '1',
        }
        forms = CategoryGroupFormSet(data=data)
        self.assertFalse(forms.is_valid())

        required_fields = [{'category': ['This field is required.']}, {}]
        self.assertEqual(forms.errors, required_fields)

    def test_formset_set_wrong_data_should_have_error_available_choices(self):

        data = {
            'categorygroup_set-TOTAL_FORMS': '2',
            'categorygroup_set-INITIAL_FORMS': '0',
            'categorygroup_set-MIN_NUM_FORMS': '1',
            'categorygroup_set-0-category': 1
        }
        forms = CategoryGroupFormSet(data=data)
        self.assertFalse(forms.is_valid())

        required_fields = [
            {'category': ['Select a valid choice. That choice is not one of the available choices.']},
            {}]
        self.assertEqual(forms.errors, required_fields)

    def test_formset_selected_choice_should_have_choice_that_we_selected(self):

        category = Category.objects.create(name='Test Category1')
        data = {
            'categorygroup_set-TOTAL_FORMS': '2',
            'categorygroup_set-INITIAL_FORMS': '0',
            'categorygroup_set-MIN_NUM_FORMS': '1',
            'categorygroup_set-0-category': category.id
        }
        forms = CategoryGroupFormSet(data=data)
        self.assertTrue(forms.is_valid())

        required_fields = [{}, {}]
        self.assertEqual(forms.errors, required_fields)


class TestDashboardPostSearchForm(TestCase):

    def setUp(self):
        self.form = PostSearchForm

    def test_should_have_fields_that_we_expect(self):
        expected_fields = ['title', 'author']
        self.assertEquals(expected_fields, self.form.Meta.fields)

    def test_should_have_data_that_we_input(self):
        data = {
            'title': 'test',
            'author': 'admin'
        }
        form = self.form(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.data['title'], data['title'])
        self.assertEqual(form.data['author'], data['author'])

    def test_should_have_not_required_fields_when_no_data(self):
        data = {
            'title': '',
            'author': ''
        }
        form = self.form(data=data)
        self.assertTrue(form.is_valid())
        required_message = {}
        self.assertEqual(form.errors, required_message)


class TestDashboardCategoryForm(TestCase):

    def setUp(self):
        self.form = CategoryForm

    def test_should_have_fields_that_we_expect(self):
        expected_fields = ['name']
        self.assertEqual(self.form.Meta.fields, expected_fields)

    def test_should_have_not_required_fields_when_no_data(self):
        data = {
            'name': ''
        }
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        required_message = {'name': ['This field is required.']}
        self.assertEqual(form.errors, required_message)


class TestDashboardCategorySearchForm(TestCase):

    def setUp(self):
        self.form = CategorySearchForm

    def test_should_have_fields_that_we_expect(self):
        expected_fields = ['name']
        self.assertEqual(self.form.Meta.fields, expected_fields)

    def test_should_have_not_required_fields_when_no_data(self):
        data = {
            'name': ''
        }
        form = self.form(data)
        self.assertTrue(form.is_valid())
        required_message = {}
        self.assertEqual(form.errors, required_message)
