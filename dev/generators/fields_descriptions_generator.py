import ast

from e_logs.common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
from e_logs.common.all_journals_app.fields_descriptions.fields_classes import *
from e_logs.common.all_journals_app.models import Plant, Journal, Table, Field


print('import pickle')
print('from e_logs.core.models import Setting')
print('from e_logs.common.all_journals_app.models import Plant, Journal, Table, Field')
print('')
print('')
print('def fill_fields_descriptions():')
print("""    Setting.objects.bulk_create([""")
for plant in Plant.objects.all():
    # print(plant.name)
    for journal in Journal.objects.filter(plant=plant).cache():
        # print(journal.name)
        for table in Table.objects.filter(journal=journal).cache():
            # print(table.name)
            for field in Field.objects.filter(table=table).cache():
                # print(field.name)
                desc = str(fields_info_desc[journal.name][table.name][field.name])
                # print(plant.name, journal.name, table.name, field.name)
                print("""        Setting(\n            name='field_description',\n            value=pickle.dumps({}),\n            scope=Field.objects.get(\n                table=Table.objects.get(\n                    journal=Journal.objects.get(\n                        plant=Plant.objects.get(\n                            name='{}'\n                        ),\n                        name='{}'\n                    ),\n                    name='{}'\n                ),\n                name='{}'\n             )\n        ),""".format(desc, plant.name, journal.name, table.name, field.name))
print('])')
