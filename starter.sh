#!/usr/bin/env bash

DIR="$( cd "$( dirname "${0}" )" && pwd )"

# install pip dependencies

source "${DIR}/.venv/ponyexpress/bin/activate"

$DIR/bin/ponyexpress runserver --no-debug --no-reload -t 0.0.0.0 -p 5555 &

exit 0
