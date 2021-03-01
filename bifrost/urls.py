from django.conf.urls import url
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from .consumer import GraphqlWsConsumer
from .views import BifrostFileView, BifrostView

# Traditional URL routing
urlpatterns = [
    url(r"^graphql", csrf_exempt(BifrostView.as_view())),
    url(
        "^bifrost-internal/(?P<path>.*)$",
        BifrostFileView.as_view(),
        name="serve_private_file",
    ),
]

websocket_urlpatterns = [re_path(r"^graphql/?$", GraphqlWsConsumer.as_asgi())]

# if SHOULD_EXPOSE_GRAPHIQL:
#     urlpatterns.append(url(r"^graphiql", graphiql))
