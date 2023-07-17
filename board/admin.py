from django.contrib import admin
from .models import Category, Ad, Reply
from modeltranslation.admin import TranslationAdmin


# @admin.site.register
# class CategoryAdmin(TranslationAdmin):
#     model = Category


admin.site.register(Category, TranslationAdmin)
admin.site.register(Ad)
admin.site.register(Reply)
