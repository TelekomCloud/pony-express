#!/usr/bin/env bash

# install pip dependencies
basepath=`pwd`

vendor="${basepath}/vendor"
if [ -d "${vendor}" ]
then

    virtualenv -p python2.7 "${basepath}/.venv/ponyexpress"

    source "${basepath}/.venv/ponyexpress/bin/activate"

    #pip install --no-index --find-links "${vendor}" -r requirements.txt
    pip install -r requirements.txt

    python setup.py install

    bin/ponyexpress db upgrade -d ponyexpress/migrations
fi