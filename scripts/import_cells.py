import pickle

from e_logs.common.all_journals_app.models import Cell, Shift, Journal, Table, Field, Plant, Year, Month, Equipment


pickleFile = open("./resources/data/kazzinc_cells_dump", 'rb')
dump = pickle.load(pickleFile)
for cell in dump:
    try:
        print(cell)
        plant = Plant.objects.get(name=cell['plant_name'])
        journal = Journal.objects.get(name=cell['journal_name'], plant=plant)
        if cell.get('shift'):
            group = Shift.objects.get_or_create(journal=journal, order=cell['shift']['order'],
                                                date=cell['shift']['date'])[0]
        if cell.get('year'):
            group = Year.objects.get_or_create(year_date=cell['year'], journal=journal)[0]
        if cell.get('month'):
            group = Month.objects.get_or_create(year_date=cell['month']['year_date'], month_date=cell['month']['date'],
                                                    month_order=cell['month']['order'],
                                                    journal=journal)[0]
        if cell.get('equipment'):
            group = Equipment.objects.get_or_create(name=cell['equipment'], journal=journal)[0]
        c = Cell.get_or_create_cell(group_id=group.id, table_name=cell['table_name'],
                        field_name=cell['field_name'], index=cell['index'])[0]
        c.value = cell['value']
        c.save()
    except:
        pass
pickleFile.close()
