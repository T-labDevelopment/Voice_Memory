#!/usr/bin/env python3
"""VoiceMemory T-Display ESP32 Rev.A - five 12-mm switch schematic/PCB edit.
Works only against the source-layout revision used in this conversation.
No tracks/zones are generated, and KiCad ERC/DRC remain to be executed.
"""
from __future__ import annotations
import csv, io, json, math, re, uuid
from pathlib import Path

root = Path(__file__).resolve().parent
schp = root/'VoiceMemory_TDisplay.kicad_sch'
pcbp = root/'VoiceMemory_TDisplay.kicad_pcb'
bomp = root/'bom_draft.csv'
pinmap = root/'pinmap.csv'
# CH switches are input-only pins first, then GPIO15 (MTDO strap).
ch = [
    ('SW2','CH1_SELECT','SW_CH1_N','36','R23',(127.00,323.85),(109.9,87.7),(68.0,69.5)),
    ('SW3','CH2_SELECT','SW_CH2_N','37','R24',(177.80,323.85),(106.0,93.0),(87.0,69.5)),
    ('SW4','CH3_SELECT','SW_CH3_N','38','R25',(228.60,323.85),(109.9,93.0),(68.0,87.0)),
    ('SW5','CH4_SELECT','SW_CH4_N','15','R26',(279.40,323.85),(106.0,98.3),(87.0,87.0)),
]
local_fp='VoiceMemory_TDisplay:SW_PUSH-12mm'

def bx(s,at):
    d=0; quoted=False; escaped=False
    for i in range(at,len(s)):
        c=s[i]
        if quoted:
            if escaped: escaped=False
            elif c=='\\':escaped=True
            elif c=='"':quoted=False
        else:
            if c=='"':quoted=True
            elif c=='(':d+=1
            elif c==')':
                d-=1
                if d==0:return s[at:i+1]
                if d<0:raise RuntimeError('Bad S-expression')
    raise RuntimeError('Unbalanced S-expression')

def sym(s,ref):
    for m in re.finditer(r'\(symbol \(lib_id "[^"]+"\) \(at [-\d.]+ [-\d.]+ [-\d.]+\)',s):
        b=bx(s,m.start())
        if f'(property "Reference" "{ref}"' in b:return m.start(), b
    raise RuntimeError('Symbol not found '+ref)

def fp(s,ref):
    for m in re.finditer(r'\(footprint "[^"]+"\s*\(layer "F.Cu"\)',s):
        b=bx(s,m.start())
        if f'(property "Reference" "{ref}"' in b:return m.start(),b
    raise RuntimeError('Footprint not found '+ref)

def replace_uuid(s):
    # Unique identification; distinct UUIDs for PCB and schematic objects.
    return re.sub(r'\(uuid "[a-f0-9-]{36}"\)',lambda m:'(uuid "'+str(uuid.uuid4())+'")',s)

def move_schematic(b,oldxy,newxy):
    dx,dy=newxy[0]-oldxy[0],newxy[1]-oldxy[1]
    def f(m):
        x,y,a=float(m[1]),float(m[2]),m[3]
        return '(at '+f'{x+dx:.2f}'.rstrip('0').rstrip('.')+' '+f'{y+dy:.2f}'.rstrip('0').rstrip('.')+' '+a+')'
    return re.sub(r'\(at ([-\d.]+) ([-\d.]+) (\d+)\)',f,b)

def new_sym_from(old,newref,newval,newxy,oldxy,newfp=None,desc=None):
    b=move_schematic(old,oldxy,newxy)
    original=old_value= re.search(r'\(property "Reference" "([^"]+)"',b).group(1)
    b=b.replace(f'(property "Reference" "{original}"',f'(property "Reference" "{newref}"',1)
    b=re.sub(r'\(reference "'+re.escape(original)+r'"\)',f'(reference "{newref}")',b)
    b=re.sub(r'\(property "Value" "[^"]+"',f'(property "Value" "{newval}"',b,count=1)
    if newfp:
        b=re.sub(r'\(property "Footprint" "[^"]+"',f'(property "Footprint" "{newfp}"',b,count=1)
    if desc:
        b=re.sub(r'\(property "Description" "[^"]*"',f'(property "Description" "{desc}"',b,count=1)
    b=replace_uuid(b)
    return b, re.search(r'\(uuid "([a-f0-9-]{36})"\)',b).group(1)

