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
    templates_dir = os.path.join('templates', 'tables', journal.plant.name, journal.name)

    real_journal_path = os.path.join('resources', 'journals', journal.plant.name)
    real_journal_filename = os.path.join(real_journal_path, journal.name + f'.{settings.JOURNAL_EXTENSION}')

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
            fd.title = f.verbose_name
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

        template_filename = os.path.join(templates_dir, t.name + '.html')
        with open(template_filename) as template_file:
            td.html = template_file.read()

        jd.tables += [td.get_dict()]

    meta_data = json.dumps(jd.get_dict(), indent=4, ensure_ascii=False)

    with open(real_journal_filename, 'w') as meta:
        meta.write(meta_data)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for j in Journal.objects.prefetch_related('tables', 'tables__fields').all():
            compress_journal(j)
