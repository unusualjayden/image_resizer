import base64
import uuid

from django.db import models


def image_upload_handler(instance, filename):
    extension = filename.split(".")[1]
    return f'uploads/{instance.image_hash}.{extension}'


class Image(models.Model):
    image_hash = models.TextField()
    image_file = models.ImageField(upload_to=image_upload_handler, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.image_hash = self.generate_hash()
        super(Image, self).save(*args, **kwargs)

    def generate_hash(self):
        hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:6]
        hash_exist = Image.objects.filter(image_hash=hash)
        while hash_exist:
            hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:6]
            hash_exist = Image.objects.filter(image_hash=hash)
            continue
        hash = hash.decode('utf-8')

        return hash

    class Meta:
        db_table = 'image'
        ordering = ['created_at']
