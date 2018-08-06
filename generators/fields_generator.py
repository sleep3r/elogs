from e_logs.common.all_journals_app.fields_descriptions.fields_info import fields_info_desc

print('from e_logs.common.all_journals_app.models import Table, Field, Journal')
print()
print()
print('def fill_fields():\n    ')

for journal in fields_info_desc:
    print("""    {}_journal = Journal.objects.get(name='{}')""".format(journal, journal))

print()

for journal in fields_info_desc:
    for table in fields_info_desc[journal]:
        print("""    {}_table_{} = Table.objects.get(name='{}', journal={}_journal)"""
              .format(
                  table.replace('_table', ''), 
                  journal, 
                  table.replace('_table', ''),
                  journal
              )
        )

print()

print('    Field.objects.bulk_create([')
for journal in fields_info_desc:
    for table in fields_info_desc[journal]:
        for field in fields_info_desc[journal][table]:
            print("""        Field(\n            name='{}',\n            table={}_table_{}\n        ),"""
                  .format(
                      field.replace('_field', ''), 
                      table.replace('_table', ''), 
                      journal
                  )
            )

print('    ])')