def label_from(src,name,x,y,orient):
    # Every global label and its text origin need updating together.
    i=src.find(f'(global_label "{name}" (shape passive) (at {x:g} {y:g} {orient})')
    if i<0:raise RuntimeError(f'Cannot locate reference label {name}, {x} {y} {orient}')
    return bx(src,i)

def clone_label(old,new_net,oldxy,newxy):
    b=move_schematic(old,oldxy,newxy)
    b=b.replace(re.search(r'\(global_label "([^"]+)"',b).group(0),f'(global_label "{new_net}"',1)
    return replace_uuid(b)

# 1. Schematic: dedicated 12mm REC + 4 CH + pullups, 1.27mm global labels.
s=schp.read_text(encoding='utf-8')
if '(paper "A3")' not in s:raise RuntimeError('Unexpected sheet size')
s=s.replace('(paper "A3")','(paper "A2")',1)
old_sw_idx,old_sw=sym(s,'SW1'); old_ridx,old_r=sym(s,'R19')
old_fp='Button_Switch_THT:SW_PUSH_6mm_H4.3mm'
if old_sw.count(old_fp)!=1:raise RuntimeError('SW1 footprint mismatch')
new_sw=old_sw.replace(old_fp,local_fp).replace('Optional separate REC button; existing T-Display buttons handle memory select and play','Required dedicated 12mm REC button; CH1-CH4 also have dedicated physical buttons')
s=s[:old_sw_idx]+new_sw+s[old_sw_idx+len(old_sw):]
# Preserve original SW1 UUID and net paths, no change to its positioning in schematic.
parts=[]; pin_assignments={}
for swr,val,net,gpio,rr,s_xy,r_xy,pcb_center in ch:
    bs,suuid=new_sym_from(old_sw,swr,val,s_xy,(163.83,264.16),local_fp,f'12mm dedicated CH selector; active low on GPIO{gpio}; external 10k pull-up')
    br,ruuid=new_sym_from(old_r,rr,'10k',r_xy if False else (s_xy[0],354.33),(341.63,226.06))
    parts += [bs,br]
    pin_assignments[swr]={'net':net,'gpio':gpio,'pin':{'36':11,'37':10,'38':9,'15':18}[gpio],'symbol_uuid':suuid,'resistor':rr,'resistor_uuid':ruuid,'pcb_center':pcb_center,'resistor_pcb':r_xy}
# insert before label array as valid top-level blocks
label_idx=s.find('(global_label "')
if label_idx<0: raise RuntimeError('No labels')
s=s[:label_idx]+'\n'.join(parts)+'\n'+s[label_idx:]
# exact original source global labels after edit
switch_label=label_from(s,'SW_REC_N',158.75,264.16,180)
gnd_switch_label=label_from(s,'GND_AUD',168.91,264.16,0)
ref_3v3=label_from(s,'+3V3',337.82,226.06,180)
ref_r19_output=label_from(s,'SW_REC_N',345.44,226.06,0)
added_labels=[]
for swr,val,net,gpio,rr,s_xy,r_xy,pcb_center in ch:
    x,y=s_xy; ry=354.33
    # switch pins at x ± 5.08, active-low to GND
    added_labels += [clone_label(switch_label,net,(158.75,264.16),(x-5.08,y)),
                     clone_label(gnd_switch_label,'GND_AUD',(168.91,264.16),(x+5.08,y))]
    # resistor oriented 90deg, pins x ± 3.81
    added_labels += [clone_label(ref_3v3,'+3V3',(337.82,226.06),(x-3.81,ry)),
                     clone_label(ref_r19_output,net,(345.44,226.06),(x+3.81,ry))]
    pin=pin_assignments[swr]['pin']
    if gpio in ('36','37','38'):
        py={36:223.52,37:226.06,38:228.60}[int(gpio)]; px=101.60
    else:px,py=50.80,236.22
    needle=re.compile(r'\(no_connect \(at '+f'{px:g}'+r' '+f'{py:g}'+r'\) \(uuid "[a-f0-9-]{36}"\)\)')
    s,n=needle.subn('',s)
    if n!=1:raise RuntimeError(f'Expected no_connect at {px},{py}, got {n}')
    # Existing pattern for module net labels, use orientation based on which edge the pin is on
    # A global label pin's shape is passive and connects at (x,y).
    orient=180 if px>76 else 0
    added_labels.append(f'(global_label "{net}" (shape passive) (at {px:g} {py:g} {orient})\n(effects (font (size 0.9 0.9)) (justify '+('right' if orient==180 else 'left')+'))\n(uuid "'+str(uuid.uuid4())+'")\n(property "Intersheetrefs" "${INTERSHEET_REFS}" (at '+f'{px:g} {py:g}'+ ' 0) (effects (font (size 0.9 0.9)) (hide yes))))')
