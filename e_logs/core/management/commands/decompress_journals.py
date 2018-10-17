import json
import os
import zipfile
from shutil import copytree, rmtree

from django.core.management.base import BaseCommand

from django.conf import settings

from journal_builder import JournalBuilder
from .database_filler import Journal


def decompress_journals():
    for plant_name in os.listdir(settings.JOURNALS_DIR):
        if os.path.isdir(settings.JOURNALS_DIR / plant_name):
            for file_name in os.listdir(settings.JOURNALS_DIR / plant_name):
                if "".endswith(f'.{settings.JOURNAL_EXTENSION}'):
                    JournalBuilder(settings.JOURNALS_DIR / plant_name / file_name, plant_name)


class Command(BaseCommand):
    def handle(self, *args, **options):
        decompress_journals()
