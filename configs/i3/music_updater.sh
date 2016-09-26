#! /bin/bash

while :;
do
		mpc idle
		pkill -RTMIN+1 i3blocks
done