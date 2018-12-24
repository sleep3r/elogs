import json
import os
import zipfile
from shutil import move, rmtree

import environ
from django.conf import settings

from e_logs.common.all_journals_app.models import Journal, Table, Field, Plant
from e_logs.core.models import Setting
from e_logs.core.utils.errors import SemanticError
from e_logs.core.utils.webutils import get_or_none


# noinspection PyMethodMayBeStatic
class JournalBuilder:
    def __init__(self, file, plant_name, version, type=None):
        env = environ.Env(DEBUG=(bool, False))
        required_version = env('CONSTRUCTOR_VERSION')

        try:
            with open(file, 'r') as f_in:
                meta = json.loads(f_in.read())
        except:
            raise SemanticError(message='Ошибка структуры файла')

        if float(meta['version']) == float(required_version):
            if not type:
                self.type = meta['type']
            else:
                self.type = type
                with open(file, 'w') as f_in:
                    meta['type'] = type
                    json.dump(meta, f_in)

            self.plant = Plant.objects.get_or_create(name=plant_name)[0]
            self.name = meta['name']
            self.title = meta['title']
            self.tables = meta['tables']
            self.version = version
        else:
            raise SemanticError(
                message=f"Некорректная версия, требуется не ниже v{required_version}")

    def create(self):
        new_journal = self.__create_journal()

        for table in self.tables:
            new_table = self.__create_table(journal=new_journal, table_meta=table)

            for field in table['fields']:
                self.__create_field(table=new_table, field_meta=field)

        self.extract_tables()

        return new_journal

    def extract_tables(self):
        tables_path = settings.JOURNAL_TEMPLATES_DIR / self.plant.name / self.name /  f'v{self.version}'

        for table in self.tables:
            template_filename = os.path.join(tables_path, table['name'] + '.html')
            os.makedirs(os.path.dirname(template_filename), exist_ok=True)

            with open(template_filename, 'w') as temp_file:
                temp_file.write(table['html'])

    def __create_journal(self):
        journal, created = Journal.objects.get_or_create(name=self.name, verbose_name=self.title,
                                                         plant=self.plant, type=self.type)
        return journal

    def __create_table(self, journal, table_meta):
        table, created = Table.objects.get_or_create(name=table_meta['name'],
                                                     journal=journal,
                                                     verbose_name=table_meta.get('title', ''))
        return table

    def __create_field(self, table, field_meta: dict):
        field, created = Field.objects.get_or_create(name=field_meta.get("name", None),
                                                     table=table,
                                                     type=field_meta.get('type', None),
                                                     units=field_meta.get('units', None),
                                                     verbose_name=field_meta.get('title', ''),
                                                     formula=field_meta.pop('formula', ''))
        return field
