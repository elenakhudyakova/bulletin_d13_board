from django.core.cache import cache
from django.db import models
from django.contrib.auth.backends import UserModel
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField


class Ad(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=256)
    content = RichTextUploadingField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name=_('active'))

    def __str__(self):
        return f"{self.author}: {self.title}"

    def get_absolute_url(self):
        return reverse('board_ad_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _('ad')
        verbose_name_plural = _('ads')


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def get_random_ads(self):
        return Ad.objects.filter(category=self, is_active=True).select_related('author') \
            .order_by('?').defer('content', 'author__password')[:3]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('categories')

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Reply(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name=_('replies'))
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} -> ({self.ad})"

    class Meta:
        verbose_name = _('reply')
        verbose_name_plural = _('replies')
