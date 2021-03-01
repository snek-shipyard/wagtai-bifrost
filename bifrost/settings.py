# time
from datetime import timedelta

# django
from django.conf import settings

# graphql
from graphql import ResolveInfo

# settings
if hasattr(settings, "GRAPHQL_API"):
    SETTINGS = settings.GRAPHQL_API
else:  # pragma: no cover
    SETTINGS = {}

URL_PREFIX = SETTINGS.get("URL_PREFIX", {})
LOAD_GENERIC_SCALARS = SETTINGS.get("GENERIC_SCALARS", True)
RELAY = SETTINGS.get("RELAY", False)

GRAPHENE = {
    "SCHEMA": "bifrost.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}
GRAPHQL_JWT = {
    "JWT_ALLOW_ARGUMENT": True,
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": timedelta(minutes=5),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
}

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# wagtail settings
try:
    from wagtail.contrib.settings.registry import registry as settings_registry
except ImportError:  # pragma: no cover
    settings_registry = None


def url_prefix_for_site(info: ResolveInfo):
    hostname = info.context.site.hostname
    return URL_PREFIX.get(hostname, info.context.site.root_page.url_path.rstrip("/"))


# > Bifrost settings
# General
BIFROST_AUTO_CAMELCASE = getattr(settings, "BIFROST_AUTO_CAMELCASE", True)
# Dropper connection
BIFROST_DROPPER_ENDPOINT = getattr(
    settings, "BIFROST_DROPPER_ENDPOINT", "https://dropper.snek.at/graphql"
)
BIFROST_DROPPER_SOCKET_ENDPOINT = getattr(
    settings, "BIFROST_DROPPER_SOCKET_ENDPOINT", "wss://dropper.snek.at/graphql"
)
BIFROST_DROPPER_HEIMDALL_LICENSE = getattr(
    settings, "BIFROST_DROPPER_HEIMDALL_LICENSE", None
)
# Conditional schema registration
BIFROST_API_FILES = getattr(settings, "BIFROST_API_FILES", False)
BIFROST_API_DROPPER = getattr(settings, "BIFROST_API_DROPPER", False)
BIFROST_API_DOCUMENTS = getattr(settings, "BIFROST_API_DOCUMENTS", False)
BIFROST_API_IMAGES = getattr(settings, "BIFROST_API_IMAGES", False)
BIFROST_API_REDIRECTS = getattr(settings, "BIFROST_API_REDIRECTS", False)
BIFROST_API_SEARCH = getattr(settings, "BIFROST_API_SEARCH", False)
BIFROST_API_SETTINGS = getattr(settings, "BIFROST_API_SETTINGS", False)
BIFROST_API_SNIPPETS = getattr(settings, "BIFROST_API_SNIPPETS", False)
