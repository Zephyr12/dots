#! /usr/bin/env python


import mimetypes
import shutil
import sys
import os
import yaml
import colorsys
import math
import jinja2
import pdb
from PIL import Image

def clamp_value(col, low, high):
    hsv = list(colorsys.rgb_to_hsv(*col))
    new_value = max(min(hsv[2], high), low)
    hsv[2] = max(min(hsv[2], high), low)
    col = tuple(int(255*i) for i in colorsys.hsv_to_rgb(*hsv))
    return col

def clamp_sat(col, low, high):
    hsv = list(colorsys.rgb_to_hsv(*col))
    new_value = max(min(hsv[1], high), low)
    hsv[1] = max(min(hsv[1], high), low)
    col = tuple(int(i) for i in colorsys.hsv_to_rgb(*hsv))
    return col

def tohex(r, g, b):
    hexchars = "0123456789ABCDEF"
    return ("#"
            + hexchars[r // 16]
            + hexchars[r % 16]
            + hexchars[g // 16]
            + hexchars[g % 16]
            + hexchars[b // 16]
            + hexchars[b % 16])


def get_n_colors(filename, n):
    img = Image.open(filename)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.convert("P", palette=Image.ADAPTIVE, colors=n)
    img = img.convert("RGB")
    return sorted(img.getcolors(n), reverse=True)


def deduplicate(cols, delta=10):
    results = {}
    for col in cols:
        for res in results:
            if contrast(col, res) > delta:
                results[col] = 1
                break
            else:
                results[res] += 1
        else:
            results[col] = 1

    return [col for col, count in sorted([(col, count) for col, count in  results.items()], key=lambda x: x[1])][::-1]


def average(a, b):
    return (int((a[0] + b[0])*0.5), int((a[1] + b[1])*0.5), int((a[2] + b[2])*0.5))

def hue_shift(col, to, by):
    hsv_col = colorsys.rgb_to_hsv(*col)
    hsv_to = colorsys.rgb_to_hsv(*to)
    return colorsys.hsv_to_rgb(
        hsv_col[0]*(1-by) + hsv_to[0]*(by),
        hsv_col[1],
        hsv_col[2])

def contrast(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)

def negate(a):
    return (255 - a[0], 255 - a[1], 255 - a[2])

canonical_colors = [
    ("black", (0, 0, 0)),
    ("red", (255, 0, 0)),
    ("green", (0, 255, 0)),
    ("blue", (0, 0, 255)),
    ("cyan", (0, 255, 255)),
    ("magenta", (255, 0, 255)),
    ("yellow", (255, 255, 0)),
    ("white", (255, 255, 255))
]

if __name__ == "__main__":
    context = yaml.safe_load(open("generic_settings.yaml"))
    colors = [col[1] for col in get_n_colors(context["background_img"], 75)]
    colors = deduplicate(colors)
    bg = colors[0]
    context["bg"] = tohex(*bg)
    fg =  sorted(colors, key=lambda col: contrast(col, bg))[-1]
    if contrast(fg, bg)< 30:
        fg = negate(fg)
    context["fg"] = tohex(*fg)
    
    for name, key in canonical_colors:
        col = sorted(colors, key=lambda col: contrast(col, key))[-1]
        colors.remove(col)
        col = clamp_value(clamp_sat(hue_shift(col, key, 0.3), 0.4, 0.8), 0.4, 0.6)
        context[name] = tohex(*col)

    all_paths = os
    for root, dirs, files in os.walk("."):
        for filename in files:
            path = os.path.join(root, filename)
            print(path)
            if not path.startswith("./template"):
                continue
            dest_root = root.replace("template", "config")
            dest = path.replace("template", "config")
            try:
                file = open(path)
                template = jinja2.Template(file.read())
                rendered_config = template.render(**context)
                try:
                    os.makedirs(dest_root)
                except:
                    pass
                outfile = open(dest, "w")
                outfile.write(rendered_config)
                shutil.copystat(path, dest)
            except UnicodeDecodeError:
                try:
                    os.makedirs(dest_root)
                except:
                    pass
                shutil.copy2(path, dest)
