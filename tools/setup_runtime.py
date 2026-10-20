"""Build optional pinned headless mGBA in a cache outside the checkout."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path('/workspace/.cache/liquid-crystal-runtime')
URL = 'https://codeload.github.com/mgba-emu/mgba/tar.gz/refs/tags/0.10.5'
SHA256 = '91d6fbd32abcbdf030d58d3f562de25ebbc9d56040d513ff8e5c19bee9dacf14'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    CACHE.mkdir(parents=True,exist_ok=True)
    binary=CACHE/'mgba-probe'; manifest=CACHE/'build.json'
    frontend=ROOT/'tools/mgba_probe.c'
    if binary.exists() and manifest.exists():
        old=json.loads(manifest.read_text())
        if old.get('recipe')==1 and old.get('frontend_sha256')==sha(frontend) and old.get('binary_sha256')==sha(binary):
            print(f'Verified cached mGBA 0.10.5 frontend: {binary}');return
    if not shutil.which('cc') or not shutil.which('make'):
        raise SystemExit('A C compiler and make are required for optional runtime validation.')
    cmake=shutil.which('cmake')
    cached_cmake=CACHE/'cmake/cmake/data/bin/cmake'
    if not cmake and cached_cmake.exists():cmake=str(cached_cmake)
    if not cmake:
        target=CACHE/'cmake'
        subprocess.run([sys.executable,'-m','pip','install','--disable-pip-version-check','--target',str(target),'cmake==4.4.4'],check=True)
        cmake=str(target/'cmake/data/bin/cmake')
    archive=CACHE/'mgba-0.10.5.tar.gz'
    if not archive.exists() or sha(archive)!=SHA256:
        with urllib.request.urlopen(URL,timeout=60) as response:
            content=response.read()
        if hashlib.sha256(content).hexdigest()!=SHA256:raise SystemExit('mGBA archive checksum mismatch')
        archive.write_bytes(content)
    source=CACHE/'mgba-0.10.5'
    if not source.exists():
        with tarfile.open(archive) as stream:stream.extractall(CACHE,filter='data')
    build=CACHE/'build'
    flags=['-DCMAKE_POLICY_VERSION_MINIMUM=3.5','-DLIBMGBA_ONLY=ON','-DBUILD_STATIC=ON','-DBUILD_SHARED=OFF']
    flags += ['-D'+name+'=OFF' for name in ('BUILD_QT','BUILD_SDL','BUILD_GL','BUILD_GLES2','BUILD_GLES3',
                'USE_FFMPEG','USE_PNG','USE_ZLIB','USE_MINIZIP','USE_LIBZIP','USE_SQLITE3','USE_LZMA',
                'USE_LUA','USE_DEBUGGERS','USE_ELF','USE_DISCORD_RPC')]
    with (CACHE/'build.log').open('w') as log:
        subprocess.run([cmake,'-S',str(source),'-B',str(build),*flags],check=True,stdout=log,stderr=subprocess.STDOUT)
        subprocess.run([cmake,'--build',str(build),'-j',str(min(os.cpu_count() or 2,6))],check=True,stdout=log,stderr=subprocess.STDOUT)
        temporary_binary=CACHE/'mgba-probe.build'
        subprocess.run(['cc','-O2','-I',str(build/'include'),'-I',str(source/'include'),str(frontend),str(build/'libmgba.a'),
                        '-lm','-lpthread','-o',str(temporary_binary)],check=True,stdout=log,stderr=subprocess.STDOUT)
        temporary_binary.replace(binary)
    manifest.write_text(json.dumps({'recipe':1,'mgba':'0.10.5','archive_url':URL,'archive_sha256':SHA256,
                                    'frontend_sha256':sha(frontend),'binary_sha256':sha(binary)},indent=2)+'\n')
    print(f'Built mGBA 0.10.5 frontend: {binary}')


if __name__=='__main__':main()
