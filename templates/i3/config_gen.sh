#! /bin/zsh
cols=($({ echo "$1" ; extractcolors -n 10 "$1"; } | ~/.i3/color_chooser.py))
echo "$cols"
pres=('$bg' '$acc_n' '$acc_u' '$fg')
for ind in {1..4}; do
        echo "set ${pres[$ind]} ${cols[$ind]}"
done
echo "exec_always feh --bg-scale $1"
cat ~/.i3/config_template
