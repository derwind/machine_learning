#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import numpy as np
import freetype
from PIL import Image
from typing import List, Set

class Rasterizer(object):
    def __init__(self, in_font:str, gids:Set[int], size:int, inverse:bool=False, rgb:bool=False):
        self.in_font = in_font
        self.gids = gids
        self.size = size
        self.inverse = inverse
        self.rgb = rgb

    def run(self):
        face = freetype.Face(self.in_font)
        face.set_char_size(self.size*64) # '*64' means '<<6' (bitwise shift) because type of width is F26Dot6
        for gid in self.gids:
            self.save_image(face, gid)

        return 0

    def save_image(self, face, gid):
        W, H = self.size, self.size
        Z = np.zeros( (H, W), dtype=np.ubyte )

        face.load_glyph(gid)
        bitmap = face.glyph.bitmap
        x, y = face.glyph.bitmap_left, face.glyph.bitmap_top
        w, h, p = bitmap.width, bitmap.rows, bitmap.pitch
        shift = -face.descender * self.size // face.units_per_EM
        y += shift

        buff = np.array(bitmap.buffer, dtype=np.ubyte).reshape((h,p))
        Z[H-y:H-y+h,x:x+w].flat |= buff[:,:w].flatten()
        if not self.inverse:
            Z = 0xff - Z
        im = Image.fromarray(Z, mode="L")
        if self.rgb:
            im = im.convert("L").convert("RGB")
        #print(np.asarray(im, np.uint8).shape)
        im.save(f"g{gid}.png", "PNG")

def expand_gids(gids:str) -> Set[int]:
    gset = set()
    for elem in gids.split(","):
        if "-" in elem:
            start, end = [int(s) for s in elem.split("-")]
            gset |= set(range(start, end+1))
        else:
            gset.add(int(elem))
    return gset

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gids", dest="gids", metavar="GIDs", type=str, required=True, help="GIDs")
    parser.add_argument("--size", dest="size", metavar="SIZE", type=int, default=1000, help="size of rasterized glyphs")
    parser.add_argument("--inverse", dest="inverse", action="store_true", help="inverse black and white")
    parser.add_argument("--rgb", dest="rgb", action="store_true", help="save as RGB image")
    parser.add_argument("in_font", metavar="IN_FONT", type=str, help="input font")

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    tool = Rasterizer(args.in_font, expand_gids(args.gids), args.size, args.inverse, args.rgb)
    sys.exit(tool.run())

if __name__ == "__main__":
    main()
