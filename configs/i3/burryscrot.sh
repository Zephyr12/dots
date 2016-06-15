#! /usr/bin/env sh

scrot ~/.i3/lockimg.png
mpc pause
convert ~/.i3/lockimg.png -blur 0x10 ~/.i3/lockimg.png
i3lock -i ~/.i3/lockimg.png -u -e
rm ~/.i3/lockimg.png


