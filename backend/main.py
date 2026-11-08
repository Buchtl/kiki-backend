import asyncio
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, StrictStr

app = FastAPI(title="backend")


class ProcessRequest(BaseModel):
    text: StrictStr


async def progress_events() -> AsyncIterator[str]:
    yield "event: progress\ndata: 0\n\n"
    for percentage in range(10, 101, 10):
        await asyncio.sleep(1)
        yield f"event: progress\ndata: {percentage}\n\n"
    yield "event: result\ndata: done\n\n"


@app.post("/process", response_class=StreamingResponse)
async def process(request: ProcessRequest) -> StreamingResponse:
    return StreamingResponse(
        progress_events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
