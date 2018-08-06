from e_logs.common.all_journals_app.fields_descriptions.fields_info import fields_info_desc

print('from e_logs.common.all_journals_app.models import Journal, Table')
print()
print()
print('def fill_tables():\n    ')


for journal in fields_info_desc:
    print("""    {}_journal = Journal.objects.get(name='{}')""".format(journal, journal))

print()

print('    Table.objects.bulk_create([')
for journal in fields_info_desc:
    for table in fields_info_desc[journal]:
        print("""        Table(\n            name='{}',\n            journal={}_journal\n        ),""".format(table.replace('_table', ''), journal))

print('    ])')
