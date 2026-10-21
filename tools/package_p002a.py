"""Ship a standalone offline safety-fix tool; no ROM or save content in ZIP."""
import hashlib
import json
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def game_hash(data):
    return hashlib.sha256(data[:0xC80000]+data[0xCA0000:0x1000000]).hexdigest()


def main():
    before=(ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes()
    after=(ROOT/'builds/dev/Liquid Crystal P002a.gba').read_bytes()
    proof=json.loads((ROOT/'extracted/runtime/stadium/summary.json').read_text())['cases']['p002a']
    if not proof['complete']or proof['rom_sha256']!=hashlib.sha256(after).hexdigest():raise ValueError('Hotfix not tested')
    config={'p002GameSha256':game_hash(before),'p002aGameSha256':game_hash(after)}
    html=(ROOT/'tools/p002a_patcher.html').read_text().replace('__CONFIG__',json.dumps(config))
    readme='''P002a SAFETY FIX — KEEP YOUR CURRENT SAVE

The warehouse's old east-facing stairs enter an unused multiplayer Colosseum.
P002a blocks that stair. Use the damaged sign after winning Mister R to enter
the Office service room. The new chapter ends there; the stadium is not a story
battle. The inherited chair route can start invalid/stalled link interactions.

1. Back up your CURRENT save and ROM with FlashGBX. Keep the originals.
2. Open Make-Safety-Fix.html in Chrome, Edge or Firefox.
3. Select that fresh16 or32 MiB ROM dump and current128 KiB .sav backup.
4. Click Create, then Download P002a-keep-progress.gba.
5. Use your already-working FlashGBX procedure, retaining/restoring that CURRENT
   save as your cartridge requires. Do not substitute the pre-puzzle test save.

This changes one map collision word and embeds your chosen current save in a
copy; it preserves16/32 MiB size and upper-bank bytes. No driver, item, battle,
flag, variable or save format changes. Both save slots are checked with native
LC checksum lengths. The page stops if saved in the broken stadium or if save
data is invalid; send that backup for recovery rather than overwriting it.
The fix does not recover unsaved progress. Everything runs offline; no uploads.
The original ROM/save files stay unchanged. No new hardware compatibility claim.

The BPS files here are an alternative ONLY for the exact standard P002/P002a
builds. They do not embed your latest progress. Use the HTML tool for a cart
dump or a ROM with a different embedded save.
'''
    folder=ROOT/'patches/P002a';folder.mkdir(exist_ok=True)
    files={'Make-Safety-Fix.html':html.encode(),'README.txt':readme.encode(),
           'P002-to-P002a.bps':(ROOT/'builds/dev/P002-to-P002a.bps').read_bytes(),
           'P002a-to-P002.bps':(ROOT/'builds/dev/P002a-to-P002.bps').read_bytes(),
           'MANIFEST.json':(ROOT/'extracted/builds/P002a-manifest.json').read_bytes()}
    files['WALKTHROUGH.md']=(ROOT/'WALKTHROUGH.md').read_bytes()
    for image in (ROOT/'walkthrough/images').iterdir():
        if image.suffix in ('.png','.svg'):files[str(image.relative_to(ROOT))]=image.read_bytes()
    browser_report=ROOT/'extracted/builds/P002a-browser-validation.json'
    if browser_report.exists() and json.loads(browser_report.read_text()).get('html_sha256')==hashlib.sha256(html.encode()).hexdigest():
        files['BROWSER-VALIDATION.json']=browser_report.read_bytes()
    files['SHA256SUMS.txt']=''.join(f'{hashlib.sha256(data).hexdigest()}  {name}\n'for name,data in sorted(files.items())).encode()
    path=folder/'P002a-safety-fix.zip'
    with zipfile.ZipFile(path,'w')as archive:
        for name,data in files.items():
            info=zipfile.ZipInfo(name,(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;archive.writestr(info,data)
    with zipfile.ZipFile(path)as archive:
        if archive.testzip()is not None:raise ValueError('ZIP integrity failure')
    print(path, path.stat().st_size)


if __name__=='__main__':main()
