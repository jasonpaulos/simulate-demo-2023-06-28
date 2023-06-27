# Algorand 3.16 New Simulation Features Demo

This repo contains a demo of two new simulation features from [Algorand 3.16](https://github.com/algorand/go-algorand/releases/tag/v3.16.2-stable):
1. Increased app opcode budget
2. Higher app log limits

This demo is for the [Proof of State show on 2023.06.28](https://www.youtube.com/watch?v=ZtEcXs3i4N8).

## Development Setup

System Dependencies:

* Python 3.10 or higher
* Access to a running Algorand node (e.g. [sandbox](https://github.com/algorand/sandbox)) with Developer API enabled.

Set up Python virtual environment (one time):
* `python3 -m venv venv`

Activate virtual environment:
* `. venv/bin/activate` (bash/zsh shell)
* `. venv/bin/activate.fish` (fish shell)

Install package dependencies:
* `pip install -r requirements.txt`:

Run tests/demo:
* Ensure your Algorand node is running.
* Set the environment variables `ALGOD_ADDRESS` and `ALGOD_TOKEN` to the address and token of the node.
* Set the environment variable `ACCOUNT_MNEMONIC` to the mnemonic of an account on the node's network.
* Run `pytest src -s` (the `-s` flag is needed to show output)

Other useful commands:
* Format code: `black src`
* Type check code: `mypy src`
