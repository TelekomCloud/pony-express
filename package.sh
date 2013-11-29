#!/usr/bin/env bash

# Package pip dependencies

project_name="pony-express"
basepath=`pwd`

project_path="${basepath}/../${project_name}"

if [ -d "${project_path}" ]
then
    vendor="${project_path}/vendor"

    mkdir -p "${vendor}"

    pip install --download "${vendor}" -r requirements.txt

    #cleanup
    rm -r "${project_path}/build/"
    rm -r "${project_path}/dist/"
    rm -r "${project_path}/*.egg-info/"

    cd "${project_path}/../"

    tar cvzf pony-express.tar.gz --exclude=.git --exclude=.idea pony-express

fi