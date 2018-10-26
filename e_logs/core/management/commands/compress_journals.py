import json
import os
from shutil import copytree, rmtree

from django.core.management.base import BaseCommand
from django.conf import settings

from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.loggers import err_logger
from e_logs.core.utils.webutils import zipdir
from .database_filler import Journal


def compress_journal(journal: Journal):
    jd = DeepDict()  # creating metadata json
    jd.version = '0.1'
    jd.name = journal.name
    jd.title = journal.verbose_name
    jd.type = journal.type

    jd.tables = []
    for t in journal.tables.all():
        td = DeepDict()
        td.name = t.name
        td.title = t.verbose_name

        td.fields = []
        for f in t.fields.all():
            fd = DeepDict()
            fd.name = f.name
            fd.formula = f.formula
            try:
                fd.type = f.type
                if fd.type == 'number':
                    fd.units = f.units
                elif fd.type == 'datalist':
                    fd.options = f.options
            except Exception as e:
                err_logger.warning(f'{(jd.name, td.name, fd.name)} failed with {e}')
                err_logger.info(f'field_description='
                                f'{f.settings.get(name="field_description").val()}')

            td.fields += [fd.get_dict()]

        jd.tables += [td.get_dict()]

    meta_data = json.dumps(jd.get_dict())  # creating paths for everything

    templates_dir = os.path.join('templates', 'tables', journal.plant.name, journal.name)
    temp_zip_dir = os.path.join('resources', 'temp', 'journals', journal.plant.name, journal.name)
    temp_zip_templates_dir = os.path.join(temp_zip_dir, 'templates')

    real_zip_path = os.path.join('resources', 'journals', journal.plant.name)
    real_zip_filename = os.path.join(real_zip_path, journal.name + f'.{settings.JOURNAL_EXTENSION}')

    meta_file = os.path.join(temp_zip_dir, 'meta.json')

    os.makedirs(temp_zip_dir, exist_ok=True)  # creating folder with zip archives
    rmtree(temp_zip_templates_dir, ignore_errors=True)
    copytree(templates_dir, temp_zip_templates_dir)
    with open(meta_file, 'w') as meta:
        meta.write(meta_data)

    rmtree(real_zip_filename, ignore_errors=True)  # creating zip archive
    os.makedirs(real_zip_path, exist_ok=True)
    zipdir(temp_zip_dir, real_zip_filename)

    rmtree(temp_zip_dir, ignore_errors=True)  # cleaning up temp folder


class Command(BaseCommand):
    def handle(self, *args, **options):
        for j in Journal.objects.prefetch_related('tables', 'tables__fields').all():
            compress_journal(j)
