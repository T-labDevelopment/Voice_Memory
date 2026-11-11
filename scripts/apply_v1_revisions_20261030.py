#!/usr/bin/env python3
"""Apply VoiceMemory v1 backported decisions to the 2026-10-29 received KiCad data.
No schematic symbols recreated from simplified cache: the existing project symbols are
renamed after confirming pin number consistency and original geometry retained.
KiCad 10 structure retained; no claims of KiCad CLI ERC/DRC verification.
"""
from pathlib import Path
import re,uuid,json,hashlib
P=Path(__file__).resolve().parents[1]/'hardware/kicad/voicememory'
PCB=P/'voicememory.kicad_pcb'; SCH=P/'voicememory.kicad_sch'; SYM=P/'Voice_Memory.kicad_sym'; FP=P/'Voice_Memory.pretty/RJ45_8P8C_THT_15.91x15.10.kicad_mod'

def balanced(s,start):
    if s[start]!='(':raise ValueError(start)
    d=0;quoted=False;escaped=False
    for i in range(start,len(s)):
        c=s[i]
        if quoted:
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c=='"':quoted=False
        elif c=='"':quoted=True
        elif c=='(':d+=1
        elif c==')':
            d-=1
            if d==0:return (start,i+1)
    raise ValueError('unbalanced '+str(start))

def subblocks(s,kind):
    # standard top-level footprint list or symbol instance; note multiline indent
    return [(m.start()+1,*balanced(s,m.start()+1)[1:]) for m in re.finditer(r'^\t\('+re.escape(kind)+r'\s',s,re.M)]

def find_pcb_fp(s,ref):
    hits=[]
    for a,b in subblocks(s,'footprint'):
        if re.search(r'\(property "Reference" "'+re.escape(ref)+r'"',s[a:b]):hits.append((a,b))
    assert len(hits)==1,(ref,len(hits))
    return hits[0]

def replaceblock(s,a,b,content):return s[:a]+content+s[b:]

def edit_fp(s,ref,f):
    a,b=find_pcb_fp(s,ref)
    return replaceblock(s,a,b,f(s[a:b]))

def replace_one(s,a,b):
    assert a in s,a
    return s.replace(a,b)

# 1) Correct RJ45 NPTH Y, preserving signal pads and all pad identities.
def rj_fix(s):
    pads=re.findall(r'\(pad "" np_thru_hole circle\s*\(at ([^)]*)\)',s)
    assert len(pads)==2, pads
    assert all(p.split()[-1]=='-4.32' or (len(p.split())==3 and p.split()[1]=='-4.32') for p in pads),pads
    s=re.sub(r'(\(pad "" np_thru_hole circle\s*\(at [^()\n]*?)\s-4\.32(?=\s|\))',r'\g<1> 4.32',s)
    assert len(re.findall(r'\(pad "" np_thru_hole circle\s*\(at [^)]* 4\.32',s))==2
    return s
fp=FP.read_text();FP.write_text(rj_fix(fp))
pcb=PCB.read_text()
for ref in ('J1','J2'):pcb=edit_fp(pcb,ref,rj_fix)

