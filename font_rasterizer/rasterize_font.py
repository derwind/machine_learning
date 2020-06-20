#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import numpy as np
from fontTools.ttLib import TTFont
import freetype
from PIL import Image
from typing import List, Set

class Rasterizer(object):
    def __init__(self, in_font, gids, size, inverse):
        self.in_font = in_font
        self.gids = self.expand_gids(gids)
        self.size = size
        self.inverse = inverse

    def run(self):
        metrics = self.load_font_metrics()
        face = freetype.Face(self.in_font)
        face.set_char_size(self.size*64) # '*64' means '<<6' (bitwise shift) because type of width is F26Dot6
        for gid in self.gids:
            self.save_image(face, gid, metrics)

        return 0

    def save_image(self, face, gid, metrics):
        face.load_glyph(gid)
        bitmap = face.glyph.bitmap
        width, height, pitch = bitmap.width, bitmap.rows, bitmap.pitch
        left, top = face.glyph.bitmap_left, face.glyph.bitmap_top
        shift = -metrics["descender"] * self.size // metrics["unitsPerEm"]
        W, H = self.size, self.size
        Z = np.zeros( (H, W), dtype=np.ubyte )
        buff = np.array(bitmap.buffer, dtype=np.ubyte).reshape((height, pitch))
        Z[H-(top+shift):H-(top+shift)+height,left:left+width].flat |= buff[:,:width].flatten()
        if not self.inverse:
            Z = 0xff - Z
        im = Image.fromarray(Z, mode="L")
        im.save(f"g{gid}.png", "PNG")

    def load_font_metrics(self) -> dict:
        metrics = {"unitsPerEm":0, "ascender":0, "descender":0}
        ttFont = TTFont(self.in_font)
        metrics["unitsPerEm"] = ttFont["head"].unitsPerEm
        metrics["ascender"] = ttFont["OS/2"].sTypoAscender
        metrics["descender"] = ttFont["OS/2"].sTypoDescender
        return metrics

    def expand_gids(self, gids:str) -> Set[int]:
        gset = set()
        for elem in gids.split(","):
            if "-" in elem:
                start, end = [int(s) for s in elem.split("-")]
                gset |= set(range(start, end+1))
            else:
                gset.add(int(elem))
        return gset

    def compact_gids(self, gids:List[int]) -> str:
        cgids = []
        s = e = -1
        for gid in sorted(gids):
            if e < 0:
                s = e = gid
                continue

            if gid == e + 1:
                e = gid
            else:
                if s == e:
                    cgids.append(str(s))
                else:
                    cgids.append("{}-{}".format(s, e))
                s = e = gid

        if s == e:
            cgids.append(str(s))
        else:
            cgids.append("{}-{}".format(s, e))

        return ",".join(cgids)

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gids", dest="gids", metavar="GIDs", type=str, required=True, help="GIDs")
    parser.add_argument("--size", dest="size", metavar="SIZE", type=int, default=1000, help="size of rasterized glyphs")
    parser.add_argument("--inverse", dest="inverse", action="store_true", help="inverse black and white")
    parser.add_argument("in_font", metavar="IN_FONT", type=str, help="input font")

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    tool = Rasterizer(args.in_font, args.gids, args.size, args.inverse)
    sys.exit(tool.run())

if __name__ == "__main__":
    main()
