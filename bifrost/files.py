import binascii
import os

from django.db import models
from private_storage.fields import PrivateFileField


# Django models
def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


class BifrostFile(models.Model):
    access_token = models.CharField(default=generate_key, max_length=40)
    file = PrivateFileField()

    def __str__(self) -> str:
        return self.file.name
