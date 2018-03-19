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
# ------------- end forms -----------------------------