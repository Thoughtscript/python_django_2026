from django.core.management.base import BaseCommand
from djangoexample.models import Example, SubExample

class Command(BaseCommand):
    help = "Initialize data in DB"

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('Populating DB data ... ')
        
        example_one = Example()
        example_one.name = "example_one"
        example_one.save()

        example_two = Example()
        example_two.name = "example_two"
        example_two.save()

        example_three = Example()
        example_three.name = "example_three"
        example_three.save()

        sub_example_one = SubExample()
        sub_example_one.name = "sub_example_one"
        sub_example_one.example = example_one
        sub_example_one.save()

        sub_example_two = SubExample()
        sub_example_two.name = "sub_example_two"
        sub_example_two.example = example_two
        sub_example_two.save()

        sub_example_three = SubExample()
        sub_example_three.name = "sub_example_three"
        sub_example_three.example = example_three
        sub_example_three.save()

        self.stdout.write('Seeding Complete!')
