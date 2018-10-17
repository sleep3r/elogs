import json
import os
import zipfile
from shutil import move, rmtree

import environ
from django.conf import settings

from e_logs.common.all_journals_app.models import Journal, Table, Field
from e_logs.core.models import Setting
from e_logs.core.utils.webutils import get_or_none
from errors import SemanticError


class JournalBuilder:
    def __init__(self, file, plant):
        env = environ.Env(DEBUG=(bool, False))
        required_version = env('CONSTRUCTOR_VERSION')
        print(file)
        self.file = zipfile.ZipFile(file)

        try:
            meta = json.loads(self.file.read(f'{file.name.split(".")[0]}/meta.json'))
        except:
            raise SemanticError(message='Ошибка структуры файла')

        if meta['version'] == float(required_version):
            self.plant = plant
            self.type = meta['type']
            self.name = meta['name']
            self.title = meta['title']
            self.tables = meta['tables']
        else:
            raise SemanticError(
                message=f"Некорректная версия, требуется не ниже v{required_version}")

    def create(self):
        journal_rel_dir = self.plant

        tables_path = settings.JOURNAL_TEMPLATES_DIR / journal_rel_dir

        new_journal = self.__create_journal(tables_path)

        for table in self.tables:
            new_table = self.__create_table(journal=new_journal, table=table)

            for field in table['fields']:
                new_field = self.__create_field(table=new_table, field=field)
                self.__set_field_settings(field=new_field, meta=field)

        self.__extract_tables(tables_path)

        self.__set_tables_order(journal=new_journal)

    def __create_journal(self, tables_path, rewrite=False):
        journal = get_or_none(Journal, name=self.name, plant=self.plant, type=self.type)

        if journal and rewrite:
            journal.delete()
        if os.path.exists(tables_path) and rewrite:
            rmtree(tables_path)

        if journal or os.path.exists(tables_path):
            raise SemanticError(message='Журнал с таким именем уже существует!')
        else:
            new_journal = Journal.objects.create(name=self.name, verbose_name=self.title,
                                                 plant=self.plant, type=self.type)

            return new_journal

    def __create_table(self, journal, table):
        table = get_or_none(Table, name=table['name'], journal=journal)

        if table:
            journal.delete()
            raise SemanticError(message=f'Две таблицы с одинаковым именем {table["name"]}!')
        else:
            new_table = Table.objects.create(name=table['name'],
                                             journal=journal,
                                             verbose_name=table.get('title', None))
            return new_table

    def __create_field(self, table, field: dict):
        field = get_or_none(Field, name=field['name'], table=table)

        if field:
            table.journal.delete()
            raise SemanticError(message=f'Две столбца с одинаковым именем {field["name"]}!')
        else:
            new_field = Field.objects.create(name=field.pop('name'),
                                             table=table,
                                             verbose_name=field.get('title', None),
                                             formula=field.pop('formula', ''))
            return new_field

    def __set_field_settings(self, field, meta):
        Setting.of(field)["field_description"] = meta

    def __extract_tables(self, tables_path):
        for table in self.file.infolist():
            if table.filename.endswith('.html'):
                table.filename = os.path.basename(table.filename)
                self.file.extract(table, tables_path)

    def __set_tables_order(self, journal):
        tables_list = []
        for table in sorted(self.tables, key=lambda t: t['order']):
            tables_list.append(f"tables/{self.plant.name}/{self.name}/{table.name}.html")
        Setting.of(journal)['tables_list'] = tables_list
