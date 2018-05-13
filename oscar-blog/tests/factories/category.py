import factory

from oscar.core.loading import get_model


__all__ = ['CategoryFactory']


class CategoryFactory(factory.DjangoModelFactory):
    name = 'Test Category'

    class Meta:
        model = get_model('appblog', 'Category')
