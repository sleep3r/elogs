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
    def __init__(self, file, plant_name, type=None):
        env = environ.Env(DEBUG=(bool, False))
        required_version = env('CONSTRUCTOR_VERSION')
        self.file = zipfile.ZipFile(file)

        try:
            meta = json.loads(self.file.read('meta.json'))
        except:
            raise SemanticError(message='Ошибка структуры файла')

        if float(meta['version']) == float(required_version):
            if not type:
                self.type = meta['type']
            else:
                self.type = type
            self.plant = Plant.objects.get_or_create(name=plant_name)[0]
            self.name = meta['name']
            self.title = meta['title']
            self.tables = meta['tables']
        else:
            raise SemanticError(
                message=f"Некорректная версия, требуется не ниже v{required_version}")

    def create(self):
        journal_rel_dir = self.plant.name

        tables_path = settings.JOURNAL_TEMPLATES_DIR / journal_rel_dir / self.name

        new_journal = self.__create_journal(tables_path)

        for table in self.tables:
            new_table = self.__create_table(journal=new_journal, table_meta=table)

            for field in table['fields']:
                self.__create_field(table=new_table, field_meta=field)

        self.__extract_tables(tables_path)

        return new_journal

    def __create_journal(self, tables_path, rewrite=True):
        # plant = Plant.objects.get_or_create(name=self.plant)[0]
        journal = get_or_none(Journal, name=self.name, plant=self.plant)

        if rewrite==True:
            if journal:
                journal.delete()
                journal = None
            if os.path.exists(tables_path):
                rmtree(tables_path)

        if journal or os.path.exists(tables_path):
            raise SemanticError(message='Журнал с таким именем уже существует!')
        else:
            new_journal = Journal.objects.create(name=self.name, verbose_name=self.title,
                                                 plant=self.plant, type=self.type)

            return new_journal

    def __create_table(self, journal, table_meta):
        table = get_or_none(Table, name=table_meta['name'], journal=journal)

        if table:
            journal.delete()
            raise SemanticError(message=f'Две таблицы с одинаковым именем {table.name}!')
        else:
            new_table = Table.objects.create(name=table_meta['name'],
                                             journal=journal,
                                             verbose_name=table_meta.get('title', ''))
            return new_table

    def __create_field(self, table, field_meta: dict):
        field_name = field_meta.get("name", field_meta.get("field_name", None))
        if not field_name:
            raise SemanticError(message=f'В таблице {table} есть поле без имени!')
        field = get_or_none(Field, name=field_name, table=table)

        if field:
            print(field)
            table.journal.delete()
            raise SemanticError(message=f'Две столбца с одинаковым именем {field.name}!')
        else:
            new_field = Field.objects.create(name=field_name,
                                             table=table,
                                             type=field_meta.get('type', None),
                                             units=field_meta.get('units', None),
                                             verbose_name=field_meta.get('title', ''),
                                             formula=field_meta.pop('formula', ''))
            return new_field

    def __extract_tables(self, tables_path):
        for table in self.file.infolist():
            if table.filename.endswith('.html'):
                table.filename = os.path.basename(table.filename)
                self.file.extract(table, tables_path)
