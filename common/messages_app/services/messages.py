from login_app.models import Employee, Message
from common.all_journals_app.models import CellValue

def get_addressees(all=False, positions=None, ids=None, plant=None):
    '''Отдает список адресатов'''
    res = []
    if all:
        return Employee.objects.only('user')
    if positions:
        for p in positions:
            emp = Employee.objects.filter(plant=plant, position=p)
            res.extend(emp)
    if ids:
        for id in ids:
            emp = Employee.objects.get(id=id)
            res.append(emp)

    return res


def filter_or_none(model, *args, **kwargs):
    try:
        return model.objects.filter(*args, **kwargs)
    except model.DoesNotExist:
        return None


def check_del_string(table, journal, ind):    
    finded_string = filter_or_none(CellValue, journal_page_id = journal, 
                                              table_name = table, 
                                              index = ind,
                                              ).exclude(field_name='index')
    if finded_string:
        for cell in finded_string:
            if cell.value: return

        messages = filter_or_none(Message, is_read=False, 
                                cell_table_name=table,
                                row_index=ind,
                                cell_journal_page=journal)
        if messages:
            for message in messages:
                message.is_read=True
                message.save()   
