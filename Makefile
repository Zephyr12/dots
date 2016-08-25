theme:
	rm configs -r
	./themer.py
	xrdb -all ~/.dots/configs/Xresources
	i3-msg restart
