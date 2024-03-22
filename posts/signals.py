from cloudinary_storage.storage import MediaCloudinaryStorage
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from posts.models import Post
import logging


logger = logging.getLogger(__name__)


# Signal receiver function
@receiver(pre_delete, sender=Post)
def mymodel_pre_delete(sender, instance, **kwargs):

    logger.info(f"Process Started to Clean Cloudinary Orphanged Media...")

    if instance.image:

        logger.info(f"Identified a stored Image...")
        try:
            logger.info(f"Trying to delete...")

            image_field = instance._meta.get_field('image')

            storage = image_field.storage if hasattr(image_field, 'storage') else None

            if storage and isinstance(storage, MediaCloudinaryStorage):

                if storage.delete(instance.image.name):
                    
                    print("deleted")

            logger.info("Image deleted Successfully...")

        except Exception as exc:

            logger.error("Unable to Delete Image...")

            logger.error(f"Error {str(exc).strip("\n")}")

    if instance.video:

        logger.info(f"Identified a stored Video...")
        try:
            logger.info(f"Trying to delete...")

            video_field = instance._meta.get_field('video')

            storage = video_field.storage if hasattr(image_field, 'storage') else None

            if storage and isinstance(storage, MediaCloudinaryStorage):

                storage.delete(instance.video.name)

            logger.info("Video deleted Successfully...")

        except Exception as exc:

            logger.error("Unable to Delete Video...")

            logger.error(f"Error {str(exc).strip("\n")}")

    logger.info("Cleaning Service Ended...")

