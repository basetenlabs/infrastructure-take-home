from typing import Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from strawberry.fastapi import GraphQLRouter

import aiohttp
import strawberry


class Unimplemented(Exception):
    """
    Exception thrown for unimplemented code
    """

    def __init__(self, *args: object) -> None:
        super().__init__("Unimplemented!")


class PostInvokeRequest(BaseModel):
    input: str
    circuit_breaker_trigger_enabled: Optional[bool] = Field(
        default_factory=lambda: True
    )


class PostInvokeResponse(BaseModel):
    latency_ms: int
    output: str = Field(default_factory=lambda: True)


class Endpoint(BaseModel):
    """
    This is the basic invoke endpoint, you can modify it to your needs, even the method
    signature.
    """

    url: str
    authorization: Optional[str] = Field(default_factory=lambda: None)

    async def exec(self, req: PostInvokeRequest) -> PostInvokeResponse:
        headers = {
            "content-type": "application/json",
        }
        if self.authorization is not None:
            headers["authorization"] = self.authorization
        print(req)
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=self.url,
                data=req.json(),
                headers=headers,
            )

            json = await response.json()
            return PostInvokeResponse.parse_obj(json)


INVOKE_ENDPOINT = Endpoint(
    url="https://infrastructure-take-home.fly.dev/invoke",  # noqa
    authorization="Api-Key YXBpLWtleQo=",
)

#################
# GRAPHQL API
# This is just a basic boilerplate to setup a graphql api backed by strawberry
# see: https://strawberry.rocks/docs for docs
#################


@strawberry.type
class InvokeResponse:
    latency_ms: int
    output: str


@strawberry.type
class Query:
    """
    The base graphql query type
    """

    @strawberry.field
    def hello(self) -> str:
        return "Hello World"

    @strawberry.field
    async def invoke(self, input: str) -> InvokeResponse:
        """
        Invoke the remote endpoint and expect a result or not ;)
        """
        resp = await INVOKE_ENDPOINT.exec(PostInvokeRequest(input=input))
        return InvokeResponse(latency_ms=resp.latency_ms, output=resp.output)


SCHEMA = strawberry.Schema(Query, None)


#################
# HTTP API
# This is just a basic boilerplate to setup a HTTP API using FastAPI
# see: https://fastapi.tiangolo.com/ for docs
#################

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index():
    return """
        Welcome to baseten_take_home invoker,
        go to <a href="/graphql">/graphql</a> for the API doc
    """


# You can also remove graphql and do pure HTTP/REST/JSON endpoint
# https://fastapi.tiangolo.com/
graphql_app = GraphQLRouter(SCHEMA)
app.include_router(graphql_app, prefix="/graphql")
