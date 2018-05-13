from oscar.core.loading import get_model, get_class

from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect


Post = get_model('appblog', 'Post')
Category = get_model('appblog', 'Category')

PostDetailForm = get_class('appblog.dashboard.forms', 'PostForm')
PostSearchForm = get_class('appblog.dashboard.forms', 'PostSearchForm')
CategoryForm = get_class('appblog.dashboard.forms', 'CategoryForm')
CategorySearchForm = get_class('appblog.dashboard.forms', 'CategorySearchForm')

CategoryGroupFormSet = get_class('appblog.dashboard.formsets', 'CategoryGroupFormSet')


class BlogPostListView(generic.ListView):
    template_name = 'dashboard/blog-post.html'
    model = Post
    context_object_name = 'posts'
    search_form_class = PostSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form_class()
        return context

    def get_queryset(self):
        queryset = self.model.objects.all()
        queryset = self.apply_search(queryset)
        return queryset

    def apply_search(self, queryset):
        self.form = self.search_form_class(self.request.GET)
        if 'search' == self.request.GET.get('action'):
            if not self.form.is_valid():
                return queryset

            data = self.form.cleaned_data
            if data['title']:
                queryset = queryset.filter(title__icontains=data['title'])
            if data['author']:
                queryset = queryset.filter(author__username__icontains=data['author'])
        return queryset


class BlogPostDetailUpdateView(generic.UpdateView):
    template_name = 'dashboard/blog-post-detail.html'
    context_object_name = 'post'
    form_class = PostDetailForm
    category_formset_class = CategoryGroupFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_formset'] = self.category_formset_class(instance=self.object)
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['id'])

    def process_all_forms(self, form):
        formset = self.category_formset_class(self.request.POST, instance=self.object)
        print('form in view : ', formset.is_valid(), formset.errors)
        is_valid = form.is_valid() and formset.is_valid()
        if is_valid:
            return self.forms_valid(form, formset)
        else:
            return self.forms_invalid(form, formset)

    form_valid = form_invalid = process_all_forms

    def forms_valid(self, form, formset):
        self.object = form.save()
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, formset):
        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the errors below"))
        context = self.get_context_data(form=form)
        context['category_formset'] = formset
        return self.render_to_response(context)

    def get_success_url(self):
        messages.success(self.request, _('save success'))

        action = self.request.POST.get('action')
        if action == 'continue':
            url = reverse(
                'blog-dashboard:blog-post-detail', kwargs={"id": self.object.id})
        else:
            url = reverse('blog-dashboard:blog-post-list')
        return url


class BlogPostDetailCreateView(generic.CreateView):
    template_name = 'dashboard/blog-post-detail.html'
    model = Post
    context_object_name = 'post'
    form_class = PostDetailForm
    category_formset_class = CategoryGroupFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_formset'] = self.category_formset_class(instance=self.object)
        return context

    def process_all_forms(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
        formset = self.category_formset_class(self.request.POST, instance=self.object)
        is_valid = form.is_valid() and formset.is_valid()
        if is_valid:
            return self.forms_valid(form, formset)
        else:
            return self.forms_invalid(form, formset)

    form_valid = form_invalid = process_all_forms

    def forms_valid(self, form, formset):
        self.object = form.save()
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, formset):
        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the errors below"))
        context = self.get_context_data(form=form)
        context['category_formset'] = formset
        return self.render_to_response(context)

    def get_success_url(self):
        messages.success(self.request, _('Post created successfully'))

        action = self.request.POST.get('action')
        if action == 'continue':
            return reverse('blog-dashboard:blog-post-detail', kwargs={'id': self.object.id})
        else:
            return reverse('blog-dashboard:blog-post-list')


class BlogPostDetailDeleteView(generic.DeleteView):
    template_name = 'dashboard/blog-post-detail-delete.html'
    model = Post
    context_object_name = 'posts'

    def get_success_url(self):
        messages.success(self.request, _('Post deleted successfully'))
        return reverse('blog-dashboard:blog-post-list')


class BlogCategoryListView(generic.ListView):
    template_name = 'dashboard/blog-category.html'
    model = Category
    context_object_name = 'categoires'
    search_form_class = CategorySearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form_class()
        return context

    def get_queryset(self):
        queryset = self.model.objects.all()
        queryset = self.apply_search(queryset)
        return queryset

    def apply_search(self, queryset):
        self.form = self.search_form_class(self.request.GET)
        if 'search' == self.request.GET.get('action'):
            if not self.form.is_valid():
                return queryset

            data = self.form.cleaned_data
            if data['name']:
                queryset = queryset.filter(name__icontains=data['name'])
        return queryset


class BlogCategoryDetailCreateView(generic.CreateView):
    template_name = 'dashboard/blog-category-detail.html'
    model = Category
    context_object_name = 'category'
    form_class = CategoryForm

    def get_success_url(self):
        messages.success(self.request, _('Category created successfully'))

        action = self.request.POST.get('action')
        if action == 'continue':
            return reverse('blog-dashboard:blog-category-detail-update', kwargs={'pk': self.object.id})
        else:
            return reverse('blog-dashboard:blog-category-list')


class BlogCategoryDetailUpdateView(generic.UpdateView):
    template_name = 'dashboard/blog-category-detail.html'
    model = Category
    context_object_name = 'category'
    form_class = CategoryForm

    def get_object(self, queryset=None):
        return get_object_or_404(Category, pk=self.kwargs['pk'])

    def get_success_url(self):
        messages.success(self.request, _('Category created successfully'))

        action = self.request.POST.get('action')
        if action == 'continue':
            return reverse('blog-dashboard:blog-category-detail-update', kwargs={'pk': self.object.id})
        else:
            return reverse('blog-dashboard:blog-category-list')


class BlogCategoryDetailDeleteView(generic.DeleteView):
    template_name = 'dashboard/blog-category-detail-delete.html'
    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Deleted {}'.format(self.object.name)
        return context

    def get_success_url(self):
        messages.success(self.request, _('Category deleted successfully'))
        return reverse('blog-dashboard:blog-category-list')
