import json
from os import walk

from e_logs.common.all_journals_app.models import Plant, Journal


tables_paths = []

print('from e_logs.common.all_journals_app.models import Plant, Journal')
print('from e_logs.core.models import Setting')

print()
print()
print('def fill_tables_lists():\n')

print('    Setting.objects.bulk_create([')

for plant in Plant.objects.all():
    for journal in Journal.objects.filter(plant=plant):
        templates_dir = 'e_logs/common/all_journals_app/templates/tables/{}/{}'.format(plant.name, journal.name)
        tables_paths = []
        for (dirpath, dirnames, filenames) in walk(templates_dir):
            paths = []
            for f in filenames:
                paths.append('tables/{}/{}/{}'.format(plant.name, journal.name, f))
            tables_paths.extend(paths)
        print("""        Setting(\n            scope=Journal.objects.get(\n                plant=Plant.objects.get(name='{}'),\n                name='{}'\n            ),\n            name='tables_list',\n            value='{}'\n        ),""".format(plant.name, journal.name, json.dumps(tables_paths)))


print('    ])')
