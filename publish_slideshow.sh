LOCK_FILE=slideshow.lock
PID_FILE=slideshow.pid
DIR_FILE=slideshow.dir


dir=$1
if [ -d $dir ] ; then
echo $dir > $DIR_FILE
else
echo "target directory does not exist"
exit 0
fi

if [ -e $PID_FILE ] ; then
kill `cat $PID_FILE`
fi

if [ ! -L $LOCK_FILE ] ; then
echo "start slideshow!"
./start_slideshow.sh &
fi

