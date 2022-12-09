#!/bin/bash
F=C:/Users/Leilani/Documents/transaction.txt
# move txid into transaction.txt
echo ${1} >> ${F}
# copy transaction.txt to pi
pscp -pw "raspberryp!123" C:/Users/Leilani/Documents/transaction.txt pi@192.168.1.205:transaction.txt
# turn wifi on
ssh pi@192.168.1.205 "sudo ifconfig wlan0 up"
# wifi will be on for 60 seconds
sleep 60
# turn wifi off
ssh pi@192.168.1.205 "sudo ifconfig wlan0 down"