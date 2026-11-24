import re,math,csv,json
from pathlib import Path
from shapely.geometry import box
from collections import Counter,defaultdict
root=Path(__file__).parent
s=(root/'VoiceMemory_TDisplay.kicad_sch').read_text();pcb=(root/'VoiceMemory_TDisplay.kicad_pcb').read_text()
def bx(text, i):
 d=0;q=False;e=False
 for j in range(i,len(text)):
  c=text[j]
  if q:
   if e:e=False
   elif c=='\\':e=True
   elif c=='"':q=False
  elif c=='"':q=True
  elif c=='(':d+=1
  elif c==')':
   d-=1
   if d==0:return text[i:j+1]
 raise ValueError('S-expression unbalanced')
assert bx(s,0).strip()==s.strip()
assert bx(pcb,0).strip()==pcb.strip()
fp={}
for m in re.finditer(r'\(footprint "([^"]+)"\s*\(layer "F.Cu"\)',pcb):
 b=bx(pcb,m.start());rm=re.search(r'\(property "Reference" "([^"]+)"',b)
 if not rm:continue
 ref=rm.group(1)
 if ref in fp:raise ValueError('dupe footprint '+ref)
 pos=re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)',b)
 x,y,angle=float(pos.group(1)),float(pos.group(2)),float(pos.group(3) or 0)
 # Read only fab courtyard for mounted dimensions.
 pts=[]
 for q in re.finditer(r'\((fp_line|fp_rect|fp_poly|fp_circle)\s',b):
  ob=bx(b,q.start())
  if '(layer "F.CrtYd")' not in ob:continue
  for p in re.finditer(r'\((start|end|xy|center) ([-\d.]+) ([-\d.]+)\)',ob):
   a=math.radians(angle);u,v=float(p[2]),float(p[3]);pts.append((x+u*math.cos(a)+v*math.sin(a),y-u*math.sin(a)+v*math.cos(a)))
 if not pts:
  print('NO_COURTYARD',ref)
  r=(x-1,y-1,x+1,y+1)
 else:r=(min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts))
 nets=[]
 for pm in re.finditer(r'\(pad "([^"]+)"',b):
  padblk=bx(b,pm.start());netm=re.search(r'\(net "([^"]+)"\)',padblk)
  if netm:nets.append((pm.group(1),netm.group(1)))
 fp[ref]={'box':r,'position':(x,y,angle),'nets':nets,'full':b}
assert len(fp)==53,len(fp)
board=[56.5,51.8,160.8,116.2]
for ref in fp:
 a,b,c,d=fp[ref]['box']
 if a<board[0]-0.1 or b<board[1]-0.1 or c>board[2]+0.1 or d>board[3]+0.1: print('OUTSIDE',ref,a,b,c,d)
conflicts=[]
for r1 in fp:
 if r1=='MOD1':continue
 for r2 in fp:
  if r2<=r1 or r2=='MOD1':continue
  a=box(*fp[r1]['box']);b=box(*fp[r2]['box']);area=a.intersection(b).area
  if area>1.e-5:conflicts.append((r1,r2,round(area,2)))
print('Courtyard conflicts (excluding module over SMD)',conflicts[:20],len(conflicts))
print('Switch bboxes',[(x,fp[x]['box'],fp[x]['nets']) for x in ['SW1','SW2','SW3','SW4','SW5']])
print('New pullups',[(x,fp[x]['position'],fp[x]['nets']) for x in ['R23','R24','R25','R26']])
print('MOD1 bbox',fp['MOD1']['box'])
assert not conflicts,conflicts
for id,net in [('SW1','SW_REC_N'),('SW2','SW_CH1_N'),('SW3','SW_CH2_N'),('SW4','SW_CH3_N'),('SW5','SW_CH4_N')]:
 pairs=fp[id]['nets']
 assert Counter(pairs)==Counter([('1',net),('1',net),('2','GND_AUD'),('2','GND_AUD')]),(id,pairs)
for r,net in [('R23','SW_CH1_N'),('R24','SW_CH2_N'),('R25','SW_CH3_N'),('R26','SW_CH4_N')]:
 pairs=fp[r]['nets'];assert len(pairs)==2 and {n for p,n in pairs}=={net,'+3V3'},(r,pairs)
labels=defaultdict(list)
for m in re.finditer(r'\(global_label "([^"]+)" \(shape passive\) \(at ([-\d.]+) ([-\d.]+) (\d+)\)',s):
 name,x,y,a=m.groups();labels[name].append((float(x),float(y),int(a)))
for ch in range(1,5):
 net=f'SW_CH{ch}_N';assert len(labels[net])==3,(net,labels[net]);
 for x,y,a in labels[net]:assert abs(x/1.27-round(x/1.27))<1e-6 and abs(y/1.27-round(y/1.27))<1e-6,(net,x,y)
print('CH net labels',[(net,len(labels[net])) for net in labels if net.startswith('SW_CH')]);
assert not any(x in s for x in ['(no_connect (at 101.6 223.52)','(no_connect (at 101.6 226.06)','(no_connect (at 101.6 228.6)','(no_connect (at 50.8 236.22)'])
print('PASS 53 footprints 5 switches 4 pull-ups labels pins courtyards, module-relative overlap remains unmeasured in Z')
