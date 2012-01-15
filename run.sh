#!/usr/bin/env bash
LOGFILE=execution.log

[[ -f $LOGFILE ]] | touch $LOGFILE

( tail -f $LOGFILE & echo $! >&3 ) 3>pid

source .env/bin/activate
python server.py > /dev/null 2>&1

kill $(<pid)
