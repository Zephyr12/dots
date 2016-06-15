#! /usr/bin/env python
import fileinput
from PIL import Image
from PIL import ImageStat

def is_bright(img_loc):
    im = Image.open(img_loc.strip()).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0] > 200

if __name__ == "__main__": 
    lines = []
    for line in fileinput.input():
        lines.append(line)
    bright = is_bright(lines[0])
    lines = lines[1:]
    len_lines = len(lines)-1
    approx_color_percs = [1, 0.4,0.6,0] if bright else [0, 0.4, 0.6, 1]
    color_indices = map(lambda x: int(x*len_lines), approx_color_percs)
    for index in color_indices:
        print (lines[index])
