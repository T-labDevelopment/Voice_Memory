#!/usr/bin/env python3
"""Offset existing R2/R3 0.75mm away from new 208mil Flash footprint to restore pad spacing."""
from pathlib import Path
import re,uuid,math
p=Path(__file__).resolve().parents[1]/'hardware/kicad/voicememory/voicememory.kicad_pcb'
s=p.read_text()
def balanced(t,a):
 d=0;ins=False;esc=False
 for i in range(a,len(t)):
  c=t[i]
  if ins:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':ins=False
  elif c=='"':ins=True
  elif c=='(':d+=1
  elif c==')':
   d-=1
   if d==0:return i+1
 raise ValueError(a)
bridges=[]
for ref,dx in [('R2',0.75),('R3',-0.75)]:
 find=re.search(r'\(property "Reference" "'+ref+r'"',s);assert find
 a=s.rfind('\n\t(footprint',0,find.start())+2;b=balanced(s,a)
 blob=s[a:b]
 m=re.search(r'\n\t\t\(at ([-\d.]+) ([-\d.]+)( [-\d.]+)?\)',blob)
 assert m
 x,y=float(m.group(1)),float(m.group(2));ang=float((m.group(3) or '0').strip())
 newx=round(x+dx,6)
 blob=blob[:m.start(1)]+str(newx)+blob[m.end(1):]
 s=s[:a]+blob+s[b:]
 for k,pad in enumerate(re.finditer(r'\n\t\t\(pad "([12])" smd roundrect\s*\(at ([-\d.]+) ([-\d.]+)',blob)):
  n=pad.group(1);lx,ly=float(pad.group(2)),float(pad.group(3));a0=math.radians(ang)
  oldx=x+lx*math.cos(a0)-ly*math.sin(a0)
  oldy=y-lx*math.sin(a0)+ly*math.cos(a0)
  net={'R2':{'1':'FLASH_WP_N','2':'+3V3'},'R3':{'1':'FLASH_HOLD_N','2':'+3V3'}}[ref][n]
  uid=uuid.uuid5(uuid.NAMESPACE_URL, f'VoiceMemory-R{ref}-flash-clearance-{n}')
  bridges.append(f'\n\t(segment\n\t\t(start {oldx:.6f} {oldy:.6f})\n\t\t(end {oldx+dx:.6f} {oldy:.6f})\n\t\t(width 0.2)\n\t\t(layer "F.Cu")\n\t\t(net "{net}")\n\t\t(uuid "{uid}")\n\t)')
 assert len(bridges)==2 if ref=='R2' else len(bridges)==4
ix=s.index('\n\t(segment');s=s[:ix]+''.join(bridges)+s[ix:]
p.write_text(s.replace('\n','\r\n'))
print('moved R2 x+0.75, R3 x-0.75, added four 0.2mm copper bridges')
