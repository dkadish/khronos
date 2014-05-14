#!/bin/bash
# Creates intermediate frames and then video

cd $1

mkdir temp

ls -v *.jpg > filenames.txt
split -l 10 filenames.txt FILENAMES

lastline=""

for f in FILENAMES*
do
   [ ! -z "$lastline" ] && echo "$lastline"|cat - $f > /tmp/out && mv /tmp/out $f
   echo "$f"
   #echo "\n"
   #head -n100 $f
   #echo "\n"
   #tail -n1 $f
   convert @$f -morph 30 -scene `ls -1 temp/ | wc -l` temp/%05d.jpg
   lastline=`tail -n1 $f`
   #echo $lastline
done

rm filenames.txt
rm FILENAMES*

ffmpeg -r 60 -i temp/%05d.jpg output.mp4
