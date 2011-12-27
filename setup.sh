#!/bin/bash

PYTHON_PATH=`which python2.7`
if [ $PYTHON_PATH != "" ]
    then
        virtualenv -p $PYTHON_PATH --no-site-packages --distribute --prompt=[cdmaker-env] .env
        pip install -E .env -r requirements.txt
    else
        echo "Can't find Python2.7 executable."
fi
