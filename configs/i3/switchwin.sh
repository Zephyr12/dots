#! /bin/zsh
winid="$(wmctrl -l | cut -d" " -f1,5- | dmenu | cut -d' ' -f1)"
echo $winid
if [[ -z "$winid" ]];then
        echo $winid
fi