#! /usr/bin/env sh

scrot ~/.i3/lockimg.png
mpc pause
convert ~/.i3/lockimg.png -resize 25% -blur 0x10 -resize 400% ~/.i3/lockimg.png
i3lock -i ~/.i3/lockimg.png -u -e
rm ~/.i3/lockimg.png


