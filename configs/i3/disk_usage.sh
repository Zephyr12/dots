#!/bin/bash
disk_gb=$(df -hP / | grep -v File | tr -s ' ' | cut -d' ' -f3)
disk_perc=$(df -hP / | grep -v File | tr -s ' ' | cut -d' ' -f5 | head -c -2)
# the -2 is for the line feed
echo "$disk_gb ($disk_perc%)"
echo "$disk_perc%"

if [ $disk_perc -gt 70 ]
then
    echo "#B2A38E"
elif [ $disk_perc -gt 50 ]
then
    echo "#B2B28E"
else
    echo "#8EB28E"
fi