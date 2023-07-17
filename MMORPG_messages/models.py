from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Post(models.Model):
    TYPES = [
        ('01', 'Танки'),
        ('02', 'Хилы'),
        ('03', 'ДД'),
        ('04', 'Торговцы'),
        ('05', 'Гилдмастеры'),
        ('06', 'Квестгиверы'),
        ('07', 'Кузнецы'),
        ('08', 'Кожевники'),
        ('09', 'Зельевары'),
        ('10', 'Мастера заклинаний')
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=2, choices=TYPES, default='1')
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(blank=True, null=True)

    # def __str__(self):
    #     return f'{self.id}: {self.author.username}: {self.creation}: ' \
    #            f'{self.category}: {self.title}: {self.content[:30]}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    approved = models.BooleanField(default=False)

