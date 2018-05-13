import factory
import datetime

from oscar.core.loading import get_model


__all__ = ['PostFactory']


class PostFactory(factory.DjangoModelFactory):
    title = 'test_post'
    content = 'test_content'
    post_date = datetime.datetime.now()
    excerpt = 'test_excerpt'
    author = None

    class Meta:
        model = get_model('appblog', 'Post')
