from service_objects.services import Service
from django import forms

from e_logs.business_logic.modes.models import Mode, FieldConstraints
from e_logs.common.all_journals_app.models import Field
from e_logs.common.messages_app.models import Message


class SetMode(Service):
    message = forms.CharField(max_length=1024)
    beginning = forms.DateTimeField()
    end = forms.DateTimeField()

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
                                   end=self.cleaned_data['end'])

        for f in self.data['fields']:
            field = Field.objects.get(name=f['name'], table__name=f['table_name'])

            FieldConstraints.objects.create(min_normal=f['min_normal'],
                                            max_normal=f['max_normal'],
                                            field=field, mode=mode)

        Message.add(cell=None,
                    message={'type':'set_mode',
                             'text':self.cleaned_data['message'],
                             'sendee':self.data['sendee']},
                    all_users=True)

        return mode