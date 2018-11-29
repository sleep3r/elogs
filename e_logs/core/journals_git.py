import json5
from datetime import datetime

from django.utils import timezone

from e_logs.core.utils.webutils import localize


class VersionControl():
    def __init__(self):
        with open('resources/versions.jrncontrol', 'r') as f:
            self.versions = json5.load(f)

    def version_of(self, group):
        for version, time in self.versions[group.journal.plant.name][group.journal.name].items():
            date = group.end_time if group.journal.type == 'shift' else localize(group.date)
            if localize(datetime(*time['start'])) < date <= localize(datetime(*time['end'])):
                return int(version)

    def commit(self):
        pass

    def add(self, journal):
        self.versions[journal.plant.name].pop(journal.name, None) # if journal entry exists
        self.versions[journal.plant.name][journal.name] = {"1": {"start": self.min_time(), "end": self.max_time()}}
        with open('resources/versions.jrncontrol', 'w') as f:
            data = json5.dumps(self.versions)
            f.write(data)

    @staticmethod
    def min_time():
        return [1000, 1, 1, 0, 0]

    @staticmethod
    def max_time():
        return [9000, 12, 31, 0, 0, 0, 0]