s=s.rstrip()[:-1]+'\n'+'\n'.join(added_labels)+'\n)\n'
if bx(s,0).strip()!=s.strip():raise RuntimeError('Schematic S-expression not balanced')
if len(list(re.finditer(r'\(symbol \(lib_id "Switch:SW_Push"\)',s)))!=5:raise RuntimeError('Switches not 5')
if s.count(local_fp)<1:raise RuntimeError('no FP switch assign')
for swr,v in pin_assignments.items():
    assert s.count(f'(global_label "{v["net"]}"')==3
schp.write_text(s,encoding='utf-8')

# 2. Full *official* KiCad Button_Switch_THT/SW_PUSH-12mm mechanical footprint copied
# verbatim from KiCad/kicad-footprints master; source blob SHA 6e8f066cfacb6b191768e98bb9497655634127f7
# The PCB instance is composed using same pad centers, size, drill, lines and courtyard.
std_switch = '''(module SW_PUSH-12mm (layer F.Cu) (tedit 5D160D14)
  (descr "SW PUSH 12mm https://www.e-switch.com/system/asset/product_line/data_sheet/143/TL1100.pdf")
  (tags "tact sw push 12mm")
  (fp_text reference REF** (at 6.08 -4.66) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value SW_PUSH-12mm (at 6.62 9.93) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_line (start 0.25 8.5) (end 12.25 8.5) (layer F.Fab) (width 0.1))
  (fp_line (start 0.25 -3.5) (end 12.25 -3.5) (layer F.Fab) (width 0.1))
  (fp_line (start 12.25 -3.5) (end 12.25 8.5) (layer F.Fab) (width 0.1))
  (fp_text user %R (at 6.35 2.54) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_line (start 0.1 -3.65) (end 12.4 -3.65) (layer F.SilkS) (width 0.12))
  (fp_line (start 12.4 0.93) (end 12.4 4.07) (layer F.SilkS) (width 0.12))
  (fp_line (start 12.4 8.65) (end 0.1 8.65) (layer F.SilkS) (width 0.12))
  (fp_line (start 0.1 -0.93) (end 0.1 -3.65) (layer F.SilkS) (width 0.12))
  (fp_line (start -1.77 -3.75) (end 14.25 -3.75) (layer F.CrtYd) (width 0.05))
  (fp_line (start -1.77 -3.75) (end -1.77 8.75) (layer F.CrtYd) (width 0.05))
  (fp_line (start 14.25 8.75) (end 14.25 -3.75) (layer F.CrtYd) (width 0.05))
  (fp_line (start 14.25 8.75) (end -1.77 8.75) (layer F.CrtYd) (width 0.05))
  (fp_circle (center 6.35 2.54) (end 10.16 5.08) (layer F.SilkS) (width 0.12))
  (fp_line (start 0.25 -3.5) (end 0.25 8.5) (layer F.Fab) (width 0.1))
  (fp_line (start 0.1 8.65) (end 0.1 5.93) (layer F.SilkS) (width 0.12))
  (fp_line (start 0.1 4.07) (end 0.1 0.93) (layer F.SilkS) (width 0.12))
  (fp_line (start 12.4 5.93) (end 12.4 8.65) (layer F.SilkS) (width 0.12))
  (fp_line (start 12.4 -3.65) (end 12.4 -0.93) (layer F.SilkS) (width 0.12))
  (pad 1 thru_hole oval (at 12.5 0) (size 3.048 1.85) (drill 1.3) (layers *.Cu *.Mask))
  (pad 2 thru_hole oval (at 12.5 5) (size 3.048 1.85) (drill 1.3) (layers *.Cu *.Mask))
  (pad 1 thru_hole oval (at 0 0) (size 3.048 1.85) (drill 1.3) (layers *.Cu *.Mask))
  (pad 2 thru_hole oval (at 0 5) (size 3.048 1.85) (drill 1.3) (layers *.Cu *.Mask))
  (model ${KISYS3DMOD}/Button_Switch_THT.3dshapes/SW_PUSH-12mm.wrl
    (at (xyz 0 0 0))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 0))
  )
)\n'''
(root/'VoiceMemory_TDisplay.pretty'/'SW_PUSH-12mm.kicad_mod').write_text(std_switch,encoding='utf-8')

