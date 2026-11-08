# backend

A Python API that accepts a string and streams progress for ten seconds.

## Setup

Python 3.10 or newer is required.

```sh
python -m venv venv
. venv/bin/activate
python -m pip install -e '.[test]'
```

## Run

```sh
uvicorn backend.main:app --reload
```

The server defaults to port `8000`. Set a different port with the `--port`
command-line argument, for example:

```sh
uvicorn backend.main:app --reload --port 8080
```

Send a JSON object with a `text` string to `POST /process`:

```sh
curl -N -X POST http://127.0.0.1:8000/process \
  -H 'Content-Type: application/json' \
  -d '{"text":"hello"}'
```

Use the configured port in the URL if you changed it.

The response uses `text/event-stream`: `progress` events report percentages
from `0` to `100` at one-second intervals, followed by a `result` event whose
data is the string `done`. The input is validated but is not otherwise used.
The connection must stay open to receive the events; configure any reverse
proxy not to buffer the response.

Run the tests with `pytest`.
