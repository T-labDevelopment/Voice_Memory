#!/usr/bin/env python3
"""Targeted altered-track clearance check. No ground-zone fill or KiCad DRC."""
from pathlib import Path
import importlib.util,math,json
from shapely.geometry import Point,LineString,box
from shapely.affinity import rotate
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('v',root/'scripts/validate_v1_static_20261030.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

# read changed segment IDs from diff against original snapshot (excluding zone fill).
import re,subprocess
s=(root/'hardware/kicad/voicememory/voicememory.kicad_pcb').read_text()
orig=subprocess.check_output(['git','show','main:hardware/kicad/voicememory/voicememory.kicad_pcb'],cwd=root).decode()
orig_ids=set(re.findall(r'^\t\t\(uuid "([^"]+)"\)',orig,re.M))
changed=[]
for t in v.top(s,'segment'):
 uid=v.val(t,r'\(uuid "([^"]+)"')
 if uid not in orig_ids:
  a=v.val(t,r'\(start ([^)]+)\)');b=v.val(t,r'\(end ([^)]+)\)')
  changed.append({'a':tuple(map(float,a.split()[:2])),'b':tuple(map(float,b.split()[:2])),
     'w':float(v.val(t,r'\(width ([^)]+)\)')),'net':v.padnet(t),'layer':v.val(t,r'\(layer "([^"]+)"'),'uuid':uid})

# all pads (non npth)
pads=[]
for ref,block in v.footprints.items():
 at=v.pos(block)
 if len(at)<2:continue
 x,y=at[:2];ang=at[2] if len(at)>2 else 0
 for pad in v.sub(block,'pad'):
  m=re.search(r'^\(pad "([^"]*)" (\w+) (\w+)',pad)
  if not m or m.group(2)=='np_thru_hole':continue
  pn,kind,shape=m.groups();net=v.padnet(pad)
  coords=v.pos(pad);sz=v.val(pad,r'\(size ([^)]+)\)')
  if len(coords)<2 or not sz:continue
  dx,dy=coords[:2];cx=x+dx*math.cos(math.radians(ang))-dy*math.sin(math.radians(ang));cy=y-dx*math.sin(math.radians(ang))+dy*math.cos(math.radians(ang));w,h=map(float,sz.split()[:2])
  if shape=='circle': geom=Point(cx,cy).buffer(w/2)
  else:geom=rotate(box(cx-w/2,cy-h/2,cx+w/2,cy+h/2),ang,origin=(cx,cy))
  pads.append((net,kind,ref,pn,geom))
check=[]
for idx,sg in enumerate(changed):
 line=LineString([sg['a'],sg['b']]).buffer(sg['w']/2)
 neighbors=[]
 for pnet,kind,ref,pn,poly in pads:
  if pnet and pnet!=sg['net'] and (sg['layer']=='F.Cu' or kind=='thru_hole'):
   d=line.distance(poly)
   if d<0.30:neighbors.append((round(d,4),'pad:'+ref+':'+pn+':'+pnet))
 for t in v.seg:
  if t['layer']!=sg['layer'] or t['net']==sg['net'] or (t['a']==sg['a'] and t['b']==sg['b']):continue
  d=line.distance(LineString([t['a'],t['b']]).buffer(t['w']/2))
  if d<0.3:neighbors.append((round(d,4),'track:'+t['net']+':'+str(t['a'])+':'+str(t['b'])))
 for t in v.via:
  if t['net']==sg['net']:continue
  d=line.distance(Point(*t['xy']).buffer(t['r']))
  if d<0.3:neighbors.append((round(d,4),'via:'+t['net']+':'+str(t['xy'])))
 check.append({'net':sg['net'],'layer':sg['layer'],'a':sg['a'],'b':sg['b'],'under_0p3_mm':sorted(neighbors)[:8]})
print(json.dumps(check,ensure_ascii=False,indent=2))
(root/'hardware/reports/ECO_NEW_TRACK_CLEARANCE_2026-10-30.json').write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n')
