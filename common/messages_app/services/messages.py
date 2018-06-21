from login_app.models import Employee
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
