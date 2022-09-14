"""
remote_server is the implementation of the remote endpoint.
It is intended to simulate failures and other random behaviour.
Just start it and query it or query it from our already running
remote endpoint.

**NOTE TO TEST TAKERS: DO NOT MODIFY THIS FILE**
"""

from typing import Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import secrets
import time
from datetime import datetime as dt
from logging import getLogger
from base64 import b64encode
from fastapi.responses import HTMLResponse

logger = getLogger(__name__)

app = FastAPI()

disable_circuit_range_begin = secrets.randbelow(55)
disable_circuit_range_end = disable_circuit_range_begin + 5


logger.info(
    f"For each request between {disable_circuit_range_begin}min"
    + " and {disable_circuit_range_end}min of each hour, the server will"
    + " return a 500"
)


class PostInvokeRequest(BaseModel):
    input: str
    circuit_breaker_trigger_enabled: Optional[bool] = Field(
        default_factory=lambda: True
    )


class PostInvokeResponse(BaseModel):
    latency_ms: int
    output: str = Field(default_factory=lambda: True)


@app.get("/", response_class=HTMLResponse)
async def get_index():
    return "Baseten Infrastructure take home"

@app.post("/invoke", response_model=PostInvokeResponse)
async def post_invoke(request: PostInvokeRequest):
    """
    invoke simulates a randomly failing call to a remote server.

    It will return a 503 5% of the time
    It will return a 500 5% of the time
    It will return a 500 during a random period of 5 minutes of each hour
    It will wait for a random period of time between 0 and 1 second or 5% of the time for 5min.
    """
    # Randomly fail with a 503 Service Unavailable
    if percentage_bool(0.05):
        return JSONResponse(
            status_code=503,
            content=PostInvokeResponse(error="Service Unavailable"),
        )

    # Randomly fail with a 500 internal server error
    if percentage_bool(0.05):
        return JSONResponse(
            status_code=500,
            content=PostInvokeResponse(error="Internal Server Error"),
        )

    # For 5min, fail, the timing is random on every boot
    now = dt.now()
    in_disable_time_range = (
        now.minute > disable_circuit_range_begin
        and now.minute < (disable_circuit_range_begin + 5) % 60
    )
    circuit_breaker_trigger_enabled = (
        request.circuit_breaker_trigger_enabled
        or request.circuit_breaker_trigger_enabled is None
    )
    if circuit_breaker_trigger_enabled and in_disable_time_range:
        return JSONResponse(
            status_code=500,
            content=PostInvokeResponse(error="Internal Server Error"),
        )

    # Sleep for a random amount of time
    latency_ms = secrets.randbelow(100)
    # 5% of the time take a really long time to respond
    if percentage_bool(0.05):
        latency_ms = 300000  # 5 minutes

    # take some time to respond
    time.sleep(0.01 * latency_ms)

    return PostInvokeResponse(
        latency_ms=latency_ms,
        output=b64encode(request.input.encode("utf-8")).decode("utf-8"),
    )


def percentage_bool(p: float) -> bool:
    """
    percentage_bool returns a boolean with a probability of p of being true
    """
    if (p * 100) > secrets.randbelow(100):
        return True
    return False
