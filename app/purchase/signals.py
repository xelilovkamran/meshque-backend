from django.db.models.signals import pre_save
from django.dispatch import receiver
from purchase.models import Order


@receiver(pre_save, sender=Order)
def set_is_paid_on_delivered(sender, instance, **kwargs):
    if instance.status == "Delivered":
        instance.is_paid = True
