import graphene


class GenerationTypes:
    class DropperState(graphene.Enum):
        PENDING = "PENDING"
        STARTED = "STARTED"
        RETRY = "RETRY"
        FAILURE = "FAILURE"
        SUCCESS = "SUCCESS"
