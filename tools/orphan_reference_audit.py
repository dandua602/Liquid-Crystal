"""Supplement the frozen 64 weak-reference text candidates; never infer reachability.

Reads the ROM and frozen input, validates each evidence claim, and writes a
deterministic report. The named offsets are investigation anchors, not a ROM
format signature or an orphan/unused-content detector.
"""
import hashlib
import json
import struct
from collections import Counter, defaultdict
from pathlib import Path

from gba_text_codec import parse
from pointer_scan import classify_operand, index_pointers

ROOT = Path(__file__).resolve().parents[1]
TRAINER_BASE = 0xABFD84
TRAINER_STRIDE = 40
ITEM_BASES = (0x3DB028, 0x9990AC)
ITEM_STRIDE = 44
CLASS_BASE = 0x23E558
CLASS_STRIDE = 13

# All peers are checked against source bytes and actual message-shaped operands.
NORMALIZED_PEERS = {
    0x90B2DA: [0x9033D6],
    0x90B30E: [0x9031E7],
    0x918E17: [0x91934B, 0x919432],
    0x92ED6E: [0x9194FF],
    0x93030B: [0x93082C],
    0x95252C: [0x945271, 0x945654, 0x95109C, 0x9514A0,
               0x951CFC, 0x952127, 0x955C4A],
    0x96823A: [0x9194FF],
    0x997E34: [0x968D35],
    0x9BA36F: [0x97AAAC],
}
TRAINER_NAMES = {0xAC03A0, 0xAC3320, 0xAC3370, 0xAC3398,
                 0xAC3410, 0xAC53A0, 0xAC5940, 0xAC5DC8,
                 0xAC5DF0, 0xAC8050, 0xAC8525}
ITEM_DESCRIPTIONS = {0x3D648D, 0x3D8F7F, 0xA9B695}
PLACE_NAMES = {0x71DD90, 0x723AB0, 0x731B10, 0xA175E4,
               0xC04EA4, 0xC05294, 0xC05304}
PREFIX_MESSAGES = {
    0x8C4EF1: (0x8C4EED, 0x8C4D7E),
    0x8C52AE: (0x8C52AA, 0x8C513C),
}
FULLER_STARTS = {0x96999A: 0x969854, 0xAAAA35: 0xAAA9DC}


