import json
from utils.deep_dict import deep_dict
from datetime import time
from common.all_journals_app.fields_descriptions.fields_classes import *


mt = deep_dict()

mt.date1 = date_default
mt.node_name = text_default
mt.signature1 = text_default
mt.date2 = date_default
mt.work_done = text_default
mt.texpl_time = text_default
mt.signature2 = text_default

main_table_desc = mt.clear_empty().get_dict()


# --------------------------------------- small table -----------------------------------------------------
