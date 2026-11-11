from pathlib import Path
import re,uuid
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
old=[((84.398,44.1722),(84.398,46.2)),((84.398,46.2),(109.036,46.2)),((109.036,46.2),(109.036,45.6922))]
removed=0
for m in list(re.finditer(r'^\t\(segment\s',s,re.M))[::-1]:
 a=m.start()+1;end=balanced(s,a);b=s[a:end]
 if '(net "MIC_DC_PASS")' not in b:continue
 aa=re.search(r'\(start ([^)]+)\)',b);bb=re.search(r'\(end ([^)]+)\)',b)
 if not aa or not bb:continue
 a1=tuple(map(float,aa.group(1).split()[:2]));b1=tuple(map(float,bb.group(1).split()[:2]))
 if any((a1,b1)==pair or (b1,a1)==pair for pair in old):
  s=s[:m.start()]+s[end:];removed+=1
assert removed==3,removed
new=[('B.Cu',(84.398,44.1722),(85.0,41.7)),('F.Cu',(85.0,41.7),(85.0,41.1)),('F.Cu',(85.0,41.1),(109.036,41.1)),('F.Cu',(109.036,41.1),(109.036,45.6922))]
append=''
for layer,start,end in new:
 uid=uuid.uuid5(uuid.NAMESPACE_URL,f'VoiceMemory-MIC_DC-eco-{layer}-{start}-{end}')
 append+=f'\n\t(segment\n\t\t(start {start[0]} {start[1]})\n\t\t(end {end[0]} {end[1]})\n\t\t(width 0.2)\n\t\t(layer "{layer}")\n\t\t(net "MIC_DC_PASS")\n\t\t(uuid "{uid}")\n\t)'
uid=uuid.uuid5(uuid.NAMESPACE_URL,'VoiceMemory-MIC_DC-eco-via-85x41.7')
append+=f'\n\t(via\n\t\t(at 85.0 41.7)\n\t\t(size 0.6)\n\t\t(drill 0.3)\n\t\t(layers "F.Cu" "B.Cu")\n\t\t(net "MIC_DC_PASS")\n\t\t(uuid "{uid}")\n\t)'
ix=s.index('\n\t(segment');s=s[:ix]+append+s[ix:]
p.write_text(s.replace('\n','\r\n'))
print('Replaced MIC_DC_PASS THT pad crossing with 1 via, 4 routed segments')
