#!/usr/bin/env bash

DIR="$( cd "$( dirname "${0}" )" && pwd )"

# install pip dependencies

vendor="${DIR}/vendor"
if [ -d "${vendor}" ]
then

    virtualenv -p python2.7 "${DIR}/.venv/ponyexpress"

    source "${DIR}/.venv/ponyexpress/bin/activate"

    #pip install --no-index --find-links "${vendor}" -r requirements.txt
    pip install -r requirements.txt

    python setup.py install

    $DIR/bin/ponyexpress db upgrade -d ponyexpress/migrations
fi
