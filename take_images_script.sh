#!/bin/bash

#echo "" >> log_spoustec.txt
#echo "před sleepem: $(date)" >> log_spoustec.txt
#sleep 20
#echo "za sleepem: $(date)" >> log_spoustec.txt

#export DISPLAY=:0
#echo "display: $(date)" >> log_spoustec.txt

/usr/bin/python3 /home/ubuntu/prog/take_images/take_images.py

#echo "volani programu: $(date)" >> log_spoustec.txt

#while true
#do
#    echo 'start'
#    GDK_BACKEND=x11 /usr/bin/python3 /home/ubuntu/prog/take_images/take_images.py
#    echo 'konec'
#done