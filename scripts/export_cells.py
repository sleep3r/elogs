import pickle

from e_logs.common.all_journals_app.models import Cell


dump = []
for cell in Cell.objects.all():
    c = {}
    c['plant_name'] = cell.journal.plant.name
    c['table_name'] = cell.field.table.name
    c['field_name'] = cell.field.name
    c['index'] = cell.index
    c['journal_name'] = cell.journal.name
    c['value'] = cell.value
    if hasattr(cell.group, 'shift'):
        c['shift'] = {}
        c['shift']['date'] = cell.group.shift.date
        c['shift']['order'] = cell.group.shift.order
    if hasattr(cell.group, 'year'):
        c['year'] = cell.group.year.year_date
    if hasattr(cell.group, 'month'):
        c['month'] = {}
        c['month']['date'] = cell.group.month.month_date
        c['month']['order'] = cell.group.month.month_order
        c['month']['year_date'] = cell.group.month.year_date
    if hasattr(cell.group, 'equipment'):
        c['equipment'] = cell.group.equipmment.name
    dump.append(c)


pickleFile = open("./resources/data/kazzinc_cells_dump", 'wb')
pickle.dump(dump, pickleFile)
