"""Draw a schematic Route59 guide from native tiles and retained walked positions."""
import hashlib
import json
from pathlib import Path
from p001_runtime import PatchJourney,ROM
from warp_graph import MapCatalog
ROOT=Path(__file__).resolve().parents[1]


def main():
    data=json.loads((ROOT/'extracted/runtime/p001/regression/regression.json').read_text())
    rom=ROM.read_bytes()
    if not data['complete']or data['rom_sha256']!=hashlib.sha256(rom).hexdigest():raise ValueError('Stale route evidence')
    p=object.__new__(PatchJourney);p.rom=rom;p.catalog=MapCatalog(rom);p.cells_cache={}
    m,cells=p.cells(3,110);route=[]
    for step in data['steps']:
        if step['map']!=[3,110]:continue
        if not route:route.append(step['from'])
        after=step['after']
        if (after['group'],after['map'])==(3,110):
            xy=[after['x'],after['y']]
            if xy!=route[-1]:route.append(xy)
    if route[0]!=[54,67]or route[-1]!=[11,23]:raise ValueError('Unexpected approach endpoints')
    scale=7;left=42;top=60
    result=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 730 660" role="img" aria-labelledby="title desc">',
            '<title id="title">Route 59: gatehouse to warehouse</title>',
            '<desc id="desc">Schematic native tile map with the actual tested approach. Start at the southern gatehouse and travel northwest to the warehouse, using Surf across water. North is up. This is not game artwork.</desc>',
            '<rect width="730" height="660" fill="#fff"/>',
            '<g font-family="sans-serif" fill="#152731"><text x="42" y="28" font-size="20" font-weight="bold">Route 59: gatehouse to warehouse</text><text x="42" y="48" font-size="12">North is up · schematic · Surf used on the tested route</text></g>']
    for (x,y),cell in cells.items():
        water=cell['behavior']in(0x10,0x11,0x12,0x15)
        color='#87bddb'if water else('#c4c9ca'if cell['collision']else'#e1e9d3')
        result.append(f'<rect x="{left+x*scale}" y="{top+y*scale}" width="7" height="7" fill="{color}"/>')
    points=' '.join(f'{left+(x+.5)*scale},{top+(y+.5)*scale}'for x,y in route)
    result.append(f'<polyline points="{points}" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/>')
    result.append(f'<polyline points="{points}" fill="none" stroke="#b02e58" stroke-width="2.5" stroke-linejoin="round"/>')
    for x,y,label,color in [(54,67,'START: gatehouse','#17644d'),(11,23,'WAREHOUSE','#b02e58')]:
        cx=left+(x+.5)*scale;cy=top+(y+.5)*scale
        result.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="{color}" stroke="#fff" stroke-width="2"/>')
        result.append(f'<text x="{cx+10}" y="{cy-8}" font-family="sans-serif" font-size="13" font-weight="bold" fill="#111" stroke="#fff" stroke-width="3" paint-order="stroke">{label}</text>')
    result.append('<g font-family="sans-serif" font-size="12" fill="#152731"><text x="42" y="582">Pink line: observed walking / Surf approach. Gray: blocked tiles.</text><text x="42" y="603">Blue: water. Pale green: other passable tiles. Doors and events still apply.</text><text x="42" y="632">From Mandarin City, leave the northern gatehouse onto Route 59.</text><text x="42" y="650">At the warehouse, face the door and press A to use the Old Key.</text></g></svg>')
    out=ROOT/'walkthrough/images/route59.svg';out.write_text('\n'.join(result)+'\n');print(out)


if __name__=='__main__':main()
