import json5
from datetime import datetime

from django.db import DatabaseError
from django.utils import timezone

from e_logs.common.all_journals_app.models import CellGroup, Journal, Equipment
from e_logs.core.utils.webutils import localize


class VersionControl():
    def __init__(self):
        with open('resources/versions.jrncontrol', 'r') as f:
            self.versions = json5.load(f)

    def version_of(self, obj):
        if isinstance(obj, CellGroup):
            group = obj
            for version, time in self.versions[group.journal.plant.name][group.journal.name].items():
                date = group.end_time if group.journal.type == 'shift' else localize(group.date)
                # print(time['start'])
                # print(time['end'])
                if localize(datetime(*time['start'][:7])) < date <= localize(datetime(*time['end'][:7])):
                    return int(version)
        elif isinstance(obj, Journal):
            journal = obj
            return int([*self.versions[journal.plant.name][journal.name]][-1])

    def commit(self, journal):
        journal_entry = self.versions[journal.plant.name][journal.name]
        journal_version = self.version_of(journal)
        now_time = list(timezone.localtime().timetuple())
        journal_entry[str(journal_version)]['end'] = now_time
        journal_entry[str(journal_version + 1)] = {"start": now_time, "end": self.max_time()}
        self.__write()

        for group in journal.group.objects.filter(journal=journal):
            if not isinstance(group, Equipment):
                date = group.end_time if group.journal.type == 'shift' else localize(group.date)
                if date >= timezone.localtime():
                    group.version = group.version + 1
                    group.save()
            else:
                group.version = group.version + 1
                group.save()

    def add(self, journal):
        self.versions[journal.plant.name].pop(journal.name, None)  # if journal entry exists
        self.versions[journal.plant.name][journal.name] = {"1": {"start": self.min_time(), "end": self.max_time()}}
        self.__write()

    @staticmethod
    def min_time():
        return [1000, 1, 1, 0, 0]

    @staticmethod
    def max_time():
        return [9000, 12, 31, 0, 0, 0, 0]

    def __write(self):
        with open('resources/versions.jrncontrol', 'w') as f:
            data = json5.dumps(self.versions)
            f.write(data)
