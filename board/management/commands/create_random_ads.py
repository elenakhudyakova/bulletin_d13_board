import random
import string

from django.core.management.base import BaseCommand, CommandError
from accounts.models import User

from board.models import Ad, Category


class Command(BaseCommand):
    help = 'Создаёт случайно сгенерированные объявления'
    requires_migrations_checks = True
    alphabet = string.ascii_letters + string.digits + ' '

    def handle(self, *args, **options):
        random.seed()
        users = User.objects.filter(email_verified=True)
        num_users = users.count()
        ad_list = []
        for category in Category.objects.all():
            for i in range(20):
                ad_list.append(Ad(
                    author=users[random.randint(0, num_users-1)],
                    title=''.join([random.choice(self.alphabet) for _ in range(20)]),
                    content=''.join([random.choice(self.alphabet) for _ in range(500)]),
                    category=category,
                ))
        Ad.objects.bulk_create(ad_list)
