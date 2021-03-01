import binascii
import os

from django.conf import settings
from django.db import models
from private_storage.fields import PrivateFileField


# Django models
def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


class BifrostFile(models.Model):
    access_token = models.CharField(default=generate_key, max_length=40)
    file = PrivateFileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.file.name

    def get_download_url(self) -> str:
        return (settings.BASE_URL + self.file.url).replace(
            "://", f"://{self.access_token}@"
        )
