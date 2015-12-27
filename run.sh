
slide_pid=0

while :
do

python sad_daemon.py  -s 18000

if [ $slide_pid != 0 ] ; then
kill $slide_pid
fi

python google_speech.py rec.wav

prefix=`date +"%Y%m%d_%H%M%S"`
python google_image.py `cat transcript.txt` $prefix


./publish_slideshow.sh $prefix

slide_pid=$!

done