# 2) C11/C19: 0603/1608 KiCad standard IPC nominal pad geometry.
# Source: KiCad/kicad-footprints C_0603_1608Metric.kicad_mod, sha e55e431a174386e5b39bac64c0e92ebb0123fe0d
# footprint pad centers +/-0.775; pads 0.90 x 0.95; body 1.6 x 0.8, courtyard +/-1.48,+/-0.73.
def c_fix(s):
    assert 'Capacitor_SMD:C_0805_2012Metric' in s
    s=s.replace('Capacitor_SMD:C_0805_2012Metric','Capacitor_SMD:C_0603_1608Metric')
    s=re.sub(r'\(descr "Capacitor SMD 0805[^"\n]+"\)',
      '(descr "Capacitor SMD 0603 (1608 Metric), IPC-7351 nominal; standard KiCad C_0603_1608Metric")',s)
    # update existing 2 silk strokes while keeping their UUIDs
    silk=re.findall(r'\(fp_line.*?\(layer "F\.SilkS"\).*?\(uuid "[^"]+"\)\s*\)',s,re.S)
    assert len(silk)==2,len(silk)
    for i,block in enumerate(silk):
        b=re.sub(r'\(start [^)]*\)',f'(start -0.14058 {0.51 if i==0 else -0.51})',block,count=1)
        b=re.sub(r'\(end [^)]*\)',f'(end 0.14058 {0.51 if i==0 else -0.51})',b,count=1)
        s=s.replace(block,b,1)
    assert '(start -1.7 -0.98)' in s and '(end 1.7 0.98)' in s
    s=s.replace('(start -1.7 -0.98)','(start -1.48 -0.73)').replace('(end 1.7 0.98)','(end 1.48 0.73)')
    s=s.replace('(start -1 -0.625)','(start -0.8 -0.4)').replace('(end 1 0.625)','(end 0.8 0.4)')
    assert s.count('(size 1 1.45)')==2
    s=s.replace('(size 1 1.45)','(size 0.9 0.95)')
    s=s.replace('(at -0.95 0 270)','(at -0.775 0 270)').replace('(at 0.95 0 270)','(at 0.775 0 270)')
    s=s.replace('(at -0.95 0 180)','(at -0.775 0 180)').replace('(at 0.95 0 180)','(at 0.775 0 180)')
    s=s.replace('C_0805_2012Metric.step','C_0603_1608Metric.step')
    assert s.count('Capacitor_SMD:C_0603_1608Metric')==1
    return s
for ref in ('C11','C19'):pcb=edit_fp(pcb,ref,c_fix)

# 3) U2 208mil SOP8 footprint. Original SPIN at +/-2.475; updated KiCad standard
# SOP-8_5.28x5.23mm_P1.27mm +/-3.6. Retain net/pad UUID, each pin number, and midpoint.
# source: KiCad/kicad-footprints blob 48f37d5d7c89bc3fc1f8de9e8d82179e9b265a76
u2_old=[]
def u2_fix(s):
    assert 'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm' in s
    s=s.replace('Package_SO:SOIC-8_3.9x4.9mm_P1.27mm','Package_SO:SOP-8_5.28x5.23mm_P1.27mm')
    s=s.replace('AT25SF321B-SSHB','W25Q32RVCSJM')
    s=re.sub(r'\(descr "SOIC, 8 Pin[^"\n]*"\)', '(descr "SOP, 8 Pin 208mil, KiCad standard SOP-8_5.28x5.23mm_P1.27mm")',s)
    # delete only footprint graphic elements that came with old footprint (preserve property/attr/pads)
    for tag in ('fp_line','fp_rect','fp_arc','fp_circle'):
        pat=re.compile(r'\n\t\t\('+tag+r'\s')
        while True:
            m=pat.search(s)
            if not m:break
            a,b=balanced(s,m.start()+3)
            s=s[:m.start()]+s[b:]
    layers={
    'F.SilkS':[((0,2.725),(2.75,2.725)),((2.75,2.725),(2.75,2.465)),((0,2.725),(-2.75,2.725)),((-2.75,2.725),(-2.75,2.465)),((0,-2.725),(2.75,-2.725)),((2.75,-2.725),(2.75,-2.465)),((0,-2.725),(-2.75,-2.725)),((-2.75,-2.725),(-2.75,-2.465)),((-2.75,-2.465),(-4.4,-2.465))],
    'F.Fab':[((-1.64,-2.615),(2.64,-2.615)),((2.64,-2.615),(2.64,2.615)),((2.64,2.615),(-2.64,2.615)),((-2.64,2.615),(-2.64,-1.615)),((-2.64,-1.615),(-1.64,-2.615))],
    'F.CrtYd':[((-4.65,-2.86),(-4.65,2.86)),((-4.65,2.86),(4.65,2.86)),((4.65,2.86),(4.65,-2.86)),((4.65,-2.86),(-4.65,-2.86))]
    }
    out=[]
    for layer,coords in layers.items():
        for j,(p,q) in enumerate(coords):
            uid=uuid.uuid5(uuid.NAMESPACE_URL,f'VoiceMemory-v1-U2-{layer}-{j}')
            w='0.05' if layer=='F.CrtYd' else ('0.12' if layer=='F.SilkS' else '0.1')
            out.append(f'\n\t\t(fp_line\n\t\t\t(start {p[0]} {p[1]})\n\t\t\t(end {q[0]} {q[1]})\n\t\t\t(stroke (width {w}) (type solid))\n\t\t\t(layer "{layer}")\n\t\t\t(uuid "{uid}")\n\t\t)')
    ix=s.index('\n\t\t(fp_text user')
    s=s[:ix]+''.join(out)+s[ix:]
    for n in range(1,9):
        pat=r'(\(pad "'+str(n)+r'" smd roundrect\s*\(at )(-?2\.475)( [-\d.]+ 180\)\s*\(size )1\.95 0\.6'
        def mod(m):return m.group(1)+('-3.6' if m.group(2).startswith('-') else '3.6')+m.group(3)+'1.6 0.6'
        s, count=re.subn(pat,mod,s)
        assert count==1,(n,count)
    assert 'SOIC-8_3.9x4.9mm_P1.27mm' in s  # old model path
    s=s.replace('SOIC-8_3.9x4.9mm_P1.27mm.step','SOP-8_5.28x5.23mm_P1.27mm.step')
    return s
