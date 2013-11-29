#!/usr/bin/env bash

# Package pip dependencies

DIR="$( cd "$( dirname "${0}" )" && pwd )"

vendor="${DIR}/vendor"

mkdir -p "${vendor}"

pip install --download "${vendor}" -r requirements.txt

#cleanup
rm -r "${DIR}/build/"
rm -r "${DIR}/dist/"
rm -r "${DIR}/*.egg-info/"

cd $DIR

tar cvzf ../pony-express.tar.gz --exclude=.git --exclude=.idea .
