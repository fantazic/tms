#!/bin/sh
# Django Server for TMS
#
workdir=/home/ec2-user/tms
 
start() {
    cd $workdir
    nohup gunicorn app.wsgi >/dev/null 2>&1 &
    echo "Server started."
}
 
stop() {
    pid=`ps -ef | grep '/usr/local/bin/gunicorn app.wsgi' | grep -v 'grep' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 2
    echo "Server killed."
}
 
case "$1" in
  start)
    start "$2"
    ;;
  stop)
    stop "$2"  
    ;;
  restart)
    stop "$2"
    start "$2"
    ;;
  *)
    echo "Usage: tornado.sh {start|stop|restart}"
    exit 1
esac
exit 0
