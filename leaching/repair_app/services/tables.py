from leaching.repair_app.models import Repairs
from utils.deep_dict import deep_dict


def get_repairs_table():
    res = deep_dict()
    data = Repairs.objects.all()

    for d in data:
        for attr in ['ph', 'cu', 'fe', 'liq_sol']:
            res[d.id][attr] = getattr(d, attr)
            res[d.id]['equipment']['id'] = d.equipment.id
            res[d.id]['equipment']['name'] = d.equipment.name

    return res.clear_empty().get_dict()