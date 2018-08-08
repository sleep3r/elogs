from e_logs.common.login_app.models import Employee
from e_logs.common.messages_app.models import Message
from e_logs.common.all_journals_app.models import Cell


def get_addressees(all=False, positions=None, ids=None, plant=None):
    """Отдает список адресатов"""
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


def filter_or_none(cell, msg_type, addressee):
    try:
        if addressee:
            return Message.objects.filter(addressee=addressee,
                                          type=msg_type,
                                          cell_field_name=cell.field_name,
                                          cell_table_name=cell.table_name,
                                          row_index=cell.index,
                                          cell_journal_page=cell.journal_page_id,
                                          is_read=False)
        else:
            return Message.objects.filter(type=msg_type,
                                          cell_field_name=cell.field_name,
                                          cell_table_name=cell.table_name,
                                          row_index=cell.index,
                                          cell_journal_page=cell.journal_page_id,
                                          is_read=False)
    except Message.DoesNotExist:
        return None

