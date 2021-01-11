from django.conf import settings
from django.conf.urls import url
from django.shortcuts import render
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer


def graphiql(request):
    graphiql_settings = {
        "REACT_VERSION": "16.13.1",
        "GRAPHIQL_VERSION": "0.17.5",
        "SUBSCRIPTIONS_TRANSPORT_VERSION": "0.9.16",
        "subscriptionsEndpoint": "ws://localhost:8000/subscription/",
        "endpointURL": "/graphql",
    }

    return render(request, "bifrost/graphiql.html", graphiql_settings)


# Traditional URL routing
SHOULD_EXPOSE_GRAPHIQL = settings.DEBUG or getattr(
    settings, "BIFROST_EXPOSE_GRAPHIQL", False
)
urlpatterns = [url(r"^graphql", csrf_exempt(FileUploadGraphQLView.as_view()))]

websocket_urlpatterns = [
    path("subscription/", GraphqlSubscriptionConsumer),
]

if SHOULD_EXPOSE_GRAPHIQL:
    urlpatterns.append(url(r"^graphiql", graphiql))
