from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment

@receiver(post_save,sender=Comment)
def comment_added(sender,instance,created,**kwargs):
    if created:
        print(f"[signal] New comment by {instance.author} on '{instance.post}'")
