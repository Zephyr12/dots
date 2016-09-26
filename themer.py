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
    hsv[2] = sorted((low, hsv[2], high))[1]
    return colorsys.hsv_to_rgb(*hsv)


def clamp_sat(col, low, high):
    hsv = list(colorsys.rgb_to_hsv(*col))
    hsv[1] = sorted((low, hsv[1], high))[1]
    return colorsys.hsv_to_rgb(*hsv)


def tohex(r, g, b):
    hexchars = "0123456789ABCDEF"
    r = int(r*255)
    g = int(g*255)
    b = int(b*255)

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


def delta_hue(a, b):
    hsv_a = colorsys.rgb_to_hsv(*a)
    hsv_b = colorsys.rgb_to_hsv(*b)
    return abs(hsv_a[0] - hsv_b[0])


def average(a, b):
    return ((a[0] + b[0])*0.5, (a[1] + b[1])*0.5, (a[2] + b[2])*0.5)


def clamp_hue(col, to, by):
    hsv_col = list(colorsys.rgb_to_hsv(*col))
    hsv_to = colorsys.rgb_to_hsv(*to)
    hsv_col[0] = sorted((hsv_to[0] - by, hsv_col[0], hsv_to[0] + by))[1]
    return colorsys.hsv_to_rgb(*hsv_col)


def contrast(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def negate(a):
    return (1 - a[0], 1 - a[1], 1 - a[2])

canonical_colors = [
    ("black", (0, 0, 0)),
    ("red", (1.0, 0, 0)),
    ("green", (0, 1.0, 0)),
    ("blue", (0, 0, 1.0)),
    ("cyan", (0, 1.0, 1.0)),
    ("magenta", (1.0, 0, 1.0)),
    ("yellow", (1.0, 1.0, 0)),
    ("white", (1.0, 1.0, 1.0))
]

if __name__ == "__main__":
    context = yaml.safe_load(open("generic_settings.yaml"))
    colors = [col[1] for col in get_n_colors(context["background_img"], 255)]
    colors = [(r/255, g/255, b/255) for r,g,b in colors]
    colors = deduplicate(colors, delta=10)
    print(colors)
    bg = colors[0]
    context["bg"] = tohex(*bg)
    fg =  sorted(colors, key=lambda col: contrast(col, bg))[-1]
    if contrast(fg, bg) < 0.3:
        fg = negate(fg)
    context["fg"] = tohex(*fg)

    for name, target in canonical_colors:
        print ("\n\n")
        cols = sorted(colors, key=lambda col: delta_hue(col, target))
        print(tohex(*target))
        print()
        for candidate in cols:
            print(tohex(*candidate))
        col = cols[0]
        colors.remove(col)
        col = clamp_value(clamp_sat(col, 0.2, 0.8), 0.4, 0.7)

        context[name] = tohex(*col)

    all_paths = os
    for root, dirs, files in os.walk("."):
        for filename in files:
            path = os.path.join(root, filename)
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
