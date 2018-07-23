from django.core.management.base import BaseCommand
from .DatabaseFiller import DatabaseFiller
from e_logs.common.all_journals_app.models import Setting, get_setting_value


# from leaching.express_anal_app.tables import command_to_process


# def command_to_process():
#     df = DatabaseFiller()
#     df.recreate_database()
#
#     # df.clean_database()
#     # a = get_densers_table()
#     # pprint(a)

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
        df.reset_increment_counter('auth_group')
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

            print("Adding settings...")
            df.create_settings()


            if add_employee:
                print("Adding Employees...")
                df.fill_employees()
            if frac_num:
                print("Filling fractional app...")
                df.fill_fractional_app(frac_num)

            # print(get_setting_value("shift_count", cell="kek"))
            # print(get_setting_value("shift_count", table="pekl"))
            # print(get_setting_value("shift_count", journal="concentrate_report"))
            # print(get_setting_value("shift_count", plant="furnace"))
            # print(get_setting_value("shift_count", journal="concentrat234e_report"))
            # print("------")
            # print(get_setting_value("background", cell="krel"))
            # print(get_setting_value("background", table="uchet"))
            # print(get_setting_value("background", journal="concentrat234e_report"))
            # print(get_setting_value("background", plant="prekl"))
            # print("------")
            # # print(get_setting_value("govno"))
            # print(get_setting_value("test", cell="pr"))
            # print(get_setting_value("test", table="toble"))
            # print(get_setting_value("test", plant="prekl"))



        print("Done!")
