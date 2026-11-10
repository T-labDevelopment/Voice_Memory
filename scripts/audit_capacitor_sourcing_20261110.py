#!/usr/bin/env python3
"""Independent limited audit of capacitor sourcing PCB ECO; not KiCad ERC or DRC."""
from pathlib import Path
import subprocess,re,json,math,hashlib
from shapely.geometry import LineString,box,Point
from shapely.affinity import rotate,translate
ROOT=Path(__file__).resolve().parents[1]; rel='hardware/kicad/voicememory/'
REFS={'C2','C4','C7','C8','C10','C14','C15','C16','C17'}

def bal(s,start):
 d=0;q=False;esc=False
 for i in range(start,len(s)):
  ch=s[i]
  if q:
   if esc:esc=False
   elif ch=='\\':esc=True
   elif ch=='"':q=False
  elif ch=='"':q=True
  elif ch=='(':d+=1
  elif ch==')':
   d-=1
   if d==0:return i+1
 raise ValueError('Unbalanced sexpr')
def children(s,tag,indent='\t'):
 return [(m.start()+len(indent),bal(s,m.start()+len(indent))) for m in re.finditer(r'^'+re.escape(indent)+r'\('+tag+r'\s',s,re.M)]
def val(s,key):
 m=re.search(r'\('+re.escape(key)+r'\s+([^)]*)\)',s)
 return m[1] if m else None
def prop(s,name):
 m=re.search(r'\(property "'+re.escape(name)+r'" "([^"]+)"',s)
 return m[1] if m else None

def pads(b):
 out={}
 for a,z in children(b,'pad','\t\t'):
  p=b[a:z];m=re.match(r'\(pad "(\d+)"',p)
  if not m: continue
  out[m[1]]={'net':val(p,'net'), 'uuid':val(p,'uuid'),'at':val(p,'at'), 'size':val(p,'size')}
 return out

def fps(s):
 fs={}
 for a,z in children(s,'footprint'):
  b=s[a:z];r=prop(b,'Reference')
  if r:fs[r]={'value':prop(b,'Value'),'type':b.splitlines()[0].split('"')[1],
             'at':val(b,'at'),'uuid':val(b,'uuid'),'pads':pads(b),'raw':b}
 return fs

def wireblocks(s,tag):return [s[a:z] for a,z in children(s,tag)]
def netname(pb):
 m=re.search(r'\(net "([^"]+)"\)',pb)
 return m[1] if m else None

def padpoly(f,p):
 coords=list(map(float,p['at'].split())); size=list(map(float,p['size'].split())); xy=list(map(float,f['at'].split()));
 a=xy[2] if len(xy)>2 else 0
 poly=box(coords[0]-size[0]/2,coords[1]-size[1]/2,coords[0]+size[0]/2,coords[1]+size[1]/2)
 return translate(rotate(poly,a,origin=(0,0)),xy[0],xy[1])

before=subprocess.check_output(['git','-C',str(ROOT),'show','a0d957f:'+rel+'voicememory.kicad_pcb']).decode().replace('\r\n','\n')
after=(ROOT/(rel+'voicememory.kicad_pcb')).read_text()
bs=fps(before);cur=fps(after)
assert bs.keys()==cur.keys(),(set(bs)^set(cur))
assert len(bs)>=60
assert len(wireblocks(before,'segment'))==len(wireblocks(after,'segment'))
assert wireblocks(before,'segment')==wireblocks(after,'segment')
assert wireblocks(before,'via')==wireblocks(after,'via')
assert wireblocks(before,'zone')==wireblocks(after,'zone')
for ref in bs:
 if ref not in REFS:
  assert bs[ref]['raw']==cur[ref]['raw'],ref
 else:
  assert bs[ref]['uuid']==cur[ref]['uuid'] and bs[ref]['at']==cur[ref]['at'],ref
  assert bs[ref]['type']=='Capacitor_SMD:C_0805_2012Metric'
  assert cur[ref]['type']=='Capacitor_SMD:C_0603_1608Metric'
  assert sorted(bs[ref]['pads'])==sorted(cur[ref]['pads'])==['1','2']
  for n in '12':
   a=bs[ref]['pads'][n];c=cur[ref]['pads'][n]
   assert a['uuid']==c['uuid'] and a['net']==c['net']
   assert list(map(float,c['size'].split()))==[.9,.95]

