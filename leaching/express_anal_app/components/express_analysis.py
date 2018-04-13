from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db import transaction
from leaching.express_anal_app.models import *
from django.utils.translation import gettext as _

import pprint



@login_required
def express(request):
    # journal = Journal.objects.get(name='Журнал экспресс анализов')
    if 'shift' in request.GET:
        shiftId = request.GET['shift']
        try:
            shift = Shift.objects.get(id=shiftId) or None
        except:
            shift = Shift.objects.all()[0]
    else:
        shift = Shift.objects.all()[0]

    shifts = Shift.objects.all()

    context = {
        'form_shift': {
            'title': _('Выбранная смена'),
            'currentId': shift.id,
            'data': shifts,
            'dump': pprint.pformat(shifts),
            'action': '/leaching/edit/wizard'
        },
        'form_express_analysis': {
            'title': _('Экспресс анализ'),
            'name': 'form_express_analysis',
            'action': '/leaching/save/express/analysis',
            'times': ['8', '10', '12', '14', '16', '18', '20'],
            'columns': [_("Кобальт") + " Co, " + _('мг/л'), _("Сурьма") + _('мг/л'), _("Медь") + _('мг/л'), _("Кадмий"), _("Твердое После 1ст"), "pH (BCHC)",
                        _("Железо"), "As",
                        _("Твёрдое "), _("Уд. вес"),
                        _("Кобальт"), _("Сурьма"), _("Кадмий"), _("Твердое"), "pH", _("Кадмий"), _("Кобальт"),
                        _("Сурьма"), _("Медь"), _("Железо"),
                        _("Выход по току"), _("Уд. вес"), _("Норма"), _("Факт"), _("Несоответствие"), _("Коррекция")],
            'shift': shift.id,
        },
        'form_densers': {
            'name': 'form_densers',
            'title': _('Сгустители'),
            'columns': ['10', "11", "12"],
            'action': '/save/densers',
            'shift': shift.id,
        },


    }
    template = loader.get_template('edit_by_hours.html')
    return HttpResponse(template.render(context, request))