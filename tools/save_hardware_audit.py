"""Record the supplied image's cartridge save conversion, without ROM writes."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WINDOW=(0xC80000,0xCA0000)
SIGNATURES={0x1DE828:bytes.fromhex('c0 46'),0x1DE840:bytes.fromhex('01 21 c7 08'),
            0xC7213C:bytes.fromhex('00 00 00 09'),0xD9748:bytes.fromhex('41 21 c7 08')}


def audit(rom,save):
    for at,expected in SIGNATURES.items():
        if rom[at:at+len(expected)]!=expected:raise ValueError(f'Cartridge conversion signature changed at {at:X}')
    embedded=rom[slice(*WINDOW)]
    return {'source_rom_sha256':hashlib.sha256(rom).hexdigest(),'source_save_sha256':hashlib.sha256(save).hexdigest(),
            'embedded_window':{'start':WINDOW[0],'end_exclusive':WINDOW[1],'bytes':len(embedded),
                               'sha256':hashlib.sha256(embedded).hexdigest(),'equals_source_save_payload':embedded==save[:0x20000]},
            'native_signatures':[{'offset':at,'hex':value.hex()} for at,value in SIGNATURES.items()],
            'bank_port':0x09000000,'sram_window':0x0E000000,
            'interpretation':'Image-specific cartridge conversion: boot restores embedded NOR save into banked SRAM; game saving updates SRAM then programs the embedded NOR window. Not a claim about unmodified Liquid Crystal releases.',
            'adapter_limits':'Functional immediate writes for the observed AMD fallback NOR command path, with a private in-memory save window and disposable file. Not hardware, timing, chip-ID or every flashcart protocol certification.'}


def main():
    result=audit((ROOT/'roms/POKEMON Liquid Crystal.gba').read_bytes(),(ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav').read_bytes())
    (ROOT/'extracted/runtime/save_hardware.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
