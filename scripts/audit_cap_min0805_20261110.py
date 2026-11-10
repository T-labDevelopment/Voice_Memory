#!/usr/bin/env python3
"""Conservative 2D screening for changed capacitor pads vs other-net pad/track/via.
This is NOT KiCad DRC; ignores copper zones, complex shapes, masking, hole clearances.
"""
import json,re,math,subprocess
from pathlib import Path
from shapely.geometry import Point,box,LineString
from shapely.affinity import rotate,translate
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'hardware/kicad/voicememory/voicememory.kicad_pcb'
BASE=subprocess.check_output(['git','show','v1-cap-sourcing-2026-11-10:hardware/kicad/voicememory/voicememory.kicad_pcb'],cwd=ROOT).decode()
UPDATED=P.read_text()
refs_changed=set([f'C{i}' for i in (2,4,7,8,10,11,14,15,16,17,19)])

def bal(s,i):
 q=esc=False;d=0
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
 raise ValueError('unbalanced')

def items(s,typ,level=1):
 prefix='\n'+'\t'*level+'('+typ
 for m in re.finditer(re.escape(prefix)+r'(?:\s|\))',s):
  a=m.start()+len(prefix)-len('('+typ)
  # actually parent starts at newline+indent, precisely:
  a=m.start()+len('\n'+'\t'*level)
  yield s[a:bal(s,a)]

def parse_fp(s):
 fps={};pads=[]
 for t in items(s,'footprint'):
  ref=re.search(r'\(property "Reference" "([^"]+)"',t)
  if ref is None:continue
  ref=ref.group(1)
  ori=re.search(r'^\(footprint "[^\n]+"\s*\(layer "[^\n]+"\)\s*\(uuid "[^\n]+"\)\s*\(at ([^ )]+) ([^ )]+)(?: ([^ )]+))?\)',t,re.S)
  if ori is None:
   ori=re.search(r'\n\t\t\(at ([^ )]+) ([^ )]+)(?: ([^ )]+))?\)',t)
  if not ori:raise ValueError((ref,'no position'))
  x,y,phi=map(float,(ori.group(1),ori.group(2),ori.group(3) or 0))
  fps[ref]=(x,y,phi)
  for p in items(t,'pad',2):
   z=re.search(r'^\(pad "([^"]+)" (smd|thru_hole|np_thru_hole) ([a-z_]+)',p)
   if not z:continue
   number,ty,shape=z.groups()
   center=re.search(r'\(at ([^ )]+) ([^ )]+)(?: ([^ )]+))?\)',p)
   size=re.search(r'\(size ([^ )]+) ([^ )]+)\)',p)
   net=re.search(r'\(net "([^"]+)"\)',p)
   if not center or not size:continue
   px,py,ang=map(float,(center.group(1),center.group(2),center.group(3) or 0))
   sx,sy=map(float,size.groups())
   rot=math.radians(phi)
   xx=x+px*math.cos(rot)-py*math.sin(rot)
   yy=y+px*math.sin(rot)+py*math.cos(rot)
   # pad local orientation already encodes the footprint orientation in these data.
   gr=rotate(box(-sx/2,-sy/2,sx/2,sy/2), ang,origin=(0,0),use_radians=False)
   sh=translate(gr,xx,yy)
   if ty=='np_thru_hole':continue
   pads.append({'ref':ref,'pad':number,'net':net.group(1) if net else None,'shape':sh,'x':xx,'y':yy,'layer':'both' if ty=='thru_hole' else 'F.Cu'})
 return fps,pads

def traces(s):
 nets={int(n):name for n,name in re.findall(r'\(net (\d+) "([^"]*)"\)',s)}
 out=[]
 for ty in ('segment','via'):
  for t in items(s,ty):
   id=re.search(r'\(net \"([^\"]+)\"\)',t)
   if not id:continue
   net=id.group(1)
   if ty=='segment':
    start=re.search(r'\(start ([^ )]+) ([^ )]+)\)',t)
    end=re.search(r'\(end ([^ )]+) ([^ )]+)\)',t)
    width=re.search(r'\(width ([^ )]+)\)',t)
    layer=re.search(r'\(layer "([^"]+)"\)',t)
    if not all([start,end,width,layer]):continue
    line=LineString([tuple(map(float,start.groups())),tuple(map(float,end.groups()))]).buffer(float(width.group(1))/2,cap_style=1)
    out.append({'id':'segment','net':net,'shape':line,'layer':layer.group(1)})
   else:
    at=re.search(r'\(at ([^ )]+) ([^ )]+)\)',t);sz=re.search(r'\(size ([^ )]+)\)',t)
    if at and sz:out.append({'id':'via','net':net,'shape':Point(*map(float,at.groups())).buffer(float(sz.group(1))/2),'layer':'both'})
 return out

def eval(s):
 fps,pads=parse_fp(s);ts=traces(s)
 issues=[];edge=[]
 for a in pads:
  if a['ref'] not in refs_changed:continue
  for b in pads:
   if a is b or b['ref']==a['ref'] or a['net']==b['net']:continue
   d=a['shape'].distance(b['shape'])
   if d<0.25:issues.append(('pad',a['ref'],a['pad'],a['net'],b['ref'],b['pad'],b['net'],round(d,3)))
  for b in ts:
   if a['net']==b['net'] or b['layer'] not in ('F.Cu','both'):continue
   if a['shape'].distance(b['shape'])<0.25:
    d=a['shape'].distance(b['shape'])
    issues.append(('trace',a['ref'],a['pad'],a['net'],b['id'],'-',b['net'],round(d,3)))
 return fps,issues
oldfps, old=eval(BASE);newfps,new=eval(UPDATED)
oldset=set(tuple(x[:-1]) for x in old); additions=[x for x in new if tuple(x[:-1]) not in oldset]
result={'old_flagged':len(old),'new_flagged':len(new),'new_closures_count':len(additions),'new_closures':additions[:150],
        'old_preview':old[:20], 'note':'Screening threshold 0.25mm; not KiCad official DRC, no zones, no rerouting'}
(ROOT/'hardware/reports/CAP_MIN_0805_STATIC_GEOM_2026-11-10.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('old_preview',)},indent=2,ensure_ascii=False)[:10000])
