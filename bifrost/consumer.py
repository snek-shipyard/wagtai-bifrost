import channels_graphql_ws

import bifrost.schema


class GraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""

    schema = bifrost.schema.schema
