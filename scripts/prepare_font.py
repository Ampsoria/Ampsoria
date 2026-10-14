#!/usr/bin/env python3
"""One-time font preparation. Requires fonttools; daily builds do not."""
import json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

root = Path(__file__).resolve().parents[1]
source = root / 'assets/fonts/Nunito.ttf'
result = {}
for weight in (600, 800):
    font = instantiateVariableFont(TTFont(source), {'wght': weight}, inplace=True)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    chars = ''.join(chr(n) for n in range(32, 127)) + '·—–…↑♥✿'
    entries = {}
    for char in chars:
        if ord(char) not in cmap:
            continue
        name = cmap[ord(char)]
        pen = SVGPathPen(glyphs, ntos=lambda n: str(round(n, 2)))
        glyphs[name].draw(pen)
        entries[char] = {'advance': font['hmtx'][name][0], 'path': pen.getCommands()}
    result[str(weight)] = {'units': font['head'].unitsPerEm, 'glyphs': entries}
(root / 'assets/fonts/glyphs.json').write_text(json.dumps(result, separators=(',', ':')) + '\n')
print('Prepared Nunito glyph outlines at weights 600 and 800')
