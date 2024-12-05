#!/bin/sh

notif="/storage/emulated/0/Music/mmp/adb_notif"
vlc="org.videolan.vlc"
timeout=1

touch $notif

while true; do
    sleep 1

    current_time=$(date +%s)
    notif_time=$(stat -c %Y $notif)

    if [ $(($current_time - $notif_time)) -ge 3 ]; then
        am force-stop $vlc
        break
    fi
done