def check(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def normalized(text):
    return ' '.join(text.split())


def complete(rom, start, end=None, strict=True, limit=8192):
    p = parse(rom, start, limit=limit, strict_english=strict)
    check(p is not None and p['terminated'] and not p['issues'],
          f'Complete parse failed at {start:#x}')
    if end is not None:
        check(p['end'] == end, f'End mismatch at {start:#x}')
    return p


def occurrences(rom, raw):
    result = []
    position = 0
    while True:
        position = rom.find(raw, position)
        if position < 0:
            return result
        result.append(position)
        position += 1


def run():
    frozen = json.loads((ROOT / 'extracted/text/text_triage_input.json').read_text())
    rom = (ROOT / 'roms/POKEMON Liquid Crystal.gba').read_bytes()
    digest = hashlib.sha256(rom).hexdigest()
    check(digest == frozen['source_sha256'], 'Source ROM hash changed')
    incoming = index_pointers(rom)
    source = frozen['reference_candidates']
    check(len(source) == 64, 'Expected the frozen 64-candidate cohort')
    output = []
    for item in sorted(source, key=lambda x: int(x['offset'], 16)):
        start = int(item['offset'], 16)
        end = int(item['end_offset_exclusive'], 16)
        p = complete(rom, start, end)
        check(p['plain'] == item['plain_text'], f'Frozen text changed: {start:#x}')
        refs = item['references'] + item['interior_references']
        for ref in refs:
            site, target = int(ref['offset'], 16), int(ref['target'], 16)
            check(site in incoming.get(target, []), f'Pointer mismatch: {site:#x}')
        entry = {
            'offset': hex(start), 'end_offset_exclusive': hex(end),
            'original_reference_status': item['reference_status'],
            'plain_text': item['plain_text'],
            'extent_sha256': hashlib.sha256(rom[start:end]).hexdigest(),
            'existing_pointer_evidence': refs,
            'classification': None, 'evidence': 'CONFIRMED_IN_ROM',
            'interpretation': 'STRONGLY_INFERRED; no runtime or native consumer validation',
            'reachability': 'UNKNOWN', 'unused_status': 'UNKNOWN',
        }
        facts = {}
        if start == 0x23E830 or start in TRAINER_NAMES or start == 0x99C03C:
            entry['classification'] = 'INLINE_NAME_FIELD'
            if start == 0x23E830:
                check((start - CLASS_BASE) % CLASS_STRIDE == 0, 'Class alignment changed')
                facts = {'kind': 'trainer_class_name', 'table_base': hex(CLASS_BASE),
                         'record_stride_bytes': CLASS_STRIDE,
                         'record_index': (start - CLASS_BASE) // CLASS_STRIDE,
                         'name_start': hex(start), 'name': p['plain']}
                entry['note'] = 'Nexus occupies a 13-byte class-name slot; the table base has native-sized raw references.'
                base = CLASS_BASE
            elif start in TRAINER_NAMES:
                name_start = 0xAC8528 if start == 0xAC8525 else start
                delta = name_start - 4 - TRAINER_BASE
                check(delta >= 0 and delta % TRAINER_STRIDE == 0, 'Trainer alignment changed')
                name = complete(rom, name_start, limit=12)
                record_start = name_start - 4
                facts = {'kind': 'trainer_name', 'table_base': hex(TRAINER_BASE),
                         'record_stride_bytes': TRAINER_STRIDE,
                         'record_index': hex(delta // TRAINER_STRIDE),
                         'record_start': hex(record_start),
                         'record_header_hex': rom[record_start:name_start].hex(' '),
                         'name_start': hex(name_start), 'name': name['plain'],
                         'candidate_contains_preceding_record_fields': start != name_start}
                entry['note'] = 'Name occupies the +4 field of a 40-byte trainer record.'
                if start != name_start:
                    entry['note'] += ' The old suffix starts three bytes early, inside the trainer header.'
                base = TRAINER_BASE
            else:
                name_start = 0x99C048
                record_index = 0x115
                check(ITEM_BASES[1] + record_index * ITEM_STRIDE == name_start,
                      'GS Ball item alignment changed')
                check(struct.unpack_from('<H', rom, name_start + 14)[0] == record_index,
                      'GS Ball item ID changed')
                name = complete(rom, name_start, limit=14)
                facts = {'kind': 'item_name', 'table_base': hex(ITEM_BASES[1]),
                         'record_stride_bytes': ITEM_STRIDE, 'record_index': hex(record_index),
                         'name_start': hex(name_start), 'name': name['plain'],
                         'candidate_includes_bytes_before_name': name_start - start}
                entry['note'] = 'The old suffix includes 12 padding/previous-record bytes before the GS BALL name field.'
                base = ITEM_BASES[1]
            facts['table_base_pointer_sites'] = [hex(x) for x in incoming.get(base, [])]
            facts['exact_name_pointer_sites'] = [hex(x) for x in incoming.get(int(facts['name_start'], 16), [])]
            check(facts['table_base_pointer_sites'], 'Expected table-base reference missing')
        elif start in ITEM_DESCRIPTIONS or start in PLACE_NAMES or start == 0x4487C0:
            entry['classification'] = 'TABLE_POINTER_TEXT'
            if start in ITEM_DESCRIPTIONS:
                records = []
                for ref in refs:
                    site = int(ref['offset'], 16)
                    for base in ITEM_BASES:
                        delta = site - 20 - base
                        if delta >= 0 and delta % ITEM_STRIDE == 0 and delta // ITEM_STRIDE < 512:
                            record = site - 20
                            records.append({'table_base': hex(base), 'record_index': hex(delta // ITEM_STRIDE),
                                            'record_start': hex(record), 'description_pointer_site': hex(site),
                                            'name': complete(rom, record, limit=14)['plain'],
                                            'stored_item_id': hex(struct.unpack_from('<H', rom, record + 14)[0])})
                check(records, 'Description table slot missing')
                facts = {'kind': 'item_description', 'record_stride_bytes': ITEM_STRIDE,
                         'description_field_offset': 20, 'records': records}
                entry['note'] = 'Item-description pointers are data fields, so message-opcode recognition is not expected.'
                if start == 0x3D648D:
                    entry['note'] += ' The orange seed is a stone-color description, without Orange story evidence.'
            elif start in PLACE_NAMES:
                check(any(0x2C8B00 <= int(r['offset'], 16) < 0x2C8BF0 for r in refs),
                      'Expected place-label pointer region missing')
                facts = {'kind': 'place_label', 'pointer_region': '0x2c8b00..0x2c8bf0 (exclusive; inspected slice, not table bounds)'}
                entry['note'] = 'Place label has an aligned entry in the shared contiguous string-pointer region; owner/lookup semantics remain unverified.'
            else:
                facts = {'kind': 'encyclopedia_description_candidate', 'pointer_site': '0x44fce8'}
                entry['note'] = 'Legendary bird description uses orange for wing color; no Orange story claim is supported.'
        elif start in (0x7720D9, 0x9C294B):
            entry['classification'] = 'OTHER_RAW_POINTER_TEXT'
            facts = {'kind': 'game_information' if start == 0x7720D9 else 'credits_names'}
            entry['note'] = ('Raw pointer-backed game-information text; it is not a script execution witness.'
                             if start == 0x7720D9 else
                             'Credits contain Mister Glitch, a lexical Mister G hit without evidence of an in-game character event.')
        elif start in PREFIX_MESSAGES:
            entry['classification'] = 'PRECEDING_MSGBOX_TARGET_WITH_PREFIX_ANOMALY'
            target, site = PREFIX_MESSAGES[start]
            check(site in incoming.get(target, []), 'Preceding message pointer missing')
            check(classify_operand(rom, site)['kind'] == 'MSGBOX_SHAPE', 'Message shape changed')
            complete(rom, target, end, strict=False)
            check(parse(rom, target, strict_english=True) is None, 'Expected strict prefix rejection changed')
            check(rom[target:start] == bytes.fromhex('fc 01 08 08'), 'Prefix anomaly bytes changed')
            facts = {'pointer_target': hex(target), 'pointer_operand_site': hex(site),
                     'command_start': hex(site - 2), 'prefix_hex': rom[target:start].hex(' '),
                     'unvalidated_english_glyph_offset': hex(start - 1)}
            entry['note'] = 'A msgbox-shaped operand targets four bytes before the old suffix. COLOR 08 is followed by glyph byte 08, rejected by strict English; rendering and execution remain unknown.'
        elif start in (0x918E17, 0x997E34):
            entry['classification'] = 'ADJACENT_BINARY_PREFIX_CANDIDATE'
            if start == 0x918E17:
                target, site, command, text_start = 0x918E14, 0x918D74, 0x918D71, 0x918E18
                check(rom[command:site] == bytes.fromhex('4f 04 00'), 'Movement command shape changed')
                check(rom[target:text_start] == bytes.fromhex('12 12 12 fe'), 'Movement bytes changed')
                facts = {'data_kind': 'applymovement_shape', 'command_start': hex(command),
                         'data_pointer_operand_site': hex(site), 'data_target': hex(target),
                         'data_hex': rom[target:text_start].hex(' '), 'text_start_candidate': hex(text_start)}
                entry['note'] = 'Nearby pointer targets movement bytes. The old suffix includes movement terminator FE as a newline; it is not a recovered text pointer.'
            else:
                target, site, command, text_start = 0x997E33, 0x997DE9, 0x997DE8, 0x997E37
                check(rom[command] == 0x86, 'Pokemart command shape changed')
                check(rom[target:text_start] == bytes.fromhex('62 00 00 00'), 'Inventory bytes changed')
                facts = {'data_kind': 'pokemart_shape', 'command_start': hex(command),
                         'data_pointer_operand_site': hex(site), 'data_target': hex(target),
                         'item_u16': '0x62', 'terminator_u16': 0,
                         'text_start_candidate': hex(text_start)}
                entry['note'] = 'Nearby pointer targets a one-item u16 inventory with zero terminator. Three data bytes were decoded as leading spaces before the dialogue.'
            check(site in incoming.get(target, []), 'Adjacent data pointer missing')
            text = complete(rom, text_start, end)
            facts['text'] = text['plain']
            facts['exact_text_start_pointer_sites'] = [hex(x) for x in incoming.get(text_start, [])]
        elif start in FULLER_STARTS:
            entry['classification'] = 'INTERIOR_POINTER_SELECTED_TRUNCATED_TEXT'
            fuller = FULLER_STARTS[start]
            full_text = complete(rom, fuller, end)
            check(not incoming.get(fuller), 'Expected full-start absence changed')
            facts = {'fuller_start_candidate': hex(fuller), 'fuller_end_exclusive': hex(end),
                     'fuller_text': full_text['plain'],
                     'fuller_start_pointer_sites': [],
                     'old_pointer_start_is_interior': True}
            entry['note'] = 'Pointer-first selection chose a raw interior hit and discarded coherent earlier text. The fuller candidate is complete strict English; the raw pointer has no recognized text-operand shape.'
        elif start in (0x93030B, 0xABB58A):
            entry['classification'] = 'UNCLASSIFIED_INTERIOR_POINTER_TEXT'
            check(not item['references'] and item['interior_references'], 'Expected interior-only references changed')
            entry['note'] = 'Only unclassified raw interior pointer hits support this extent. Keep the dialogue and its separately referenced variant; no use/unused conclusion follows.'
        else:
            entry['classification'] = 'NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE'
            check(item['reference_status'] == 'NO_ABSOLUTE_POINTER_FOUND', 'Unclassified raw-reference row')
            check(not any(start <= t < end - 1 for t in incoming), 'Expected absence changed')
            entry['note'] = 'No absolute pointer to this parsed text extent was found. Indirect/native uses, edited duplicates, and map/script ownership remain open.'
            if start == 0xB01BB0:
                clean = complete(rom, 0xB01BB2, end)
                facts = {'cleaner_start_candidate': '0xb01bb2', 'cleaner_text': clean['plain'],
                         'old_prefix_hex': rom[start:start + 2].hex(' ')}
                entry['note'] += ' A cleaner Danny dialogue start is two bytes later; the apostrophe/a prefix adjoins nontext bytes, so the original boundary is uncertain.'
        entry['facts'] = facts
        copies = occurrences(rom, rom[start:end])
        entry['exact_raw_copies_including_self'] = [hex(x) for x in copies]
        peer_evidence = []
        for peer in NORMALIZED_PEERS.get(start, []):
            peer_text = complete(rom, peer)
            check(normalized(peer_text['plain']) == normalized(p['plain']), 'Normalized peer mismatch')
            sites = [classify_operand(rom, site) for site in incoming.get(peer, [])
                     if classify_operand(rom, site)['kind'] != 'RAW_POINTER']
            check(sites, 'Referenced duplicate witness missing')
            peer_evidence.append({'offset': hex(peer), 'comparison': 'plain text with collapsed whitespace',
                                  'typed_operand_shapes': sites})
        entry['normalized_referenced_copy_witnesses'] = peer_evidence
        output.append(entry)
    counts = dict(Counter(e['classification'] for e in output))
    expected = {'INLINE_NAME_FIELD': 13, 'TABLE_POINTER_TEXT': 11,
                'OTHER_RAW_POINTER_TEXT': 2,
                'PRECEDING_MSGBOX_TARGET_WITH_PREFIX_ANOMALY': 2,
                'ADJACENT_BINARY_PREFIX_CANDIDATE': 2,
                'INTERIOR_POINTER_SELECTED_TRUNCATED_TEXT': 2,
                'UNCLASSIFIED_INTERIOR_POINTER_TEXT': 2,
                'NO_ABSOLUTE_POINTER_DIALOGUE_CANDIDATE': 30}
    check(counts == expected, '64-row classification partition changed')
    summary = {'source_sha256': digest, 'input_cohort': 'frozen original Orange-specific weak-reference candidates',
               'candidate_count': len(output), 'original_reference_status_counts': dict(Counter(e['original_reference_status'] for e in output)),
               'classification_counts': counts,
               'candidates_with_normalized_referenced_copy_witnesses': sum(bool(e['normalized_referenced_copy_witnesses']) for e in output),
               'certified_unused': 0, 'certified_reachable': 0,
               'scope': 'Static text/reference triage; no map owner, native consumer or runtime validation.'}
    result = {'summary': summary, 'records': output}
    (ROOT / 'extracted/text/orphan_reference_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    write_report(result)
    print(json.dumps(summary, indent=2))
    return result


def write_report(result):
    summary = result['summary']
    lines = ['# Weak-reference text candidate review', '',
             f"Source SHA-256: `{summary['source_sha256']}`. Input is the frozen 64-row cohort in `extracted/text/text_triage_input.json` (47 without absolute pointers; 17 raw-pointer-only). This supplements the original corpus; it does not silently relabel it.", '',
             'Bytes, pointer values, field alignment and equality are CONFIRMED_IN_ROM. FireRed-format interpretations and data-field roles are STRONGLY_INFERRED. Every map owner, native consumer, execution path and unused/reachable status remains UNKNOWN. No ROM/save changes were made.', '',
             '## Partition of all 64 candidates', '', '| Classification | Count |', '|---|---:|']
    for kind, count in summary['classification_counts'].items():
        lines.append(f'| `{kind}` | {count} |')
    lines += ['', '## Findings that change the interpretation', '',
              '- Thirteen candidates are inline name fields: Nexus class name, eleven trainer names and the GS BALL item name. Trainer names align to table `0xABFD84`, stride 40, field +4; the class table uses base `0x23E558`, stride 13. The bases have raw references. No direct pointer to each inline string is expected from this storage pattern. This does not establish runtime lookup or trainer reachability.',
              '- The old `0xAC8525` suffix begins inside trainer header bytes; Danny’s actual +4 name field starts at `0xAC8528`, trainer index `0x364`. The old `0x99C03C` GS BALL suffix includes 12 bytes before the name at `0x99C048`, item index `0x115` in table `0x9990AC`, stride 44.',
              '- Two message-shaped operands target before the strict-English suffix: operand `0x8C4D7E` → `0x8C4EED`, and operand `0x8C513C` → `0x8C52AA`. Each target begins `FC 01 08 08`: COLOR 08 followed by an English-unvalidated glyph byte 08. These explain the missed reference, while rendering/execution remain unverified.',
              '- Two nearby pointers are to adjacent binary data, not recovered text references. `0x918D74` targets movement `12 12 12 FE` at `0x918E14`; speech plausibly starts `0x918E18`. `0x997DE9` targets a one-item u16 inventory (`0x62`, zero terminator) at `0x997E33`; dialogue starts `0x997E37`. The original suffixes included movement/inventory bytes as formatting/spaces.',
              '- Pointer priority truncated two complete strings: the old `0x96999A` candidate is inside Oak’s full dialogue at `0x969854` through `0x969BBA` exclusive; old `0xAAAA35` is inside the Sunburst Island map text at `0xAAA9DC` through `0xAAAA7B` exclusive. Both fuller candidates parse strictly to EOS and have no exact start pointer. The raw interior pointer hits remain unclassified.',
              '- Eleven raw-pointer texts fit table/data roles: seven place labels, three item descriptions and a legendary-bird description. The orange-colored evolution stone and bird wings do not establish Orange story relevance. Credits mentioning Mister Glitch are another lexical false relevance match.',
              '- Nine of the 64 candidates have normalized-equal copies with message-shaped references. Equality removes controls and collapses whitespace; it does not identify which copy is active or prove another copy unused.',
              '- Thirty remaining candidates have no absolute pointer over their existing parsed extent. This is a bounded static observation; indirect/native use and ownership remain open. One Danny candidate at `0xB01BB0` has a cleaner possible start at `0xB01BB2` after an uncertain two-byte prefix.', '',
              '## Candidate ledger', '', '| Original start | Classification | Text preview |', '|---|---|---|']
    for entry in result['records']:
        preview = normalized(entry['plain_text'])[:85].replace('|', '\\|')
        lines.append(f"| `{entry['offset']}` | `{entry['classification']}` | {preview} |")
    lines += ['', '## Reproduce and next work', '',
              '`python tools/orphan_reference_audit.py` validates source hash, exact text extents, pointer values, table geometry, representative normalized duplicates, binary/message-prefix distinctions and the 64-row partition before regenerating this report and `extracted/text/orphan_reference_audit.json`.', '',
              'Keep the original reference status separate from this supplemental classification. Candidate discovery should retain complete strict-English starts even when an interior raw pointer exists; nearby pointer targets should be typed by their consumer before becoming text references. Fixed-width field consumers need table-base plus index analysis. Review surviving dialogue variants and their map/script owners next; no absent-pointer candidate is certified orphaned, broken or deletable.']
    (ROOT / 'research/orphan_candidate_review.md').write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    run()
