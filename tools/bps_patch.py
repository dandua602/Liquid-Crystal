"""Small standard BPS encoder/strict applier (SourceRead and TargetRead)."""
import struct
import zlib


def number(value):
    if value<0:raise ValueError('Negative BPS integer')
    result=bytearray()
    while True:
        x=value&127;value>>=7
        if not value:result.append(x|128);return bytes(result)
        result.append(x);value-=1


def create(source,target,metadata=b''):
    if len(source)!=len(target):raise ValueError('This bounded encoder requires equal lengths')
    out=bytearray(b'BPS1'+number(len(source))+number(len(target))+number(len(metadata))+metadata)
    start=0
    while start<len(target):
        same=source[start]==target[start];end=start+1
        while end<len(target)and(source[end]==target[end])==same:end+=1
        out+=number(((end-start-1)<<2)|(0 if same else 1))
        if not same:out+=target[start:end]
        start=end
    out+=struct.pack('<II',zlib.crc32(source),zlib.crc32(target));out+=struct.pack('<I',zlib.crc32(out))
    return bytes(out)


def apply(source,patch):
    if len(patch)<16 or patch[:4]!=b'BPS1':raise ValueError('Invalid BPS header')
    if zlib.crc32(patch[:-4])!=struct.unpack_from('<I',patch,len(patch)-4)[0]:raise ValueError('BPS checksum failed')
    source_crc,target_crc=struct.unpack_from('<II',patch,len(patch)-12)
    if zlib.crc32(source)!=source_crc:raise ValueError('Wrong BPS source')
    at=4;stop=len(patch)-12
    def read():
        nonlocal at
        value=0;shift=1
        for _ in range(10):
            if at>=stop:raise ValueError('Truncated BPS integer')
            x=patch[at];at+=1;value+=(x&127)*shift
            if x&128:return value
            shift<<=7;value+=shift
        raise ValueError('Oversized BPS integer')
    size,outsize,metadata=read(),read(),read()
    if size!=len(source)or outsize>0x2000000 or at+metadata>stop:raise ValueError('Invalid BPS bounds')
    at+=metadata;out=bytearray()
    while len(out)<outsize:
        action=read();mode=action&3;length=(action>>2)+1
        if len(out)+length>outsize:raise ValueError('BPS output overflow')
        if mode==0:
            if len(out)+length>len(source):raise ValueError('BPS source overflow')
            out+=source[len(out):len(out)+length]
        elif mode==1:
            if at+length>stop:raise ValueError('Truncated BPS target data')
            out+=patch[at:at+length];at+=length
        else:raise ValueError('Unsupported BPS action in bounded patch')
    if at!=stop or zlib.crc32(out)!=target_crc:raise ValueError('BPS target checksum/trailing data failed')
    return bytes(out)


if __name__=='__main__':
    import argparse
    import hashlib
    from pathlib import Path
    parser=argparse.ArgumentParser(description='Apply a generated P001 forward or reverse BPS patch to a new file.')
    parser.add_argument('source',type=Path);parser.add_argument('patch',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args()
    result=apply(args.source.read_bytes(),args.patch.read_bytes())
    # Never overwrite a ROM or save, including an existing output.
    with args.output.open('xb')as stream:stream.write(result)
    print(hashlib.sha256(result).hexdigest(),args.output)
