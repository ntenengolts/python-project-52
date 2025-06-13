#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv --version

uv venv

make install && make collectstatic && make migrate

