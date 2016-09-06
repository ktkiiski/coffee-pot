from webcam.models import Picture
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


@receiver(pre_delete, sender=Picture)
def handle_deleted_picture(sender, instance, **kwargs):
    print("Deleting the file of image {}".format(instance))
    instance.image.delete(save=False)
