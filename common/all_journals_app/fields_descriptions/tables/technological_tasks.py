from common.all_journals_app.fields_descriptions.fields_classes import *
from utils.deep_dict import deep_dict



ts = deep_dict()
ts.date_create = dict(type="date")
ts.comments = text_default
ts.employee = text_default

technologial_tasks_main_desc = ts.clear_empty().get_dict()