theme:
	rm configs -r
	./themer.py
	xrdb -all ~/.Xresources
	i3-msg restart