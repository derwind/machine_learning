#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
convert .ipynb for jupyter to that for Google Colaboratory, i.e. image files referenced by img are assumed under /usr/local/share/jupyter/nbextensions/
"""

import os, sys, re

def insert_code_cell_between_markdowns(lines, line, prefix=""):
    lines[-1] = re.sub(r"\s*,\s*$", "", lines[-1])

    lines.append(f'   ]\n  }},\n  {{\n   "cell_type": "code",\n   "metadata": {{}},\n   "source": [{prefix}')
    lines.append(line)
    lines.append('   ]\n  },\n  {\n   "cell_type": "markdown",\n   "metadata": {},\n   "source": [')

def proc_img_line(lines, line):
    line = re.sub(r"\s*,\s*$", "", line)
    line = re.sub(r"'(\S+)'", r"'/nbextensions/\1'", line)
    line = re.sub(r"\\\"(\S+)\\\"", r"\"/nbextensions/\1\"", line)

    insert_code_cell_between_markdowns(lines, line, prefix='\n    "%%html\\n",')

def proc_img_line2(lines, line):
    """
    A helper function like below is assumed to be defined in advance:

    def display_image(url):
        from IPython.display import Image, display
        url = os.path.join(root_dir, url)
        display(Image(url))
    """

    m = re.search(r"'(\S+)'", line)
    if m:
        url = m.group(1)
        line = f'    "display_image(\\\"{url}\\\")"'

    insert_code_cell_between_markdowns(lines, line)

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
                proc_img_line2(lines, line)
            else:
                lines.append(line)
    with open(out_path, "w") as fout:
        for line in lines:
            print(line, file=fout)

if __name__ == "__main__":
    main()
