from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Example, SubExample

@receiver(pre_save, sender=Example)
def notify_example_pre_save(sender, instance, **kwargs):
    print("Example pre_save signal")

@receiver(pre_save, sender=SubExample)
def notify_sub_example_pre_save(sender, instance, **kwargs):
    print("SubExample pre_save signal")