# -*- coding: utf-8 -*-
import inspect
import random
from datetime import timedelta
from inspect import ismethod
from itertools import product

from django.db.models import Model
from django.utils import timezone

from models import *
import models
from utils.webutils import parse, translate
from django.utils.translation import gettext as _


class Filler:
    def __init__(self, journal):
        self.journal = journal

    def fill(self, table_name, field_name, values):
        for values in values:
            if type(value) is not str:
                value = str(value)
            v = CellValue(
                object=self.journal,
                table_name=table_name,
                field_name=field_name,
                value=value)
            v.save()


def main():
    journal = JournalPage(type="shift", journal_name=u"Журнал рапортов")
    table_name = "big table"
    n = 10
    data = {
        "Номер вагона": [1234] * n,
        "Наименование концентрата": ["ЗГОК"] * n,
        "Время поставки": ["11:00"] * n,
        "Время сообщения диспетчеру": ["12:00"] * n,
        "Время перепростоя": ["12:00"] * n,
        "Контейнеров": [3] * n,
        "Подонов": [3] * n,
        "Упоров": [3] * n,
        "Скоб": [3] * n,
        "Сданы по смене": ["Что-нибудь"] * n
    }

    filler = Filler(journal)
    for field_name, values in data.items():
        filler.fill(table_name, field_name, values)
