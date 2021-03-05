import channels_graphql_ws


class GraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    import bifrost.schema

    """Channels WebSocket consumer which provides GraphQL API."""

    schema = bifrost.schema.schema
