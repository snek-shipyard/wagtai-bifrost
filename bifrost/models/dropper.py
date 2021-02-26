from django.conf import settings
from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting


class DropperSettings(BaseSetting):
    class DropperEndpoints(models.TextChoices):
        PUBLIC = "P", "https://dropper.snek.at/graphql"
        LOCAL = "L", "http://localhost:8000/graphql"

    dropper_endpoint = models.CharField(
        max_length=6, choices=DropperEndpoints.choices, default=DropperEndpoints.PUBLIC
    )
    license = models.TextField()


if getattr(settings, "BIFROST_DROPPER", False):
    register_setting(DropperSettings)