# 3. PCB: insert fully editable native KiCad 10 switch footprint instances.
# Numeric pad positions and geometry are from KiCad official SW_PUSH-12mm footprint.
def pcb_switch(ref,value,net,suid,center):
    x=round(center[0]-6.24,2); y=round(center[1]-2.5,2)
    def cid():return str(uuid.uuid4())
    def geom_line(layer,coords,width):
        x1,y1,x2,y2=coords
        return f'''\n  (fp_line (start {x1:g} {y1:g}) (end {x2:g} {y2:g}) (stroke (width {width}) (type solid)) (layer "{layer}") (uuid "{cid()}"))'''
    outline=''
    fab=[(.25,8.5,12.25,8.5),(.25,-3.5,12.25,-3.5),(12.25,-3.5,12.25,8.5),(.25,-3.5,.25,8.5)]
    silk=[(.1,-3.65,12.4,-3.65),(.1,8.65,12.4,8.65),(12.4,.93,12.4,4.07),(.1,-.93,.1,-3.65),(.1,8.65,.1,5.93),(.1,4.07,.1,.93),(12.4,5.93,12.4,8.65),(12.4,-3.65,12.4,-.93)]
    courtyard=[(-1.77,-3.75,14.25,-3.75),(-1.77,-3.75,-1.77,8.75),(14.25,8.75,14.25,-3.75),(14.25,8.75,-1.77,8.75)]
    for coords in fab:outline+=geom_line('F.Fab',coords,'0.1')
    for coords in silk:outline+=geom_line('F.SilkS',coords,'0.12')
    for coords in courtyard:outline+=geom_line('F.CrtYd',coords,'0.05')
    outline+=f'''\n  (fp_circle (center 6.35 2.54) (end 10.16 5.08) (stroke (width 0.12) (type solid)) (fill none) (layer "F.SilkS") (uuid "{cid()}"))'''
    pads=''
    for num,px,py in [(1,12.5,0),(2,12.5,5),(1,0,0),(2,0,5)]:
        n=net if num==1 else 'GND_AUD'
        pads+=f'''\n  (pad "{num}" thru_hole oval (at {px:g} {py:g}) (size 3.048 1.85) (drill 1.3) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (net "{n}") (pinfunction "{num}") (pintype "passive") (uuid "{cid()}"))'''
    return f'''(footprint "{local_fp}"
  (layer "F.Cu") (uuid "{cid()}") (at {x:g} {y:g} 0)
  (descr "KiCad official SW_PUSH-12mm, TL1100 style, 12mm tactile; verify actual switch pin assignment")
  (tags "tact sw push 12mm")
  (property "Reference" "{ref}" (at 6.08 -4.66 0) (layer "F.SilkS") (uuid "{cid()}") (effects (font (size 1 1) (thickness 0.15))))
  (property "Value" "{value}" (at 6.62 9.93 0) (layer "F.Fab") (uuid "{cid()}") (effects (font (size 1 1) (thickness 0.15))))
  (path "/{suid}") (sheetname "/") (sheetfile "VoiceMemory_TDisplay.kicad_sch")
  (units (unit (name "A") (pins "1" "2")))
  (attr through_hole) (duplicate_pad_numbers_are_jumpers no){outline}{pads}
  (embedded_fonts no)
  (model "${{KICAD10_3DMODEL_DIR}}/Button_Switch_THT.3dshapes/SW_PUSH-12mm.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))
)'''

