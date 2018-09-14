from datetime import timedelta

from django.utils import timezone
from service_objects.services import Service
from django import forms

from e_logs.business_logic.modes.models import Mode, FieldConstraints
from e_logs.common.all_journals_app.models import Field, Shift, Journal
from e_logs.common.messages_app.models import Message
from e_logs.core.models import Setting
from e_logs.common.all_journals_app.tasks import end_of_mode, end_of_limited_access, \
    send_deferred_message
from e_logs.core.utils.webutils import get_or_none


class SetMode(Service):
    message = forms.CharField(max_length=1024)
    beginning = forms.DateTimeField()
    end = forms.DateTimeField()
    journal_id = forms.IntegerField()
    table_name = forms.CharField(max_length=256)

    # для валидации списка полей
    def clean(self):
        super().clean()

        if ('fields' in self.data) and (isinstance(self.data['fields'], list)) is True:
            return self.cleaned_data
        else:
            raise forms.ValidationError('Invalid fields data')

    def process(self):
        mode = Mode.objects.create(message=self.cleaned_data['message'],
                                   beginning=self.cleaned_data['beginning'],
                                   end=self.cleaned_data['end'],
                                   journal=Journal.objects.get(id=self.cleaned_data['journal_id']))

        for f in self.data['fields']:
            field = Field.objects.get(name=f['name'],
                                      table__name=self.cleaned_data['table_name'],)

            FieldConstraints.objects.create(min_normal=f['min_normal'],
                                            max_normal=f['max_normal'],
                                            field=field, mode=mode)

        Message.add(cell=None,
                    message={'type':'set_mode',
                             'text':self.cleaned_data['message'],
                             'sendee':self.data['sendee']},
                    all_users=True)

        end_of_mode.apply_async((mode.id,), eta=self.cleaned_data['end'])

        return mode


class CheckRole(Service):
    def clean(self):
        super().clean()

        if ('employee' in self.data) and ('page' in self.data):
            return self.cleaned_data
        else:
            raise forms.ValidationError('Invalid data')

    def process(self):
        page = self.data['page']
        position = self.data['employee'].position
        allowed_positions = Setting.of(page)["allowed_positions"]
        if position in allowed_positions if allowed_positions else ('boss', 'laborant',):
            if page.employee_set.filter(position=position).\
                    count() < int(Setting.of(page)[f"number_of_{position}"] or 1):
                return True
        if self.data['employee'] in page.employee_set.all():
            return True

        return False


class CheckTime(Service):
    def clean(self):
        super().clean()

        if ('employee' in self.data) and ('page' in self.data):
            return self.cleaned_data
        else:
            raise forms.ValidationError('Invalid data')

    def process(self):
        page = self.data['page']
        employee = self.data['employee']
        assignment_time = Setting.of(page)['shift_assignment_time']

        if timezone.now() > page.end_time - timedelta(**assignment_time if \
           assignment_time else {"hours":1}) and employee not in page.employee_set.all():
            return False

        if timezone.now() > page.end_time + timedelta(hours=12):
            return False

        shift = get_or_none(Shift, date=page.date, order=int(page.order-1), journal=page.journal)
        if shift and not shift.ended and employee not in page.employee_set.all():
            return False

        return True

class SetLimitedAccess(Service):
    shift_id = forms.IntegerField()

    def clean(self):
        super().clean()

        if ('emp_id_list' in self.data) and (isinstance(self.data['emp_id_list'],list)) is True and\
           ('time' in self.data) and (isinstance(self.data['time'], dict)) is True:
            return self.cleaned_data
        else:
            raise forms.ValidationError('Invalid time data')

    def process(self):
        page = get_or_none(Shift, id=self.cleaned_data['shift_id'])

        if page and page.closed == True:
            Setting.of(page)['limited_access_employee_id_list'] = self.data['emp_id_list']

            end_time = timezone.now() + timedelta(**self.data['time'])
            end_of_limited_access.apply_async((page.id,), eta=end_time)

            for min in (60, 40, 20):
                send_deferred_message.apply_async(
                    ('warning', f'До конца ограниченного доступа осталось {min} минут'),
                    eta=end_time - timedelta(minutes=min))

            return page