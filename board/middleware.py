from django.core.cache import cache

from .models import Category


class CategoriesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        categories = cache.get('categories', None)

        if not categories:
            categories = {obj.pk: obj for obj in Category.objects.all()}
            cache.set('categories', categories)

        response.context_data['categories'] = categories
        return response
