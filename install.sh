#!/usr/bin/env bash

DIR="$( cd "$( dirname "${0}" )" && pwd )"

# install pip dependencies

cd ${DIR}

virtualenv -p python2.7 "${DIR}/.venv/ponyexpress"

source "${DIR}/.venv/ponyexpress/bin/activate"

pip install -r "${DIR}/requirements.txt"

python setup.py install

${DIR}/bin/ponyexpress db upgrade -d ponyexpress/migrations

exit 0
