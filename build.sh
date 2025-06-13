#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv --version

uv venv

us sync

make install && make collectstatic && make migrate

