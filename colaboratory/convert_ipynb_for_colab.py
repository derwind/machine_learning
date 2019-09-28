#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
convert .ipynb for jupyter to that for Google Colaboratory, i.e. image files referenced by img are assumed under /usr/local/share/jupyter/nbextensions/
"""

import os, sys, re

def main():
    path = sys.argv[1]
    dirname = os.path.dirname(path)
    basename, ext = os.path.splitext(os.path.basename(path))
    out_path = os.path.join(dirname, "{}_colab{}".format(basename, ext))

    lines = []
    with open(path) as fin:
        for line in fin.readlines():
            line = line.rstrip()
            if re.search(r"img.*src", line):
                lines[-1] = re.sub(r"\s*,\s*$", "", lines[-1])

                line = re.sub(r"\s*,\s*$", "", line)
                line = re.sub(r"'(\S+)'", r"'/nbextensions/\1'", line)
                line = re.sub(r"\\\"(\S+)\\\"", r"\"/nbextensions/\1\"", line)
                lines.append('   ]\n  },\n  {\n   "cell_type": "code",\n   "metadata": {},\n   "source": [\n    "%%html\\n",')
                lines.append(line)
                lines.append('   ]\n  },\n  {\n   "cell_type": "markdown",\n   "metadata": {},\n   "source": [')
            else:
                lines.append(line)
    with open(out_path, "w") as fout:
        for line in lines:
            print(line, file=fout)

if __name__ == "__main__":
    main()
