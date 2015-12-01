#!/bin/sh 
WID=`xdotool search --name "Indiana" | head -1`
for room in "$@"
do 
  echo $room
  xdotool windowfocus $WID
  xdotool key "Escape"
  xdotool key ctrl+d
  sleep 1
  xdotool type "room $room"
  xdotool key "Return"
  sleep 2
  import -screen -window $WID $room.png
  sleep 2
done
