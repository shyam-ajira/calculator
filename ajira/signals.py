from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Room, Floor, Summary

def update_summary(instance):
    """ Recalculate the summary whenever a Room or Floor changes """
    summary, created = Summary.objects.get_or_create(user_name=instance.user_name)
    summary.save()  # Triggers the updated save() logic

@receiver(post_save, sender=Room)
@receiver(post_delete, sender=Room)
@receiver(post_save, sender=Floor)
@receiver(post_delete, sender=Floor)
def recalculate_summary(sender, instance, **kwargs):
    update_summary(instance)
