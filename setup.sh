#!/bin/bash

PYTHON_PATH=`which python`
if [ $PYTHON_PATH != "" ]
    then
        easy_install virtualenv
        virtualenv -p $PYTHON_PATH --no-site-packages --distribute --prompt=[cdmaker-env] .env
        pip install -E .env -r requirements.txt
    else
        echo "Can't find Python executable."
fi
