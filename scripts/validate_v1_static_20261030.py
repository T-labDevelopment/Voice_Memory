#!/usr/bin/env python3
"""Static (NOT KiCad DRC) PCB ECO check, for reporting geometry and pin-net consistency."""
import math,re,json
from pathlib import Path
from collections import Counter
D=Path(__file__).resolve().parents[1]/'hardware/kicad/voicememory'; T=D/'voicememory.kicad_pcb'; src=T.read_text(); sch=(D/'voicememory.kicad_sch').read_text()
def balanced(s,a):
 depth=0;ins=False;esc=False
 for i in range(a,len(s)):
  c=s[i]
  if ins:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':ins=False
  elif c=='"':ins=True
  elif c=='(':depth+=1
  elif c==')':
   depth-=1
   if depth==0:return i+1
 raise ValueError(a)
def top(s,tag):
 for m in re.finditer(r'^\t\('+tag+r'(?:\n|\s)',s,re.M):
  a=m.start()+1;yield s[a:balanced(s,a)]
def sub(s,tag):
 for m in re.finditer(r'^\t\t\('+tag+r'(?:\n|\s)',s,re.M):
  a=m.start()+2; yield s[a:balanced(s,a)]
def val(s,pattern):
 x=re.search(pattern,s);return x.group(1) if x else None
def fp_ref(x):return val(x,r'\(property "Reference" "([^"]+)"')
def pos(x):
 a=val(x,r'\(at ([^)]+)\)');return tuple(float(k) for k in a.split()) if a else ()
def padnet(x):return val(x,r'\(net "([^"]+)"')
def distseg(p,a,b):
 v=(b[0]-a[0],b[1]-a[1]);dd=v[0]**2+v[1]**2
 t=0 if dd<1e-20 else max(0,min(1,((p[0]-a[0])*v[0]+(p[1]-a[1])*v[1])/dd))
 return math.hypot(p[0]-a[0]-t*v[0],p[1]-a[1]-t*v[1])
footprints={fp_ref(x):x for x in top(src,'footprint') if fp_ref(x)}
assert len(footprints)>=60,len(footprints)
assert all(x in footprints for x in ('J1','J2','C11','C19','U2','U3'))
assert len(list(top(src,'segment')))>436
assert sch.count('Voice_Memory:TLP592A')>=1
assert sch.count('Voice_Memory:W25Q32RVCSJM')>=1
expected_holes={}; news=[]
for ref in ('J1','J2'):
 block=footprints[ref]; x,y,rot=pos(block)
 pads=list(sub(block,'pad'))
 for p in pads:
  if not p.startswith('(pad "" np_thru_hole'):continue
  u,v,_=pos(p);a=math.radians(rot)
  xy=(x+u*math.cos(a)-v*math.sin(a),y+u*math.sin(a)+v*math.cos(a))
  news.append({'ref':ref,'xy':xy,'drill_mm':3.2})
 assert len([p for p in pads if p.startswith('(pad "" np_thru_hole')])==2
 assert len([p for p in pads if re.match(r'\(pad "\d',p)])==8
 for p in pads:
  if re.match(r'\(pad "\d',p):assert padnet(p)
for ref in ('C11','C19'):
 block=footprints[ref]
 assert 'Capacitor_SMD:C_0603_1608Metric' in block
 pads=list(sub(block,'pad'));assert len(pads)==2
 for p in pads:assert '(size 0.9 0.95)' in p and '.775' in p
for ref in ('U2',):
 block=footprints[ref]
 assert 'Package_SO:SOP-8_5.28x5.23mm_P1.27mm' in block
 pads=list(sub(block,'pad'))
 assert len(pads)==8
 for p in pads:assert '3.6' in p and '(size 1.6 0.6)' in p
assert 'TLP592A(F)' in footprints['U3']
seg=[]
for block in top(src,'segment'):
 a=val(block,r'\(start ([^)]+)\)');b=val(block,r'\(end ([^)]+)\)');w=val(block,r'\(width ([^)]+)\)');layer=val(block,r'\(layer "([^"]+)"');net=padnet(block)
 if a and b:seg.append({'a':tuple(map(float,a.split()[:2])),'b':tuple(map(float,b.split()[:2])),'w':float(w),'layer':layer,'net':net})
via=[]
for block in top(src,'via'):
 a=val(block,r'\(at ([^)]+)\)');size=val(block,r'\(size ([^)]+)\)')
 if a and size:via.append({'xy':tuple(map(float,a.split()[:2])),'r':float(size)/2,'net':padnet(block)})
checks=[]
for hole in news:
 p=hole['xy']
 close_seg=sorted([(distseg(p,z['a'],z['b'])-(1.6+z['w']/2),z['net'],z['layer']) for z in seg],key=lambda x:x[0])[:4]
 close_via=sorted([(math.hypot(p[0]-z['xy'][0],p[1]-z['xy'][1])-1.6-z['r'],z['net']) for z in via],key=lambda x:x[0])[:4]
 checks.append({'ref':hole['ref'],'hole_xy':list(map(lambda a:round(a,4),p)), 'closest_copper_trace_edge_mm':round(close_seg[0][0],3),'closest_copper_trace_net':close_seg[0][1], 'closest_via_edge_mm':round(close_via[0][0],3),'closest_via_net':close_via[0][1]})
print('static_checks=',json.dumps({'footprints':len(footprints),'segments':len(seg),'vias':len(via),'new_hole_clearance':checks},ensure_ascii=False,indent=2))
(Path(__file__).resolve().parents[1]/'hardware/reports/ECO_STATIC_CHECK_2026-10-30.json').write_text(json.dumps({'footprints':len(footprints),'segments':len(seg),'vias':len(via),'new_hole_clearance':checks},ensure_ascii=False,indent=2)+'\n')
