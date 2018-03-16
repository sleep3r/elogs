# -------------- django web forms -----------------------
from django import forms
from django.forms import ModelForm
from express_anal_app.models import *


class PostForm(forms.Form):
    content = forms.CharField(max_length=255)
    created_at = forms.DateTimeField()


class DenserForm(ModelForm):
    error_css_class = 'label label-danger'
    def __init__(self, *args, **kwargs):
        super(DenserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = DenserAnal
        fields = ['journal', 'shift', 'point','sink','ph', 'cu', 'fe', 'liq_sol', 'time']
        widgets = {
            'time': forms.DateInput(attrs={'type': 'hidden', 'class':'form-control has-feedback-left'}),
            'journal': forms.HiddenInput(attrs={'style': 'display:none'}),
            'shift': forms.HiddenInput(attrs={'type': 'hidden'})
        }


class ReadyProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReadyProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ReadyProduct
        fields = [
                    'journal',
                    'shift',
                    'num',
                    'cd',
                    'cu',
                    'co',
                    'sb',
                    'fe',
                    'vt',
                    'density',
                    'norm',
                    'fact',
                    'correction',
                    'verified',
                  ]

class ReagentsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReagentsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Reagents
        fields = [
                  'shlippe',
                  'zn_dust',
                  'mg_ore',
                  'magnaglobe',
                  'fe_shave',
                  'state',
                  'stage',
                  'fence_state',
                  'journal',
                  'shift'
                  ]



# ------------- end forms -----------------------------