from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Room, Floor, Summary, Cost

def update_summary_and_cost(instance):
    """ Recalculate the summary and cost whenever a Room or Floor changes """
    # Update or create Summary
    summary, created = Summary.objects.get_or_create(user_name=instance.user_name)
    summary.save()
    
    # Update or create Cost
    cost, created = Cost.objects.get_or_create(user_name=instance.user_name)
    cost.save()

@receiver(post_save, sender=Room)
@receiver(post_delete, sender=Room)
@receiver(post_save, sender=Floor)
@receiver(post_delete, sender=Floor)
def recalculate_summary_and_cost(sender, instance, **kwargs):
    update_summary_and_cost(instance)
