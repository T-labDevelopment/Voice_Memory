#!/usr/bin/env python3
"""Make only sourcing-driven capacitor updates to VoiceMemory v1 ECO.

Source geometry: original project's standard KiCad10 C_0603_1608Metric footprint
(exact IPC nominal shapes/dimensions already embedded in C11/C19).
This script edits real PCB footprints and schematic instance metadata and does
not create a simplified copy of standard KiCad library symbols.

CAUTION: This does not run KiCad 10 ERC/DRC or copper-zone refill.
"""
from pathlib import Path
import re, json, datetime, hashlib
BASE=Path(__file__).resolve().parents[1]
P=BASE/'hardware/kicad/voicememory'
SCH=P/'voicememory.kicad_sch'; PCB=P/'voicememory.kicad_pcb'
TARGETS={
    'C2': ('1uF/25V X5R','1uF/25V X6S'),
    'C4': ('1uF/25V X5R','1uF/25V X6S'),
    **{f'C{n}':('0.1uF/50V','0.1uF/100V X7R') for n in [7,8,10,14,15,16,17]},
}
# Old 2012 footprint has pad centers +/-0.95, nominal silk at +/-0.735.
# The KiCad 10 standard 1608 footprint embedded in C11/C19 has centers +/-0.775,
# pads (0.9 x 0.95), silk at +/-0.51, courtyard +/-1.48 x +/-0.73.

def balanced(s,i):
    assert s[i]=='('
    q=False; esc=False; d=0
    for j in range(i,len(s)):
        c=s[j]
        if q:
            if esc:esc=False
            elif c=='\\':esc=True
            elif c=='"':q=False
        elif c=='"':q=True
        elif c=='(':d+=1
        elif c==')':
            d-=1
            if d==0:return j+1
    raise ValueError('S-expression unbalanced')

def top(s,tag):
    return [(m.start()+1,balanced(s,m.start()+1)) for m in re.finditer(r'^\t\('+re.escape(tag)+r'\s',s,re.M)]

def find_block(s,tag,ref):
    hits=[]
    for a,b in top(s,tag):
        if re.search(r'\(property "Reference" "'+re.escape(ref)+r'"',s[a:b]):hits.append((a,b))
    if len(hits)!=1:raise ValueError((tag,ref,len(hits)))
    return hits[0]

def substitute_one(s,old,new,what=''):
    if s.count(old)!=1:raise ValueError(f'{what} expected one {old}: {s.count(old)}')
    return s.replace(old,new,1)

def replace_fp(block,ref,oldval,newval):
    block=substitute_one(block,'(footprint "Capacitor_SMD:C_0805_2012Metric"','(footprint "Capacitor_SMD:C_0603_1608Metric"',ref)
    block=re.sub(r'\(descr "Capacitor SMD 0805[^"\n]+"\)',
       '(descr "Capacitor SMD 0603 (1608 Metric), IPC-7351 nominal; standard KiCad C_0603_1608Metric")',block,count=1)
    # Only pad/value dimension changes. Preserve all UUIDs, nets, and part position.
    block=substitute_one(block,'(property "Value" "'+oldval+'"','(property "Value" "'+newval+'"',ref)
    # Preserve original reference, value locations and rotations as drawn.
    matches=re.findall(r'\(fp_line.*?\(layer "F\.SilkS"\).*?\(uuid "[^"]+"\)\s*\)',block,re.S)
    assert len(matches)==2,(ref,len(matches))
    for n,original in enumerate(matches):
        ordinate='0.51' if n==0 else '-0.51'
        patched=re.sub(r'\(start [^)]*\)',f'(start -0.14058 {ordinate})',original,count=1)
        patched=re.sub(r'\(end [^)]*\)',f'(end 0.14058 {ordinate})',patched,count=1)
        block=substitute_one(block,original,patched,ref+' silk')
    block=substitute_one(block,'(start -1.7 -0.98)','(start -1.48 -0.73)',ref)
    block=substitute_one(block,'(end 1.7 0.98)','(end 1.48 0.73)',ref)
    block=substitute_one(block,'(start -1 -0.625)','(start -0.8 -0.4)',ref)
    block=substitute_one(block,'(end 1 0.625)','(end 0.8 0.4)',ref)
    if block.count('(size 1 1.45)')!=2:raise ValueError(ref+' pads')
    block=block.replace('(size 1 1.45)','(size 0.9 0.95)')
    for x,xx in [('-0.95','-0.775'),('0.95','0.775')]:
        n=0
        for angle in ('270','180','90','0',''):
            old=f'(at {x} 0'+(' '+angle if angle else '')+')'
            new=f'(at {xx} 0'+(' '+angle if angle else '')+')'
            if old in block:
                block=block.replace(old,new,1);n+=1;break
        if n!=1:raise ValueError((ref,'pad',x))
    block=substitute_one(block,'C_0805_2012Metric.step','C_0603_1608Metric.step',ref)
    assert block.count('(pad "1"')==1 and block.count('(pad "2"')==1
    assert '(size 0.9 0.95)' in block
    return block

