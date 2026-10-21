"""Read-only checksum/driver audit for this Liquid Crystal cartridge image.

Uses the pinned ROM's native layout table, not vanilla FireRed's sector sizes.
No repairs, resigning, source writes or physical-hardware certification.
"""
import hashlib
import json
import struct
from pathlib import Path
from verify_sources import checksum
from save_hardware_audit import SIGNATURES

ROOT = Path(__file__).resolve().parents[1]
TABLE = 0x3FEC94
LAYOUT = '0000240f0000f00ff00ff00fe01ff00fd02f980d0000f00ff00ff00fe01ff00fd02ff00fc03ff00fb04ff00fa05ff00f906ff00f807f5004'
CONSUMER = 0xDA1D4


def audit(rom, save):
    table = bytes.fromhex(LAYOUT)
    if rom[TABLE:TABLE+56] != table or rom[0xDA23C:0xDA240] != struct.pack('<I', 0x08000000+TABLE):
        raise ValueError('Unexpected native save-layout identity')
    if rom[0xDA1DA:0xDA1E8] != bytes.fromhex('184a118800684018186050889880'):
        raise ValueError('Unexpected native save-layout consumer')
    if len(save) not in (0x20000, 0x20010):
        raise ValueError('Expected 128 KiB save, optionally with FlashGBX footer')
    sizes = [struct.unpack_from('<HH', table, 4*i)[1] for i in range(14)]
    slots = []
    for slot in range(2):
        sections = []
        for i in range(14):
            at = (slot*14+i)*0x1000
            sid, stored, signature, generation = struct.unpack_from('<HHII', save, at+0xFF4)
            calculated = checksum(save[at:at+sizes[sid]]) if sid < 14 else None
            sections.append({'physical_sector': slot*14+i, 'id': sid, 'generation': generation,
                             'stored_checksum': stored, 'calculated_checksum': calculated,
                             'valid': sid < 14 and stored == calculated and signature == 0x08012025})
        slots.append({'slot': slot, 'all_ids_once': sorted(s['id'] for s in sections) == list(range(14)),
                      'all_checksums_and_signatures_valid': all(s['valid'] for s in sections),
                      'generations': sorted(set(s['generation'] for s in sections)), 'sections': sections})
    return {'save_sha256': hashlib.sha256(save[:0x20000]).hexdigest(), 'native_layout_table': TABLE,
            'consumer_literal_site': 0xDA23C, 'section_lengths': sizes,
            'driver_signatures_match': all(rom[at:at+len(data)] == data for at, data in SIGNATURES.items()),
            'slots': slots, 'all_28_sections_valid': all(s['all_ids_once'] and s['all_checksums_and_signatures_valid'] for s in slots),
            'limits': 'Static native-layout checksum/driver check. Does not show what a real cartridge read or programmed, certify native timing/chip compatibility, or repair data.'}


def main():
    rom = (ROOT/'builds/dev/Liquid Crystal P002.gba').read_bytes()
    result = {'user_hardware_report': 'Boot corruption/previous-save warning, then stuck on Saving',
              'root_cause': 'Unknown; original saves on the same cart (user confirmed); actual failed-cart readback needed',
              'hardware': 'FlashGBX5.0.1; GBxCart RWv1.4a/b/c family; AGB-E20-30/S29GL256N10TFI01 (or compatible);32 MiB; unknown save ID0x8209',
              'hardware_acceptance': 'failed as reported', 'same_cart_original_saving_baseline': 'works, user confirmed',
              'source_save': audit(rom, (ROOT/'saves/source/POKEMON Liquid Crystal DD 5 badge.sav').read_bytes()),
              'packaged_warehouse_save': audit(rom, (ROOT/'saves/test/P002-cart-puzzle.sav').read_bytes())}
    if not all(result[k]['all_28_sections_valid'] for k in ('source_save', 'packaged_warehouse_save')):
        raise ValueError('Save checksum audit failed')
    path = ROOT/'extracted/runtime/cartridge/hardware_failure_audit.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('source_save', 'packaged_warehouse_save')}, indent=2))
    print('Both source and packaged save pass all 28 native-layout sector checks.')


if __name__ == '__main__':
    main()