b=pcbp.read_text(encoding='utf-8')
# SW1 old footstep entirely replaced with footprint matching official 12mm and preserve schematic uuid.
i,fpsw=fp(b,'SW1');newrec=pcb_switch('SW1','REC_ARM','SW_REC_N','d4a22a7f-d4a2-44a2-a4a2-d4a22a7fd4a2',(77.5,104.5))
b=b[:i]+newrec+b[i+len(fpsw):]
# clone R19 from original updated text and replace origin, ref/path/net/uuid for each R23-26
oldri,oldrf=fp(b,'R19')
new_fps=[]
for swr,val,net,gpio,rr,s_xy,r_xy,center in ch:
    x,y=r_xy
    rfp=replace_uuid(oldrf)
    rfp=rfp.replace('(property "Reference" "R19"',f'(property "Reference" "{rr}"',1)
    rfp=rfp.replace('(net "SW_REC_N")',f'(net "{net}")')
    rfp=rfp.replace('(at 106 82.4 90)',f'(at {x:g} {y:g} 90)',1)
    rfp,npath=re.subn(r'\(path "/[a-f0-9-]{36}"\)',f'(path "/{pin_assignments[swr]["resistor_uuid"]}")',rfp,count=1)
    if npath!=1:raise RuntimeError('RFP path change failed')
    if '(path "/'+pin_assignments[swr]['resistor_uuid']+'")' not in rfp:raise RuntimeError('RFP path bad')
    # note: no schematic UUID inside pcb property names beyond PATH
    new_fps.extend([rfp,pcb_switch(swr,val,net,pin_assignments[swr]['symbol_uuid'],center)])
# insert before edges, after all existing footprints. Do not reorder existing footprints.
firstedge=b.find('(gr_line (start 100.2 51.8)')
if firstedge<0:raise RuntimeError('expected old board edge')
b=b[:firstedge]+'\n'+'\n'.join(new_fps)+'\n'+b[firstedge:]
# board outline left x from 100.2 to 56.5; other edges remain exactly unchanged
edge_head=b[firstedge+len('\n'+'\n'.join(new_fps)+'\n'):]
edge_head=edge_head.replace('100.2','56.5')
b=b[:firstedge+len('\n'+'\n'.join(new_fps)+'\n')]+edge_head
# New PCB should have 53 components: original45 + 4CH +4 resistors; SW1 replaces original
if len(re.findall(r'\(footprint "[^\n]+',b))!=53:raise RuntimeError('expected 53 footprints')
for ref in ['SW1','SW2','SW3','SW4','SW5']:
    ii,bb=fp(b,ref)
    if local_fp not in bb:raise RuntimeError(ref+' missing 12mm footprint')
    if bb.count('(pad "1"')!=2 or bb.count('(pad "2"')!=2:raise RuntimeError(ref+' missing duplicated pads')
for ref in ['R23','R24','R25','R26']:
    ii,bb=fp(b,ref)
    if '(net "+3V3")' not in bb:raise RuntimeError(ref+' missing 3V3')
if bx(b,0).strip()!=b.strip():raise RuntimeError('PCB S-expr is not balanced')
pcbp.write_text(b,encoding='utf-8')

# 4. BOM - append four switches, four resistors; update REC footprint.
import collections
with bomp.open(encoding='utf-8-sig',newline='') as f:
    rdr=csv.DictReader(f); fieldnames=rdr.fieldnames; rows=list(rdr)
assert fieldnames is not None
prior={row['Ref']:row for row in rows}
if len(prior)!=45 or len(rows)!=45: raise RuntimeError('Expected 45 BOM lines')
prior['SW1']['Footprint']=local_fp
prior['SW1']['Status']='BOARD_PLACED_PART_NUMBER_VERIFY'
for swr,val,net,gpio,rr,s_xy,r_xy,center in ch:
    sw_row={key:'' for key in fieldnames}
    sw_row.update({'Ref':swr,'Part':'Switch:SW_Push','Value':val,'Qty':'1','Footprint':local_fp,
        'Status':'BOARD_PLACED_PART_NUMBER_VERIFY','BodyDimensions':'12x12mm 4pin (pads 12.5mm x 5mm)',
        'SupplyVerification':'manufacturer switch model not fixed; verify exact terminal rows and 1.3mm holes'})
    rr_row={key:'' for key in fieldnames}
    rr_row.update({'Ref':rr,'Part':'Device:R','Value':'10k','Qty':'1','Footprint':'Resistor_SMD:R_0805_2012Metric',
        'Status':'ADDED_0805_PULLOUT','RatedVoltage':'3.3V logic','SizeRule':'0805 imperial minimum',
        'SupplyVerification':'3.3V pull-up for CH GPIO; confirm stock and tolerance'})
    rows.extend([sw_row,rr_row])
assert len(rows)==53
with bomp.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fieldnames,lineterminator='\n');writer.writeheader();writer.writerows(rows)

