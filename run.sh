#!/bin/bash
set -e

source .env/bin/activate
python server.py

cd -> /dev/null
