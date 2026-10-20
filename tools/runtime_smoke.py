"""Replay headless boot/source-save loading on disposable copies; optional forced room.

Requires the separately built mGBA frontend in mgba_probe.c. No ROM patching.
The forced-room mode injects a warp bytecode into the emulator's RAM context;
it establishes behavior in that state, never normal story reachability.
"""
import argparse
import hashlib
import json
import shutil
import struct
import subprocess
import tempfile
import zlib
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ppm_to_png(source, target):
    header, size, maximum, pixels = Path(source).read_bytes().split(b'\n', 3)
    width, height = map(int, size.split())
    if header != b'P6' or maximum != b'255' or len(pixels) != width * height * 3:
        raise ValueError('Unexpected screenshot format')
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    scan = b''.join(b'\0' + pixels[p:p + width*3] for p in range(0, len(pixels), width*3))
    Path(target).write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>2I5B', width, height, 8, 2, 0, 0, 0)) +
                             chunk(b'IDAT', zlib.compress(scan)) + chunk(b'IEND', b''))


def warp_context(group, number, warp=0):
    # Supplied-ROM native Init/Setup at 0x697AC/0x697E8 and literals at
    # 0x69B18/20/24 establish this layout. Use unused context stack storage
    # for a warp command that makes no script call, then ends.
    data = bytearray(0x74)
    data[1] = 1
    struct.pack_into('<I', data, 8, 0x03000EBC)
    data[12:21] = bytes([0x3D, group, number, warp]) + b'\xff'*4 + b'\x02'
    struct.pack_into('<II', data, 0x5C, 0x0815F9B4, 0x0815FD08)
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frontend', required=True, type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'extracted/runtime')
    parser.add_argument('--forced-room', action='store_true')
    parser.add_argument('--room-interactions', action='store_true', help='Also walk to the sign, telephone, lights, machine and stair; implies --forced-room')
    args = parser.parse_args()
    started = datetime.now(timezone.utc).isoformat()
    args.output.mkdir(parents=True, exist_ok=True)
    rom = ROOT / 'roms/POKEMON Liquid Crystal.gba'
    save = ROOT / 'saves/source/POKEMON Liquid Crystal DD 5 badge.sav'
    original = {'rom': hashlib.sha256(rom.read_bytes()).hexdigest(), 'save': hashlib.sha256(save.read_bytes()).hexdigest()}
    transcript = []
    with tempfile.TemporaryDirectory(prefix='lc-runtime-') as directory:
        temp = Path(directory)
        shutil.copyfile(rom, temp / 'copy.gba')
        (temp / 'copy.sav').write_bytes(save.read_bytes()[:0x20000])
        process = subprocess.Popen([str(args.frontend.resolve()), str(temp / 'copy.gba'), str(temp / 'copy.sav')],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        if json.loads(process.stdout.readline()) != {'ready': True}:
            raise RuntimeError('Frontend did not start')
        def command(line):
            process.stdin.write(line + '\n'); process.stdin.flush()
            response = json.loads(process.stdout.readline())
            transcript.append({'command': line, 'response': response})
            return response
        def frame(count, keys=0):
            return command(f'f {count} {keys}')
        def capture(name):
            command(f'p {temp / "frame.ppm"}')
            ppm_to_png(temp / 'frame.ppm', args.output / f'{name}.png')
            # Use a stable path in the retained command transcript.
            transcript[-1]['command'] = f'p <temporary>/{name}.ppm'
        mapper_start=command('m')
        frame(300); frame(1, 8); frame(180); frame(1, 8); frame(180)
        capture('title')
        frame(1, 8); frame(420)
        capture('continue_menu')
        frame(1, 1); frame(300)
        capture('continue_selection')
        frame(1, 1); frame(120)
        capture('continue_menu')
        frame(1, 1); frame(240)
        capture('loaded_field')
        pointer = int.from_bytes(bytes.fromhex(command('r 3005008 4')['hex']), 'little')
        location = command(f'r {pointer:x} 12')
        if bytes.fromhex(location['hex'])[:6] != bytes.fromhex('20001d00033e'):
            raise RuntimeError('Copied save did not reach the expected source-save field location')
        if args.forced_room or args.room_interactions:
            command(f'w 3000eb0 {warp_context(6, 31).hex()}')
            command('w 3000ea8 00'); command('w 3000eac 01')
            frame(180); capture('forced_room_intro')
            for _ in range(50):
                frame(10, 1); frame(30)
            capture('forced_room_after_intro')
            command('r 3000ea8 116')
            pointer = int.from_bytes(bytes.fromhex(command('r 3005008 4')['hex']), 'little')
            command(f'r {pointer:x} 12')
            if args.room_interactions:
                from mister_r_audit import room_geometry
                geometry = room_geometry(rom.read_bytes())
                floor = {(c['x'],c['y']) for c in geometry['cells'] if c['in_floor_component']}
                def position():
                    ptr = int.from_bytes(bytes.fromhex(command('r 3005008 4')['hex']), 'little')
                    data = bytes.fromhex(command(f'r {ptr:x} 12')['hex'])
                    return struct.unpack_from('<hh',data), list(data[4:7])
                def walk_to(target):
                    start, map_slot = position()
                    if map_slot[:2] != [6,31]:raise RuntimeError(f'Unexpected map {map_slot}')
                    queue=deque([start]); parents={start:None}
                    while queue and target not in parents:
                        x,y=queue.popleft()
                        for neighbor in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                            if neighbor in floor and neighbor not in parents and neighbor not in {(12,14),(20,7)}:
                                parents[neighbor]=(x,y);queue.append(neighbor)
                    if target not in parents:raise RuntimeError(f'No floor path to {target}')
                    path=[];point=target
                    while point!=start:path.append(point);point=parents[point]
                    for next_pos in reversed(path):
                        key={(1,0):16,(-1,0):32,(0,-1):64,(0,1):128}[(next_pos[0]-start[0],next_pos[1]-start[1])]
                        frame(16,key);frame(24)
                        actual, slot=position()
                        if actual!=next_pos or slot[:2]!=[6,31]:raise RuntimeError(f'Walk expected {next_pos}, got {actual} in {slot}')
                        start=next_pos
                for name,target,direction in [('damaged_sign',(14,9),32),('telephone',(14,7),64),
                                               ('lights',(11,7),64),('machine',(8,8),64)]:
                    walk_to(target)
                    frame(1,direction);frame(16);frame(1,1);frame(120)
                    capture('interaction_'+name)
                    for _ in range(64):
                        status=bytes.fromhex(command('r 3000ea8 4')['hex'])[0]
                        if status==2:break
                        frame(10,1);frame(30)
                    else:raise RuntimeError(f'Interaction {name} did not finish')
                walk_to((19,7))
                frame(16,16);frame(180)
                capture('forced_stair_landing')
                position()
                frame(16,16);frame(180)
                capture('forced_stair_result')
                position()
        mapper_end=command('m')
        process.stdin.write('q\n'); process.stdin.flush()
        if process.wait(timeout=20) != 0:
            raise RuntimeError('Frontend failed')
        copied_save_hash = hashlib.sha256((temp / 'copy.sav').read_bytes()).hexdigest()
    after = {'rom': hashlib.sha256(rom.read_bytes()).hexdigest(), 'save': hashlib.sha256(save.read_bytes()).hexdigest()}
    if original != after:
        raise RuntimeError('Source changed')
    result = {'complete':True,'started_at_utc':started,'frontend_sha256':hashlib.sha256(args.frontend.read_bytes()).hexdigest(),
              'emulator': 'mGBA 0.10.5, headless software renderer, HLE BIOS; exact-ROM banked-SRAM adapter when detected',
              'mapper_at_start':mapper_start,'mapper_at_end':mapper_end,
              'source_sha256': original, 'source_unchanged': True, 'flash_copy_sha256_after': copied_save_hash,
              'forced_room': args.forced_room or args.room_interactions, 'room_interactions': args.room_interactions,
              'normal_field_location': location, 'transcript': transcript,
              'limits': 'Screenshots require review. This smoke case does not perform a fresh game save/reload; see linked_progression.py for that test. Forced room entry bypasses story progression and is not a reachability test.'}
    (args.output / 'smoke.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'transcript'}, indent=2))


if __name__ == '__main__':
    main()
