from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import IntegrityError

from .models import Cell


@receiver(pre_save, sender=Cell)
def check_cell_integrity(sender, instance: Cell, **kwargs):
    if not instance.group.journal == instance.field.table.journal:
        raise IntegrityError("Can't save cell related to different journals")
