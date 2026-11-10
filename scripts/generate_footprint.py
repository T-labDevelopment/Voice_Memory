#!/usr/bin/env python3
"""Reproducibly generate a KiCad 10-compatible RJ45 8P8C footprint.
Datum: pin 1 center at (0, 0); component-side PCB layout (user-provided drawing).
"""
from pathlib import Path
import math
import re
import uuid

ROOT = Path(__file__).resolve().parent
NAME = 'RJ45_8P8C_THT_15.91x15.10'
OUT = ROOT / 'Voice_Memory.pretty' / f'{NAME}.kicad_mod'

def uid(s):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f'VoiceMemory/RJ45fix/2026-10-25/{s}'))

# Dimension references from user-provided drawing (PCB LAYOUT).
PITCH = 1.02
ROW_SEPARATION = 1.78
MOUNT_HOLE_DIAMETER = 3.20
MOUNT_HOLE_SPACING = 12.70
MOUNT_Y = 4.32
PIN_DRILL = 0.90
PIN_COPPER = 1.50  # chosen annulus; drill given on drawing
FRONT_OFFSET = 5.10   # front face to mounting post centre on supplied side view
BODY_DEPTH = 15.10
BODY_WIDTH = 15.91

# Pin 1 datum, conventional odd/even numbering, both rows preserved.
pins = [(n, (n-1)*PITCH, 0.0 if n%2 else ROW_SEPARATION) for n in range(1,9)]
xc = 7*PITCH/2
hole_l = (round(xc-MOUNT_HOLE_SPACING/2, 3), MOUNT_Y)
hole_r = (round(xc+MOUNT_HOLE_SPACING/2, 3), MOUNT_Y)
body_left = xc-BODY_WIDTH/2
body_right = xc+BODY_WIDTH/2
body_front = MOUNT_Y+FRONT_OFFSET
body_back = body_front - BODY_DEPTH

def fmt(v):
    return ('%.4f' % v).rstrip('0').rstrip('.') if abs(v)>1e-10 else '0'

parts = [f'''(footprint "{NAME}"
    (version 20260206)
    (generator "pcbnew")
    (generator_version "10.0")
    (layer "F.Cu")
    (descr "RJ45 8P8C vertical THT; 15.91x15.10mm body; 2x NPTH dia3.20 at 12.70 pitch, staggered 1.02x1.78 signal pads, per supplied mechanical drawing. Verify pin1 orientation before manufacturing.")
    (tags "RJ45 8P8C modular jack THT VoiceMemory")
    (property "Reference" "REF**"
        (at 3.57 -7.0 0)
        (layer "F.SilkS")
        (uuid "{uid('reference')}")
        (effects (font (size 1 1) (thickness 0.15)))
    )
    (property "Value" "{NAME}"
        (at 3.57 10.75 0)
        (layer "F.Fab")
        (uuid "{uid('value')}")
        (effects (font (size 0.8 0.8) (thickness 0.12)))
    )
    (attr through_hole)
''']

def line(x1,y1,x2,y2,layer,width,index):
    return f'    (fp_line (start {fmt(x1)} {fmt(y1)}) (end {fmt(x2)} {fmt(y2)}) (stroke (width {fmt(width)}) (type solid)) (layer "{layer}") (uuid "{uid(layer+str(index))}"))\n'

# Accurate body width/depth projection. Side view gives the post position 5.10mm from front.
for idx,(x1,y1,x2,y2) in enumerate([
    (body_left,body_back,body_right,body_back),
    (body_right,body_back,body_right,body_front),
    (body_right,body_front,body_left,body_front),
    (body_left,body_front,body_left,body_back),
]):
    parts.append(line(x1,y1,x2,y2,'F.Fab',0.10,idx))

# Courtyard encloses complete body and all holes (0.25mm margin).
left,right,back,front=body_left-.25,body_right+.25,body_back-.25,body_front+.25
for idx,(x1,y1,x2,y2) in enumerate([
    (left,back,right,back), (right,back,right,front),
    (right,front,left,front), (left,front,left,back),
]):
    parts.append(line(x1,y1,x2,y2,'F.CrtYd',0.05,idx))

# Silk avoids fixing NPTH post bores (both touch near side of plastic boundary).
parts.append(line(body_left,body_back,body_right,body_back,'F.SilkS',0.12,1))
parts.append(line(body_left,body_front,body_right,body_front,'F.SilkS',0.12,2))
parts.append('''    (fp_circle (center -1.4 -1.4) (end -1.05 -1.4)
        (stroke (width 0.12) (type solid)) (fill none)
        (layer "F.SilkS") (uuid "'''+uid('pin1_silk')+'''"))
''')
parts.append('''    (fp_text user "${REFERENCE}"
        (at 3.57 7.7 0)
        (layer "F.Fab")
        (uuid "'''+uid('ref_fab')+'''" )
        (effects (font (size 1 1) (thickness 0.15)))
    )
''')

for n,x,y in pins:
    shape = 'roundrect' if n==1 else 'circle'
    extra = ' (roundrect_rratio 0.2)' if n==1 else ''
    parts.append(f'    (pad "{n}" thru_hole {shape} (at {fmt(x)} {fmt(y)}) (size {fmt(PIN_COPPER)} {fmt(PIN_COPPER)}) (drill {fmt(PIN_DRILL)}) (layers "*.Cu" "*.Mask"){extra} (uuid "{uid("pin"+str(n))}"))\n')
for idx,(x,y) in enumerate([hole_l,hole_r]):
    parts.append(f'    (pad "" np_thru_hole circle (at {fmt(x)} {fmt(y)}) (size {fmt(MOUNT_HOLE_DIAMETER)} {fmt(MOUNT_HOLE_DIAMETER)}) (drill {fmt(MOUNT_HOLE_DIAMETER)}) (layers "*.Cu" "*.Mask") (uuid "{uid("hole"+str(idx))}"))\n')
parts.append(')\n')
OUT.write_text(''.join(parts),encoding='utf-8')

# Strict geometric self-checks independent of KiCad GUI.
assert len(pins)==8 and len({n for n,x,y in pins})==8
assert math.isclose(hole_r[0]-hole_l[0],12.70,abs_tol=1e-6)
assert all(math.isclose(pins[i+2][1]-pins[i][1],2.04,abs_tol=1e-8) for i in range(6))
assert math.isclose(pins[1][2]-pins[0][2],ROW_SEPARATION)
assert math.isclose((body_right-body_left),BODY_WIDTH)
assert math.isclose((body_front-body_back),BODY_DEPTH)
assert (hole_l[0]+hole_r[0])/2==xc
s=OUT.read_text(encoding='utf-8')
assert len(re.findall(r'\(pad "[1-8]" thru_hole',s))==8
assert len(re.findall(r'\(pad "" np_thru_hole',s))==2
assert s.count('(')==s.count(')')
print(f'CREATED {OUT} ({OUT.stat().st_size} bytes)')
print('pins:',pins)
print('mounting holes:',hole_l,hole_r,'drill diameter',MOUNT_HOLE_DIAMETER)
print('body:',body_left,body_right,body_back,body_front)
print('Geometric checks: PASS (KiCad ERC/DRC: NOT RUN)')