# 5. Pinmap update: preserve all existing connections.
with pinmap.open('r',encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f);fn=reader.fieldnames; pr=list(reader)
assert fn is not None
for swr,val,net,gpio,rr,s_xy,r_xy,center in ch:
    pr.append({'Name':f'{val}','GPIO':gpio,'Dir':'IN','Net':net,
      'Notes':f'12mm physical {swr}, active LOW, external 10k pull-up; '+('GPIO15 is a boot strap and LOW suppresses ROM log at reset' if gpio=='15' else 'input only, no internal pull-up')})
with pinmap.open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fn,lineterminator='\n');writer.writeheader();writer.writerows(pr)

# 6. Board switches have 12x12mm fab bodies but 16.02x12.5 courtyard. Layout verification.
placements=[]
for ref,center in [('SW1',(77.5,104.5))]+[(swr,data['pcb_center']) for swr,data in pin_assignments.items()]:
    x,y=center
    placements.append({'ref':ref,'center':[x,y], 'footprint_origin':[round(x-6.24,2),round(y-2.5,2)],
        'courtyard':[round(x-8.01,2),round(y-6.25,2),round(x+8.01,2),round(y+6.25,2)]})
board=[56.5,51.8,160.8,116.2]
for p in placements:
    a,bx_,c,d=p['courtyard']
    if a<board[0]+2 or bx_<board[1]+2 or c>board[2]-2 or d>board[3]-2:
        raise RuntimeError(f'Edge clearance less than 2mm for {p}')
for i,p in enumerate(placements):
    for o in placements[i+1:]:
        a,b_,c,d=p['courtyard']; e,f,g,h=o['courtyard']
        if min(c,g)>max(a,e) and min(d,h)>max(b_,f):raise RuntimeError('Switch courier overlap '+p['ref']+' '+o['ref'])

# Board labels (F.SilkS) must not lie inside switch courtyard.
labels=[]
for ref,name,center in [('SW1','REC',(77.5,104.5))]+[(p[0],p[1][:3],p[-1]) for p in ch]:
    x,y=center
    ly=y-9.0
    labels.append(f'(gr_text "{name}" (at {x:g} {ly:g} 0) (layer "F.SilkS") (uuid "{uuid.uuid4()}") (effects (font (size 1 1) (thickness 0.15))))')
b=pcbp.read_text(encoding='utf-8')
lastidx=b.rfind('(embedded_fonts no)')
if lastidx<0:raise RuntimeError('No final embedded_fonts')
b=b[:lastidx]+ '\n'+'\n'.join(labels)+'\n'+b[lastidx:]
if bx(b,0).strip()!=b.strip():raise RuntimeError('PCB expression malformed after adding silk legend')
pcbp.write_text(b,encoding='utf-8')

# 7. Separate structured placement log for user edits and Git diff.
with (root/'PCB_BUTTONS_JA.csv').open('w',newline='',encoding='utf-8-sig') as f:
    wr=csv.writer(f);wr.writerow(['Ref','Function','Net','GPIO','Footprint','CenterX','CenterY','Status'])
    wr.writerow(['SW1','REC','SW_REC_N',13,local_fp,77.5,104.5,'Replacement 6mm to 12mm'])
    for swr,val,net,gpio,rr,s_xy,r_xy,center in ch:
        wr.writerow([swr,val,net,gpio,local_fp,*center,'Added dedicated button'])
        wr.writerow([rr,'10k pullup',net,gpio,'Resistor_SMD:R_0805_2012Metric',*r_xy,'Added'])

report={'source_schematic_pins':{'CH1':36,'CH2':37,'CH3':38,'CH4':15,'REC':13},
    'new_parts':8,'total_parts':53,'switches':5,'pullups':4,
    'footprint':local_fp,'board_mm':board,'board_size_mm':[104.3,64.4],
    'switch_courtyards':placements,'source_switch_official_sha':'6e8f066cfacb6b191768e98bb9497655634127f7',
    'routing':'not started','kicad10_erc':'not executed','kicad10_drc':'not executed',
    'boot_caveat':'GPIO15 LOW during reset disables ROM boot messages; no GPIO12/2 assignment',
    'mechanical_caveat':'Verify chosen physical 12mm switch pad pinout and drill size; generic KiCad TL1100 geometry may not fit every 12mm part.'}
(root/'button_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
