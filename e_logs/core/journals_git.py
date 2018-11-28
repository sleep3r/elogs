import json5
from datetime import datetime

from django.utils import timezone

from e_logs.core.utils.webutils import localize


class VersionControl():
    def __init__(self):
        with open('resources/versions.jrncontrol') as f:
            self.versions = json5.load(f)

    def version_of(self, group):
        for version, time in self.versions[group.journal.plant.name][group.journal.name].items():
            date = group.end_time if group.journal.type == 'shift' else localize(group.date)
            if localize(datetime(*time['start'])) < date <= localize(datetime(*time['end'])):
                return int(version)
