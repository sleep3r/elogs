from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from .DatabaseFiller import DatabaseFiller
from e_logs.core.models import Setting





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

    def handle(self, *args, **options):
        df = DatabaseFiller()
        df.reset_increment_counter('auth_group')
        frac_num = options["frac"]
        if options["clean"] or options["recreate"]:
            print("Cleaning db")
            df.clean_database()

        if options["create"] or options["recreate"]:
            print("Creating db")

            print("Adding permissions...")
            df.create_permissions_and_groups()

            print("Adding plants...")
            df.fill_plants()
            print("Adding journals...")
            df.fill_journals()
            print("Adding tables...")
            df.fill_tables()
            print("Adding fields...")
            df.fill_fields()

            print("Adding settings...")
            df.create_tables_lists()
            df.create_fields_descriptions()
            df.create_number_of_shifts()

            print("Adding Employees...")
            df.fill_employees()

            if frac_num:
                print("Filling fractional app...")
                df.fill_fractional_app(frac_num)

        print("Done!")
