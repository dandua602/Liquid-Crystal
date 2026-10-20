"""Gen III English text with controls and offsets; see reference manifest.
Unknown controls/glyphs are reported rather than silently consumed.
"""
import re
from pathlib import Path

REF=Path(__file__).resolve().parents[1]/'research/references/charmap.txt'
TABLE={}
for line in REF.read_text().split('@ Hiragana')[0].splitlines():
    match=re.fullmatch(r"'(.+)'\s*=\s*([0-9A-F]{2})",line.strip())
    if match:
        char,value=match.groups()
        if char=="\\'":char='’'
        if int(value,16)!=255:TABLE.setdefault(int(value,16),char)
TABLE.update({0x2C:'<SUPER_ER>',0x34:'<LV>',0x53:'<PK>',0x54:'<MN>',
 0x55:'<PO>',0x56:'<KE>',0x57:'<BLOCK1>',0x58:'<BLOCK2>',0x59:'<BLOCK3>',
 0x77:'<SPACER>',0x79:'↑',0x7A:'↓',0x7B:'←',0x7C:'→',0x84:'<SUPER_E>',0xA0:'<SUPER_RE>'})
CONTROL_NAMES=['COLOR','HIGHLIGHT','SHADOW','COLOR_HIGHLIGHT_SHADOW','PALETTE',
 'FONT','RESET_FONT','PAUSE','WAIT_BUTTON','WAIT_SE','PLAY_BGM','ESCAPE',
 'SHIFT_RIGHT','SHIFT_DOWN','FILL_WINDOW','PLAY_SE','CLEAR','SKIP','CLEAR_TO',
 'MIN_LETTER_SPACING','JPN','ENG','PAUSE_MUSIC','RESUME_MUSIC']
CONTROL_ARITY=dict(enumerate([1,1,1,3,1,1,0,1,0,0,2,1,1,1,0,2,1,1,1,1,0,0,0,0],1))
PLACEHOLDERS={1:'PLAYER',2:'STR_VAR_1',3:'STR_VAR_2',4:'STR_VAR_3',6:'RIVAL'}
# Strict English is only a boundary heuristic, not a claim about font coverage.
ENGLISH_GLYPHS=set(range(0xA1,0xF7))|{0,0x1B,0x2C,0x2D,0x2E,0x34,0x35,
 0x36,0x51,0x52,0x53,0x54,0x55,0x56,0x57,0x58,0x59,0x5B,0x5C,0x5D,
 0x77,0x79,0x7A,0x7B,0x7C,0x84,0x85,0x86,0xA0}

def parse(data,start=0,limit=8192,strict_english=False):
    """EOS-aware parser. FF inside a control parameter is data, not EOS.
    Dynamic placeholders retain their indices; expansion and Japanese mode
    are not simulated. F7+index is documented in retained src/text.c.
    """
    pos=start;stop=min(len(data),start+limit);tokens=[];issues=[];parts=[];plain=[]
    while pos<stop:
        at=pos;value=data[pos];pos+=1;kind='glyph';text='';visible=''
        if value==255:
            return {'start':start,'end':pos,'terminated':True,'text':''.join(parts),
                    'plain':''.join(plain),'tokens':tokens,'issues':issues}
        if value==0xFC:
            if pos>=stop:issues.append({'offset':at,'reason':'truncated control'});break
            code=data[pos];pos+=1
            if code not in CONTROL_ARITY:
                issues.append({'offset':at,'reason':f'unknown control {code:02X}'})
                if strict_english:return None
                break
            arity=CONTROL_ARITY[code]
            if pos+arity>stop:issues.append({'offset':at,'reason':'truncated control parameters'});break
            args=data[pos:pos+arity];pos+=arity;kind='control'
            text='<'+CONTROL_NAMES[code-1]+(' '+args.hex(' ').upper() if args else '')+'>'
            if code==0x15:
                issues.append({'offset':at,'reason':'Japanese mode not decoded'})
                if strict_english:return None
        elif value in (0xF7,0xFD,0xF8,0xF9):
            if pos>=stop:issues.append({'offset':at,'reason':'truncated two-byte token'});break
            arg=data[pos];pos+=1;kind='dynamic' if value==0xF7 else ('placeholder' if value==0xFD else 'symbol')
            label=('DYNAMIC_'+f'{arg:02X}') if value==0xF7 else (PLACEHOLDERS.get(arg,f'PLACEHOLDER_{arg:02X}') if value==0xFD else ('KEY_' if value==0xF8 else 'SYMBOL_')+f'{arg:02X}')
            text='{'+label+'}';visible=text
            if value==0xFD and arg>0x0D:
                issues.append({'offset':at,'reason':'unknown placeholder'})
                if strict_english:return None
        elif value in (0xFA,0xFB,0xFE):
            kind='layout';text={0xFA:'<SCROLL>\n',0xFB:'<PARAGRAPH>\n\n',0xFE:'\n'}[value];visible='\n'
        else:
            if value not in TABLE or (strict_english and value not in ENGLISH_GLYPHS):
                if strict_english:return None
                issues.append({'offset':at,'reason':f'unvalidated English glyph {value:02X}'})
            text=TABLE.get(value,f'<BYTE_{value:02X}>');visible=text
        tokens.append({'offset':at,'end':pos,'kind':kind,'text':text,'raw':data[at:pos].hex()})
        parts.append(text);plain.append(visible)
    return {'start':start,'end':pos,'terminated':False,'text':''.join(parts),
            'plain':''.join(plain),'tokens':tokens,'issues':issues}

def decode(data):return parse(data,limit=len(data))['text']
def encode(text):
    inverse={v:k for k,v in TABLE.items() if len(v)==1}
    return bytes(inverse[c] for c in text)
def fold_case(data):
    table=bytearray(range(256))
    for i in range(26):table[0xD5+i]=0xBB+i
    return data.translate(bytes(table))
