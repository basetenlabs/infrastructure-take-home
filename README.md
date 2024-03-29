This is the Baseten platform engineer take-home challenge. It should be a short challenge, we don't expect everything to be coded, comments on what you would do or would improve will also be happily evaluated. It is optional to use this boilerplate (eg: you want to use a different language) but we do think it's gonna save you some precious time.

# The Problem

- **Goal:** Show us your ability to incorporate reliability & infrastructure concepts through code by making making `main.py` handle failures that come from the remote web service https://infrastructure-take-home.fly.dev/.
- **Estimated time:** max. 2hours. We'd like to see some actual code, but you can also leave a bunch of comments on things you would improve. We're trying to be respectful of your time here so we totally understand if stuff is stubbed out or missing.

## Scenario
We've simulated an architecture where a service (`main.py`) calls another service (`remote_server.py`) which is hosted here https://infrastructure-take-home.fly.dev/. Unfortunately `remote_server` is hosted on the internet and as such is not 100% reliable (as with all online things).

**Our goal is to evaluate some knowledge of infrastructure and reliability concepts.**

Try to improve `main.py` to be more resilient to `https://infrastructure-take-home.fly.dev/` failures by adding some reliability and observability concepts in. There are multiple ways to approach this problem and multiple topics you could take on.


Example topics of improvements to the server:
- Testing
- Observatility
- Error budgets
- Retries
- Timeouts
- Circuit breakers
- Charge distribution / load-balancing
- ...

Example topics of improvements around the server:
- CI/CD
- Infrastructure as code
- ...


**Note:** I suggest you look at `remote_server.py`, it's the implementation of your "test endpoint" and it generates errors on purpose. The goal here is for you to make main.py somewhat more reliable.


# The boilerplate & remote server
## Prerequisite

- python >= 3.9
- [poetry](python-poetry.org/)

## Run

1. Start your local server (using vscode launch configurations or `make start`)

Once the server runs you can open `http://localhost:8000/graphql` and test the API with a sample graphql query.

Invoke the remote service:
```
query {
  invoke(input:"123123"){
    latencyMs
    output
  }
}
```

## Develop

### With vscode

1. In a command line run `poetry install`
2. Open the workspace in vscode
3. `⇧⌘P` then choose `Python: Select Interpreter`
4. The interpreter is the virtual env associated with poetry it should be named `baseten-infra-take-home...`. 
   To validate the path you can run, in your terminal `poetry env info`
5. Make your changes
6. Open the run and debug tab `⇧⌘D` and run `Run: Server`

### With makefile
```sh
# Install dependencies
make install
# Run Mock API Server:
make mock_server
# Run Real Server:
make start
# Run linters+formatters
make lint
```

## Libraries' Documentation

- Strawberry: https://strawberry.rocks/docs
- FastAPI: https://fastapi.tiangolo.com/
- AIOHTTP: https://docs.aiohttp.org/en/stable/
- Pydantic: https://pydantic-docs.helpmanual.io/

Feel free to replace any of those, we've provided a boilerplate to ease the start of the take home and save you some time.
