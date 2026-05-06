from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lead


@receiver(post_save, sender=Lead)
def on_lead_created(sender, instance, created, **kwargs):
    if not created:
        return
    from .services.notifications import notify_new_lead
    notify_new_lead(instance)
