import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as models_reviews
from places import models as models_places
from users import models as models_users


class Command(BaseCommand):
    help = "This command created many reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many reviews do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = models_users.User.objects.all()
        places = models_places.Place.objects.all()
        seeder.add_entity(
            models_reviews.Review,
            number,
            {
                "safety": lambda x: random.randint(0, 5),
                "accuracy": lambda x: random.randint(0, 5),
                "communication": lambda x: random.randint(0, 5),
                "location": lambda x: random.randint(0, 5),
                "value": lambda x: random.randint(0, 5),
                "place": lambda x: random.choice(places),
                "user": lambda x: random.choice(users),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reivews created!"))
