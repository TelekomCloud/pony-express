#!/usr/bin/env bash

# install pip dependencies
basepath=`pwd`

source "${basepath}/.venv/ponyexpress/bin/activate"

bin/ponyexpress runserver --no-debug --no-reload -t 0.0.0.0 &