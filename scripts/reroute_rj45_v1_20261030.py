#!/usr/bin/env python3
"""Reroute old MIC/PTT tracks displaced by relocating RJ45 NPTH holes.
These are proposed tracks, NOT a replacement for KiCad DRC/zone refill.
"""
from pathlib import Path
import re,uuid
PCB=Path(__file__).resolve().parents[1]/'hardware/kicad/voicememory/voicememory.kicad_pcb'
s=PCB.read_text()
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

def segkey(b):
 match=lambda pat:re.search(pat,b).group(1)
 start=tuple(map(float,match(r'\(start ([^)]+)\)').split()))
 end=tuple(map(float,match(r'\(end ([^)]+)\)').split()))
 return (match(r'\(layer "([^"]+)"\)'),match(r'\(net "([^"]+)"\)'),start,end)
originals=[
('F.Cu','PTT_GND',(110.996,43.5722),(84.149471,43.5722)),
('F.Cu','PTT_GND',(81.086,43.6642),(73.476,43.6642)),
('B.Cu','MIC_DOWN',(80.08,42.6482),(108.032,42.6482)),
('B.Cu','MIC_DOWN',(108.032,42.6482),(111.076,45.6922)),
('F.Cu','MIC_DC_PASS',(84.398,44.1722),(107.516,44.1722)),
('F.Cu','MIC_DC_PASS',(107.516,44.1722),(109.036,45.6922))]
count=[]
for m in list(re.finditer(r'^\t\(segment\s',s,re.M))[::-1]:
 a=m.start()+1;end=balanced(s,a)
 b=s[a:end];k=segkey(b)
 if any(k[0]==t[0] and k[1]==t[1] and ((k[2],k[3])==(t[2],t[3]) or (k[3],k[2])==(t[2],t[3])) for t in originals):
  count.append(k);s=s[:m.start()]+s[end:]
assert len(count)==len(originals),(len(count),count)
paths=[
('F.Cu','PTT_GND',[(110.996,43.5722),(110.996,40.55),(84.149471,40.55),(84.149471,43.5722)]),
('F.Cu','PTT_GND',[(81.086,43.6642),(81.086,40.55),(73.476,40.55),(73.476,43.6642)]),
('B.Cu','MIC_DOWN',[(80.08,42.6482),(80.08,40.9),(109.1,40.9),(111.076,45.6922)]),
('B.Cu','MIC_DC_PASS',[(84.398,44.1722),(84.398,46.2),(109.036,46.2),(109.036,45.6922)])]
insert=''
for layer,net,points in paths:
 for i,(p,q) in enumerate(zip(points,points[1:])):
  uid=uuid.uuid5(uuid.NAMESPACE_URL,f'VoiceMemory-20261030-RJ45-{layer}-{net}-{str(p)}-{str(q)}')
  insert+=f'\n\t(segment\n\t\t(start {p[0]} {p[1]})\n\t\t(end {q[0]} {q[1]})\n\t\t(width 0.2)\n\t\t(layer "{layer}")\n\t\t(net "{net}")\n\t\t(uuid "{uid}")\n\t)'
index=s.index('\n\t(segment')
s=s[:index]+insert+s[index:]
# Zone filling in the source was computed for OLD drill locations: deliberately remove stale cached filled zones.
# The zones remain configured for fill, but user MUST press 'B' in KiCad and save before generating Gerbers.
removed=0
while True:
 m=re.search(r'^\t\t\(filled_polygon\s',s,re.M)
 if not m:break
 a=m.start()+2;end=balanced(s,a)
 s=s[:m.start()]+s[end:];removed+=1
assert removed>0,removed
PCB.write_text(s)
print('removed original tracks',len(count),'inserted',sum(len(p)-1 for _,_,p in paths),'cleared stale filled_polygon',removed)
