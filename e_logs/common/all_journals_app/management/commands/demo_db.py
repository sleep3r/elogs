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
            help='Cleans db',
        )

        parser.add_argument(
            '--create',
            action="store_true",
            help='Creates db',
        )

        parser.add_argument(
            '--recreate',
            action="store_true",
            help='Recreates db',
        )

        parser.add_argument(
            '-frac',
            type=int,
            help='Number of fraction hists to create',
        )

        parser.add_argument(
            '-employee',
            action="store_true",
            help='Number of fraction hists to create',
        )

    def handle(self, *args, **options):
        df = DatabaseFiller()
        frac_num = options["frac"]
        add_employee = options["employee"]
        if options["clean"] or options["recreate"]:
            print("Cleaning db")
            df.clean_database()

        if options["create"] or options["recreate"]:
            print("Creating db")
            print("Adding permissions...")
            df.create_permissions_and_groups()
            print("Adding plants...")
            df.fill_plants()
            if add_employee:
                print("Adding Employees...")
                df.fill_employees()
            if frac_num:
                print("Filling fractional app...")
                df.fill_fractional_app(frac_num)

        print("Done!")
