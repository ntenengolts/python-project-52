#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

make install

source /opt/render/project/.venv/bin/activate

make collectstatic && make migrate

