from oscar.core.loading import get_model, get_class

from django.forms.models import inlineformset_factory


Post = get_model('appblog', 'Post')
CategoryGroup = get_model('appblog', 'CategoryGroup')

CategoryGroupForm = get_class('appblog.dashboard.forms', 'CategoryGroupForm')

CategoryGroupFormSet = inlineformset_factory(
    Post, CategoryGroup, form=CategoryGroupForm, extra=2, min_num=1, can_delete=True)
