LOCK_FILE=slideshow.lock
PID_FILE=slideshow.pid
DIR_FILE=slideshow.dir

if ! ln -s $$ $LOCK_FILE; then
	echo "already started"
	exit 0
fi

while :
do
if [ ! -e $DIR_FILE ] ; then
echo "$DIR_FILE does not exist"
break
fi

dir=`cat $DIR_FILE`
feh -F -D 1 -Z $dir
# debug
#feh -D 1 $dir &

pid=$!
echo $pid > $PID_FILE

wait
rm -f $PID_FILE

done

rm -f $LOCK_FILE
exit 0