pcb=edit_fp(pcb,'U2',u2_fix)

# compensate pad displacement: add copper extensions from old pad centers to new pad centers.
# These are mechanical ECO patch routes and MUST be verified with actual KiCad DRC before manufacture.
ix=pcb.index('\n\t(segment')
connectors=[]
# U2 instance at (96.476,65.0002), 180 degrees - local x neg -> PCB x pos
for n in range(1,9):
    xold= -2.475 if n<5 else 2.475
    xnew= -3.6 if n<5 else 3.6
    yy={1:-1.905,2:-0.635,3:0.635,4:1.905,5:1.905,6:0.635,7:-0.635,8:-1.905}[n]
    name={1:'FLASH_CS',2:'SPI_MISO',3:'FLASH_WP_N',4:'GND_AUD',5:'SPI_MOSI',6:'SPI_SCK',7:'FLASH_HOLD_N',8:'+3V3'}[n]
    X=lambda x:round(96.476-x,6)
    Y=round(65.0002-yy,6)
    uid=uuid.uuid5(uuid.NAMESPACE_URL,'VoiceMemory-v1-u2-sop208-adapter-'+str(n))
    connectors.append(f'\n\t(segment\n\t\t(start {X(xold):.6f} {Y:.6f})\n\t\t(end {X(xnew):.6f} {Y:.6f})\n\t\t(width 0.20)\n\t\t(layer "F.Cu")\n\t\t(net "{name}")\n\t\t(uuid "{uid}")\n\t)')
pcb=pcb[:ix]+''.join(connectors)+pcb[ix:]

