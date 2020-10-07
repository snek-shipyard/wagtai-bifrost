import graphene
from django.conf import settings
from graphql.validation.rules import NoUnusedFragments, specified_rules

# HACK: Remove NoUnusedFragments validator
# Due to the way previews work on the frontend, we need to pass all
# fragments into the query even if they're not used.
# This would usually cause a validation error. There doesn't appear
# to be a nice way to disable this validator so we monkey-patch it instead.


# We need to update specified_rules in-place so the change appears
# everywhere it's been imported

specified_rules[:] = [rule for rule in specified_rules if rule is not NoUnusedFragments]


def create_schema():
    """
    Root schema object that graphene is pointed at.
    It inherits its queries from each of the specific type mixins.
    """
    from .registry import registry
    from .types.documents import DocumentsQuery
    from .types.images import ImagesQuery
    from .types.pages import PagesQuery, has_channels
    from .types.search import SearchQuery
    from .types.settings import SettingsQuery
    from .types.sites import SitesQuery
    from .types.snippets import SnippetsQuery
    from .types.redirects import RedirectsQuery
    from .types.tags import TagsQuery

    query_kwargs = [
        graphene.ObjectType,
        PagesQuery(),
        SitesQuery(),
        ImagesQuery(),
        DocumentsQuery(),
        SnippetsQuery(),
        SettingsQuery(),
        SearchQuery(),
        RedirectsQuery,
        TagsQuery(),
    ]

    try:
        from .types.media import MediaQuery

        query_kwargs.append(MediaQuery())
    except ModuleNotFoundError:
        pass

    query_kwargs += registry.schema

    class Query(*query_kwargs,):
        pass

    if has_channels:
        from .types.pages import PagesSubscription

        class Subscription(PagesSubscription(), graphene.ObjectType):
            pass

    else:
        Subscription = None

    return graphene.Schema(
        query=Query,
        subscription=Subscription,
        types=list(registry.models.values()),
        auto_camelcase=getattr(settings, "BIFROST_AUTO_CAMELCASE", True),
    )


schema = create_schema()
