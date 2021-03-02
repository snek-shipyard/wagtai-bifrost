import channels_graphql_ws


class GraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""

    schema = None