# 4) U3 Toshiba TLP592A(F) updated manufacturer pin naming while preserving pin numbers and existing DIP-6 pads.
def symrename(t):
    t=t.replace('AT25SF321B-SSHB','W25Q32RVCSJM').replace('AQV212','TLP592A')
    # U2 pinout compatible; only description/datasheet update
    t=t.replace('Renesas/Adesto W25Q32RVCSJM 32Mbit 2.7-3.6V SPI NOR flash, SOIC-8 150mil',
      'Winbond W25Q32RVCSJM 32Mbit SPI NOR, 2.7-3.6V, SOP-8 208mil; SPI 1/2/3/4/5/6/7/8 pinout')
    t=t.replace('Renesas/Adesto W25Q32RVCSJM 32Mbit SPI NOR flash, SOIC-8 150mil',
      'Winbond W25Q32RVCSJM 32Mbit SPI NOR 208mil SOP-8')
    t=t.replace('https://www.renesas.com/en/document/dst/at25sf321b-datasheet?r=1608806',
      'https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/w25q-rv/?__locale=en&partNo=W25Q32RVCSJM')
    t=t.replace('Panasonic TLP592A PhotoMOS GU DIP6 1 Form A. Pin3 is internal NC and must not be externally connected; A connection uses pins 4 and 6.',
      'Toshiba TLP592A(F) DIP-6 photorelay. 1=A,2=K,3=NC,4=Drain D1,5=Source (left unconnected),6=Drain D2. Output across pins 4/6.')
    t=t.replace('https://na.industrial.panasonic.com/products/relays-contactors/semiconductor-relays/photomosr/series/12544/model/90976',
      'https://toshiba.semicon-storage.com/info/TLP592A_datasheet_ja_20190624.pdf?did=17082&prodName=TLP592A')
    t=t.replace('SOIC-8_3.9x4.9mm_P1.27mm','SOP-8_5.28x5.23mm_P1.27mm')
    t=t.replace('PhotoMOS TLP592A SSR','PhotoMOS TLP592A(F) Toshiba SSR')
    t=t.replace('SPI NOR W25Q32RVCSJM flash','SPI NOR Winbond W25Q32RVCSJM flash')
    # Fix assigned value for instances (library and PCB separately)
    t=t.replace('(property "Value" "TLP592A"','(property "Value" "TLP592A(F)"')
    t=t.replace('(name "OUT1"','(name "DRAIN_D1"').replace('(name "OUT2"','(name "DRAIN_D2"').replace('(name "OUT_MID"','(name "SOURCE"')
    return t
src=SYM.read_text();src=symrename(src)
# one and only one source symbol named TLP592A; only one Winbond
assert src.count('(symbol "TLP592A"')==1 and src.count('(symbol "W25Q32RVCSJM"')==1
SYM.write_text(src)
src=SCH.read_text();src=symrename(src)
# 0603 C11/C19 schematic fields only
for ref in ('C11','C19'):
    # locate exact SCH instance by property Reference
    pos=src.index(f'(property "Reference" "{ref}"')
    a=src.rfind('\n\t(symbol',0,pos)
    assert a>=0
    a+=2; _,b=balanced(src,a)
    unit=src[a:b]
    assert 'Capacitor_SMD:C_0805_2012Metric' in unit
    unit=unit.replace('Capacitor_SMD:C_0805_2012Metric','Capacitor_SMD:C_0603_1608Metric')
    src=src[:a]+unit+src[b:]
assert src.count('(lib_id "Voice_Memory:W25Q32RVCSJM")')==1
assert src.count('(lib_id "Voice_Memory:TLP592A")')==1
SCH.write_text(src)
pcb=pcb.replace('(property "Value" "AQV212"','(property "Value" "TLP592A(F)"')
PCB.write_text(pcb)

report={'source':'voicememory-2026-10-05_162836(2).zip',
 'applied':['J1/J2 NPTH hole Y -4.32 => +4.32, pad positions/nets retained',
            'C11/C19 footprint to standard KiCad C_0603_1608Metric; 1uF/25V',
            'U2 W25Q32RVCSJM / KiCad SOP-8_5.28x5.23mm_P1.27mm; bridging segments added',
            'U3 TLP592A(F) DIP6 and pin naming; pad3/pad5 NC external; R20 original retained'],
 'not_changed':['R1-R20 0805 values','C3/C6/C9/C13 THT electrolytics','C1 1206 10uF','U4 NJM2732D','functional software specification'],
 'tests':'Static assertions and geometric approximations only. KiCad 10 CLI ERC/DRC NOT performed. Manufacturing release NOT approved.',
 'pcb_revision':'v1-eco-2026-10-30','component_count_expected':61}
rp=Path(__file__).resolve().parents[1]/'hardware/reports/ECO_2026-10-30.json'
rp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
