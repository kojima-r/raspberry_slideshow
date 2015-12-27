LOCK_FILE=slideshow.lock
PID_FILE=slideshow.pid
DIR_FILE=slideshow.dir

if [ -e $DIR_FILE ] ; then
rm -f $DIR_FILE
fi

if [ -e $PID_FILE ] ; then
echo "kill `cat $PID_FILE`"
kill `cat $PID_FILE`
fi

