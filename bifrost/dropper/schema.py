import json
from os.path import basename
from tempfile import TemporaryFile
from urllib.parse import urlsplit

import graphene
import requests
from django.core.files import File
from graphene.types.generic import GenericScalar
from graphql import GraphQLError
from graphql_jwt.decorators import superuser_required
from python_graphql_client import GraphqlClient
from wagtail.core.models import Site

from ..models import BifrostFile, DropperSettings
from .types import GenerationStatus


def get_dropper_connection():

    settings = DropperSettings.for_site(Site.objects.get(is_default_site=True))

    license_key = settings.license
    endpoint = settings.get_dropper_endpoint_display()

    client = GraphqlClient(endpoint=endpoint)

    return client, endpoint, license_key


def bifrost_authenticate():
    client, endpoint, license_key = get_dropper_connection()

    authData = client.execute(
        query="""
            mutation tokenAuth($username: String!, $password: String!) {
                tokenAuth(username: $username, password: $password) {
                    token
                    refreshToken
                    user {
                        username
                    }
                }
            }     
        """,
        variables={"username": "cisco", "password": "ciscocisco"},
    )

    bifrost_auth_token = authData["data"]["tokenAuth"]["token"]

    return bifrost_auth_token


def download_to_file_field(url, field):
    with TemporaryFile() as tf:
        r = requests.get(url, stream=True)
        for chunk in r.iter_content(chunk_size=4096):
            tf.write(chunk)

        tf.seek(0)
        field.save(basename(urlsplit(url).path), File(tf))


def download_file(url):
    r = requests.get(url, allow_redirects=True)

    with open("bridge-drop.tgz", "wb") as file:
        file.write(r.content)

        private_file = BifrostFile.objects.get_or_create(file__name=file.name)

        private_file.file.save(file.name, File(file))
        return private_file


class RequestDropperBridgeDrop(graphene.Mutation):
    taskId = graphene.String()

    class Arguments:
        token = graphene.String(required=False)

    @superuser_required
    def mutate(self, info, **kwargs):
        try:
            import bifrost.schema

            bifrost_auth_token = bifrost_authenticate()
            client, endpoint, license_key = get_dropper_connection()

            introspection_dict = bifrost.schema.schema.introspect()
            introspection_data = json.dumps(introspection_dict)

            document = """
                mutation requestBridgeDrop($introspectionData: JSONString!, $licenseKey: String!) {
                    requestBridgeDrop(introspectionData: $introspectionData, licenseKey: $licenseKey) {
                        taskId
                    }
                }
            """

            request_bridge_drop_data = client.execute(
                query=document,
                variables={
                    "introspectionData": introspection_data,
                    "licenseKey": license_key,
                },
                headers={"Authorization": f"JWT {bifrost_auth_token}"},
            )

            if "errors" in request_bridge_drop_data:
                raise GraphQLError(request_bridge_drop_data["errors"][0]["message"])

            taskId = request_bridge_drop_data["data"]["requestBridgeDrop"]["taskId"]

            return RequestDropperBridgeDrop(
                taskId=taskId,
            )
        except Exception as ex:
            raise GraphQLError(ex)


class Mutation(graphene.ObjectType):
    request_dropper_bridge_drop = RequestDropperBridgeDrop.Field()


class Query(graphene.ObjectType):
    get_dropper_bridge_drop = graphene.Field(
        GenerationStatus, task_id=graphene.ID(required=True)
    )

    @superuser_required
    def resolve_get_dropper_bridge_drop(root, info, task_id):
        try:
            bifrost_auth_token = bifrost_authenticate()
            client, endpoint, license_key = get_dropper_connection()

            request_bridge_drop_data = client.execute(
                query="""
                    query getBridgeDrop($taskId: ID!) {
                        getBridgeDrop(taskId:$taskId){
                            status
                            url
                        }
                    }
                """,
                variables={"taskId": task_id},
                headers={"Authorization": f"JWT {bifrost_auth_token}"},
            )

            if "errors" in request_bridge_drop_data:
                raise GraphQLError(request_bridge_drop_data["errors"])

            generation_status = request_bridge_drop_data["data"]["getBridgeDrop"]
            file_url = generation_status["url"]

            if file_url:
                private_file = BifrostFile()
                download_to_file_field(file_url, private_file.file)
                file_url = private_file.get_download_url()

            return {
                "status": GenerationStatus.Status.get(generation_status["status"]),
                "url": file_url,
            }

        except:
            raise GraphQLError("Something went wrong. Please try again later!")
