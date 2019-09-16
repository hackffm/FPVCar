#!/bin/bash
#
### BEGIN INIT INFO
# Description:      
# location: /etc/init.d/fpvcar
### END INIT INFO

workdir=/home/pi/git/FPVCar/webserver_tornado/

start() {
   echo "start fpvcar"
   cd $workdir
   python3 server.py &
}

stop() {
   echo "stop fpvcar"
   cd $workdir
   pid=`ps -ef | grep '[s]erver.py' | awk '{ print $2 }'`
   echo $pid
   kill $pid
}

# Actions
case "$1" in
    start)
        start
        ;;
    stop)
        # STOP
	stop
        ;;
    restart)
        # RESTART
	echo "restart fpvcar"
	stop
	start
        ;;
    *)
	echo "Usage: /etc/init.d/fpvcar {start|stop|restart}"
	exit 1
esac

exit 0