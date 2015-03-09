#!/bin/bash

# kill current process
kill -9 `ps -ef | grep 'manage.py celeryd' | grep -v grep | awk '{print $2}'`
sleep 5

# run celery process
RUN=`dirname $0`
python $RUN/../dian/manage.py celeryd -B -l INFO -f /tmp/rabbitmq.log -c 10 &
