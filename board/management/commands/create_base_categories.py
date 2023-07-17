from django.core.management.base import BaseCommand, CommandError
from board.models import Category


class Command(BaseCommand):
    help = 'Создаёт базовые категории'
    requires_migrations_checks = True
    names = {
        'Танки': 'Tanks',
        'Хилы': 'Healers',
        'ДД': 'DD',
        'Торговцы': 'Merchants',
        'Гилдмастеры': 'Guildmasters',
        'Квестгиверы': 'Questgivers',
        'Кузнецы': 'Blacksmiths',
        'Кожевники': 'Leatherworkers',
        'Зельевары': 'Potion makers',
        'Мастера заклинаний': 'Spell masters',
    }

    def handle(self, *args, **options):
        existing_categories = Category.objects.filter(name__in=self.names).values_list('name', flat=True)
        categories = Category.objects.bulk_create([Category(name=name_ru, name_en_us=name_en)
                                                   for name_ru, name_en in self.names.items()
                                                   if name_ru not in existing_categories])
        if categories:
            self.stdout.write(f"Созданы категории: {', '.join(map(str, categories))}")
