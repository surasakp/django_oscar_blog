from oscar.core.compat import AUTH_USER_MODEL

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
# Create your models here.


class Timestamp(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractCategory(Timestamp):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @property
    def get_number_posts(self):
        return AbstractCategoryGroup.objects.filter(category__name=self.name).count()


class AbstractPost(Timestamp):

    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    featured_image = models.ImageField(_("Featured Image"), upload_to=settings.OSCAR_IMAGE_FOLDER)
    post_date = models.DateField(default=timezone.now)
    author = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    category = models.ManyToManyField(
        AbstractCategory, blank=True, through='AbstractCategoryGroup', verbose_name=_("Category"))
    excerpt = models.TextField(blank=True)

    def __str__(self):
        return self.title


class AbstractCategoryGroup(Timestamp):
    post = models.ForeignKey(AbstractPost, on_delete=models.CASCADE)
    category = models.ForeignKey(AbstractCategory, on_delete=models.CASCADE)
    group = models.CharField(max_length=100)

    def __str__(self):
        return '{}-{}'.format(self.post, self.category)
