from django.core.management.base import BaseCommand

from e_logs.core.utils.loggers import stdout_logger
from .database_filler import DatabaseFiller


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
            stdout_logger.info("Cleaning db")
            df.clean_database()

        if options["create"] or options["recreate"]:
            stdout_logger.info("Creating db")

            stdout_logger.info("Creating superuser...")
            df.create_superuser()
            stdout_logger.info("Adding permissions...")
            df.create_permissions_and_groups()

            stdout_logger.info("Adding plants...")
            df.fill_plants()
            stdout_logger.info("Adding journals...")
            df.fill_journals()
            stdout_logger.info("Adding tables...")
            df.fill_tables()
            stdout_logger.info("Adding fields...")
            df.fill_fields()

            stdout_logger.info("Adding settings...")
            df.load_settings()
            df.create_tables_lists()
            df.create_fields_descriptions()
            df.create_number_of_shifts()

            stdout_logger.info("Adding Employees...")
            df.fill_employees()

            if frac_num:
                stdout_logger.info("Filling fractional app...")
                df.fill_fractional_app(frac_num)

            stdout_logger.info("Done!")
