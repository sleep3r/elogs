from django.core.management.base import BaseCommand
from .DatabaseFiller import DatabaseFiller


# from leaching.express_anal_app.tables import command_to_process


def command_to_process():
    df = DatabaseFiller()
    df.recreate_database()

    # df.clean_database()
    a = get_densers_table()
    pprint(a)

class Command(BaseCommand):
    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            '--clean',
            action="store_true",
            dest='clean',
            help='Cleans db',
        )

        parser.add_argument(
            '--created',
            action="store_true",
            dest='create',
            help='Creates db',
        )


    def handle_noargs(self, **options):
        print("Recreating db")
        df = DatabaseFiller()
        df.recreate_database()

    def handle(self, *args, **options):
        df = DatabaseFiller()

        if options["clean"]:
            print("Cleaning db")
            df.clean_database()

        if options["create"]:
            print("Creating db")
            df.create_demo_database()

        # command_to_process()