def edit_sch_unit(unit,ref,oldval,newval):
    unit=substitute_one(unit,'(property "Footprint" "Capacitor_SMD:C_0805_2012Metric"',
                        '(property "Footprint" "Capacitor_SMD:C_0603_1608Metric"',ref)
    # value is also in schematic instance; it is not a library symbol type modification
    return substitute_one(unit,'(property "Value" "'+oldval+'"','(property "Value" "'+newval+'"',ref)

pcb_crlf=b'\r\n' in PCB.read_bytes()
sch_crlf=b'\r\n' in SCH.read_bytes()
pcb=PCB.read_bytes().decode('utf-8').replace('\r\n','\n')
sch=SCH.read_bytes().decode('utf-8').replace('\r\n','\n')
results=[]
for ref,(oldval,newval) in TARGETS.items():
    # Board edit
    a,b=find_block(pcb,'footprint',ref)
    old=pcb[a:b]
    old_pads=re.findall(r'\(net "([^"]+)"\)',old)
    new=replace_fp(old,ref,oldval,newval)
    assert re.findall(r'\(net "([^"]+)"\)',new)==old_pads,(ref,'pad nets')
    pcb=pcb[:a]+new+pcb[b:]
    # Schematic edit
    a,b=find_block(sch,'symbol',ref)
    patched=edit_sch_unit(sch[a:b],ref,oldval,newval)
    sch=sch[:a]+patched+sch[b:]
    results.append({'ref':ref,'from':oldval,'to':newval,'new_footprint':'Capacitor_SMD:C_0603_1608Metric',
                    'retained_net_names':old_pads})
# Verify exactly 9 and old contacts/others persisted
assert len(results)==9
for ref in ('C1','C3','C5','C6','C9','C11','C12','C13','C18','C19'):
  assert find_block(pcb,'footprint',ref) and find_block(sch,'symbol',ref)
PCB.write_bytes((pcb.replace('\n','\r\n') if pcb_crlf else pcb).encode('utf-8'))
SCH.write_bytes((sch.replace('\n','\r\n') if sch_crlf else sch).encode('utf-8'))
OUT=BASE/'hardware/reports/CAP_SOURCING_2026-11-10.json'
OUT.write_text(json.dumps({'date':'2026-11-10','base':'v1-eco-2026-10-30',
    'modifications':results,
    'sources':{'0.1uF':'https://akizukidenshi.com/catalog/g/g114559/',
              '1uF':'https://akizukidenshi.com/catalog/g/g116993/'},
    'limitations':['KiCad 10 official ERC/DRC not available in environment',
                   'GND copper zone is unfilled in source and must be refilled using KiCad',
                   'Direct copper attachment of some legacy pads was already absent and needs review',
                   'Physical solderability/trace spacing not verified by official DRC']},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'changed':len(results),'refs':list(TARGETS),'pcb_sha256':hashlib.sha256(pcb.encode()).hexdigest(),
                  'sch_sha256':hashlib.sha256(sch.encode()).hexdigest()},indent=2))
