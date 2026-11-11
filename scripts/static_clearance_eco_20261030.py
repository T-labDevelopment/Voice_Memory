#!/usr/bin/env python3
"""Conservative geometric-only clearance audit, not KiCad DRC nor manufacturing approval."""
import re,math,importlib.util,json
from shapely.geometry import Point,LineString,box
from shapely.affinity import rotate,translate
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('static',root/'scripts/validate_v1_static_20261030.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
pads=[]
for ref,block in v.footprints.items():
 at=v.pos(block)
 if len(at)<2:continue
 x,y=at[:2];ang=at[2] if len(at)>2 else 0
 for p in v.sub(block,'pad'):
  match=re.search(r'^\(pad "([^"]*)" (smd|thru_hole|np_thru_hole) (\w+)',p)
  if not match:continue
  pn,kind,shape=match.groups(); net=v.padnet(p)
  l=v.pos(p)
  if len(l)<2:continue
  dx,dy=l[:2]
  size=v.val(p,r'\(size ([^)]+)\)')
  if not size:continue
  sw,sh=map(float,size.split()[:2]); a=ang
  # KiCad pad local coordinates in footprint convention: on board local axes rotated with the footprint and reflected Y down.
  cx=x+dx*math.cos(math.radians(a))-dy*math.sin(math.radians(a))
  cy=y-dx*math.sin(math.radians(a))+dy*math.cos(math.radians(a))
  if shape=='circle':poly=Point(cx,cy).buffer(sw/2,resolution=24)
  else:
   poly=box(cx-sw/2,cy-sh/2,cx+sw/2,cy+sh/2)
   poly=rotate(poly,a,origin=(cx,cy),use_radians=False)
  pads.append(dict(ref=ref,pn=pn,kind=kind,net=net,poly=poly,xy=(cx,cy)))

# target-specific proximity: U2 pad to other-net pads/segments/vias, C11/19 to same, RJ45 NPTH to all copper.
report={}
for ref in ('U2','C11','C19'):
 matches=[]
 for p in pads:
  if p['ref']!=ref or not p['pn']:continue
  near=[]
  for q in pads:
   if q['ref']==ref or not q['net'] or q['net']==p['net'] or q['kind']=='np_thru_hole':continue
   d=p['poly'].distance(q['poly']);
   if d<1.2:near.append((round(d,3),q['ref']+':'+q['pn']+':'+str(q['net'])))
  for s in v.seg:
   if s['net']==p['net'] or s['layer']!='F.Cu':continue
   d=p['poly'].distance(LineString([s['a'],s['b']]).buffer(s['w']/2));
   if d<0.4:near.append((round(d,3),'track:'+str(s['net'])+':'+str(s['a'])+':'+str(s['b'])))
  matches.append({'pin':p['pn'],'net':p['net'],'nearest_different_net':sorted(near)[:8]})
 report[ref]=matches
for ref in ('J1','J2'):
 report[ref]=[]
 for hole in [h for h in v.news if h['ref']==ref]:
  disk=Point(*hole['xy']).buffer(1.6,resolution=24)
  conflict=[]
  for q in pads:
   if not q['net']:continue
   d=disk.distance(q['poly'])
   if d<.4:conflict.append((round(d,3),'pad:'+q['ref']+':'+q['pn']))
  for s in v.seg:
   d=disk.distance(LineString([s['a'],s['b']]).buffer(s['w']/2))
   if d<.4:conflict.append((round(d,3),'trace:'+str(s['net'])))
  for q in v.via:
   d=disk.distance(Point(*q['xy']).buffer(q['r']))
   if d<.4:conflict.append((round(d,3),'via:'+str(q['net'])))
  report[ref].append({'hole':[round(k,4) for k in hole['xy']],'below_0p4mm_clearance':sorted(conflict)[:20]})
print(json.dumps(report,ensure_ascii=False,indent=2))
(root/'hardware/reports/ECO_PROXIMITY_2026-10-30.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