# Track attachment comparison against current net copper. Ground pads may rely on unfilled zone.
segs=[];vias=[]
for b in wireblocks(after,'segment'):
 n=netname(b); layer=val(b,'layer');w=float(val(b,'width'));aa=list(map(float,val(b,'start').split()));zz=list(map(float,val(b,'end').split()))
 if layer=='"F.Cu"':segs.append((n,LineString([aa,zz]).buffer(w/2)))
for b in wireblocks(after,'via'):
 n=netname(b); a=list(map(float,val(b,'at').split()));d=float(val(b,'size'))
 vias.append((n,Point(a).buffer(d/2)))
check=[];new_short=[]
for ref in sorted(REFS,key=lambda x:int(x[1:])):
 for n in '12':
  p=cur[ref]['pads'][n];net=p['net'].strip('\"') if p['net'] else None
  old=padpoly(bs[ref],bs[ref]['pads'][n]);new=padpoly(cur[ref],p)
  old_match=sum(1 for k,g in segs if k==net and g.intersects(old))+sum(1 for k,g in vias if k==net and g.intersects(old))
  new_match=sum(1 for k,g in segs if k==net and g.intersects(new))+sum(1 for k,g in vias if k==net and g.intersects(new))
  old_cross=sum(1 for k,g in segs if k!=net and g.intersects(old))+sum(1 for k,g in vias if k!=net and g.intersects(old))
  new_cross=sum(1 for k,g in segs if k!=net and g.intersects(new))+sum(1 for k,g in vias if k!=net and g.intersects(new))
  assert not(old_match>0 and new_match==0),('lost contact',ref,n)
  if new_cross>old_cross:new_short.append({'ref':ref,'pin':n,'old':old_cross,'new':new_cross})
  check.append({'ref':ref,'pad':n,'net':net,'old_direct':old_match,'new_direct':new_match,'old_other_copper_intersections':old_cross,'new_other_copper_intersections':new_cross})
assert not new_short,new_short
# Count footprint and schematic component references
sch=(ROOT/(rel+'voicememory.kicad_sch')).read_text()
for ref in REFS:
 units=[]
 for a,z in children(sch,'symbol'):
  unit=sch[a:z]
  if prop(unit,'Reference')==ref:units.append(unit)
 assert len(units)==1,ref
 assert '(property "Footprint" "Capacitor_SMD:C_0603_1608Metric"' in units[0],ref
 assert prop(units[0],'Value')==cur[ref]['value'],ref
r={'base_commit':'a0d957f3e961b686945c244d7daa850e124963c5','changed_references':sorted(REFS),
   'changed_count':len(REFS),'unchanged_footprints':len(bs)-len(REFS),'unchanged_segments':len(wireblocks(before,'segment')),
   'unchanged_vias':len(wireblocks(before,'via')),'pad_net_uuid_and_board_origin_preserved':True,
   'existing_direct_trace_connections_retained':True,
   'no_new_other_net_intersections_with_segments_and_vias':True,
   'pads_with_no_preexisting_direct_FCu_contact':[f'{x["ref"]}-{x["pad"]}' for x in check if x['old_direct']==0],
   'notes':['Static intersection check is not KiCad 10 official DRC',
            'No zone refill was performed and direct-F.Cu contact counts do not include filled zones or pad-pad contacts',
            'Potential F.SilkS text collisions and full copper clearances remain unverified'],
   'pad_checks':check}
out=ROOT/'hardware/reports/CAP_SOURCING_STATIC_AUDIT_2026-11-10.json'
out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='pad_checks'},ensure_ascii=False,indent=2))
