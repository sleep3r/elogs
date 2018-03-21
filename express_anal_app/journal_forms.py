# -------------- django web forms -----------------------
import inspect

from django import forms
from django.forms import ModelForm
from express_anal_app.models import *

import inspect
from express_anal_app import models as eamodels
from django.db import models


def generate_standard_forms():
    """

    :return:
    """
    standard_forms = {}

    db_models = []
    exception_models = [User, Employee, Shift, Journal, JournalTable]
    for name, obj in inspect.getmembers(eamodels):
        if inspect.isclass(obj) and issubclass(obj, models.Model) and not obj in exception_models:
            db_models.append(obj)

    exception_fields = ['journaltable_ptr']
    for m in db_models:
        fields = [f.name for f in m._meta.get_fields(include_parents=False) if f.name not in exception_fields]
        Meta = type('Meta', (object,), {'model': m, 'fields': fields})
        FormClass = type(m.__name__ + 'Form', (ModelForm,), {'Meta': Meta})

        standard_forms[m.__name__] = FormClass

    return standard_forms

# Any form class can be instanced like jea_stand_forms['CinderDensity']() (model name inside brackets)
# Any class can be obtained like jea_stand_forms['CinderDensity']
jea_stand_forms = generate_standard_forms()


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
                  'journal',
                  'shift',
                  'shlippe',
                  'zn_dust',
                  'mg_ore',
                  'magnaglobe',
                  'fe_shave',
                  'state',
                  'stage',
                  'fence_state',
                  ]


class NeuturalDensersForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NeuturalDensersForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = NeutralDenser
        fields = [
            'journal',
            'shift',
            'num',
            'sediment',
            'liq_sol1',
            'liq_sol2'
        ]


class ExpressAnalysisForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExpressAnalysisForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = LeachingExpressAnal
        fields = [
            'journal',
            'shift',
            'point',
            'co',
            'sb',
            'cu',
            'cu_st1',
            'cd',
            'solid_st1',
            'ph',
            'fe',
            'arsenic',
            'solid',
            'current',
            'density'
        ]


class DenserAnalysisForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DenserAnalysisForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = DenserAnal
        fields = [
            'journal',
            'shift',
            'time',
            'point',
            'sink',
            'ph',
            'cu',
            'fe',
            'liq_sol',
        ]



class ZnPulpForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ZnPulpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = ZnPulpAnal
        fields = [
            'journal',
            'shift',
            'liq_sol',
            'ph',
            't0'
        ]

class CuPulpForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CuPulpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = CuPulpAnal
        fields = [
            'journal',
            'shift',
            'liq_sol',
            'before',
            'after',
            'solid'
        ]


class FeSolutionForm(ModelForm):
    class Meta:
        model = FeSolutionAnal
        fields = [
            'journal',
            'shift',
            'h2so4',
            'solid',
            'sb',
            'cu',
            'fe',
            'density',
            'arsenic',
            'cl',
        ]

class HydrometalForm(ModelForm):
    class Meta:
        model = HydroMetal
        fields = [
            'journal',
            'shift',
            'ph',
            'acid',
            'fe2',
            'fe_total',
            'cu',
            'sb',
            'sediment',
            'mann_num',
            'employee'
        ]

class AgitatorsForm(ModelForm):
    class Meta:
        model = Agitators
        fields = [
            'journal',
            'shift',
            'num',
            'before',
            'ph',
            'cu',
            'co',
            'cd',
            'h2so4',
            'comment',
            'employee'
        ]
# ------------- end forms -----------------------------