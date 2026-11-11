#!/usr/bin/env python3
"""Generate a 300dpi equivalent technical preview without requiring KiCad GUI."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
ROOT=Path(__file__).resolve().parent
W,H=2650,1900
im=Image.new('RGB',(W,H),'#ffffff')
d=ImageDraw.Draw(im)
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
try:
    ftitle=ImageFont.truetype(fontpath,58)
    fsub=ImageFont.truetype(fontpath,35)
    flabel=ImageFont.truetype(fontpath,28)
    fpins=ImageFont.truetype(fontpath,26)
except OSError:
    ftitle=fsub=flabel=fpins=ImageFont.load_default()
S=80; XO=790; YO=760
def tr(x,y):return (round(XO+x*S),round(YO+y*S))
def circle(x,y,r,fill,outline=None,width=1):
    X,Y=tr(x,y); rr=round(r*S)
    d.ellipse((X-rr,Y-rr,X+rr,Y+rr),fill=fill,outline=outline,width=width)
def line_mm(coords,fill,width=4): d.line([tr(*p) for p in coords],fill=fill,width=width)
# technical grid
for x in range(-6,15):
    X,_=tr(x,0)
    d.line([(X,130),(X,1500)],fill='#e8eef4',width=1)
for y in range(-7,11):
    _,Y=tr(0,y)
    d.line([(220,Y),(1900,Y)],fill='#e8eef4',width=1)
# Envelope drawing
bl,br,bk,fr=-4.385,11.525,-5.68,9.42
xy1=tr(bl,bk); xy2=tr(br,fr)
d.rectangle([xy1,xy2],fill='#eef6f6',outline='#235c5c',width=6)
# opening
line_mm([(bl,fr),(br,fr)],'#168a8a',10)
# mounting holes
for x in [-2.78,9.92]:
    circle(x,4.32,1.6,'#ffffff','#c43b55',9)
    X,Y=tr(x,4.32)
    d.line([(X-30,Y),(X+30,Y)],fill='#c43b55',width=3)
    d.line([(X,Y-30),(X,Y+30)],fill='#c43b55',width=3)
# copper rings and drilled pins
for n in range(1,9):
    x=(n-1)*1.02; y=0 if n%2 else 1.78
    circle(x,y,.75,'#c38e2a','#916720',4)
    circle(x,y,.45,'#fffdf8','#ffffff',1)
    X,Y=tr(x,y)
    d.text((X,Y),str(n),font=fpins,anchor='mm',fill='#273c55',stroke_width=1,stroke_fill='#ffffff')
# x spacing dims mount
xmin,_=tr(-2.78,0); xmax,_=tr(9.92,0)
y_dim=round(tr(0,7.0)[1])
d.line([(xmin,y_dim),(xmax,y_dim)],fill='#c43b55',width=4)
for xx in [xmin,xmax]:d.line([(xx,y_dim-18),(xx,y_dim+18)],fill='#c43b55',width=4)
d.text(((xmin+xmax)/2,y_dim+32),'12.70 mm mounting-hole spacing',font=flabel,anchor='mt',fill='#a72648')
# headers
d.text((110,50),'RJ45 8P8C - CORRECTED FOOTPRINT',font=ftitle,fill='#17293a')
d.text((110,125),'Component-side PCB layout  |  Datum: pin 1 = (0, 0) mm',font=fsub,fill='#34516d')
# callouts right
x0=1840
d.text((x0,350),'Body outline',font=fsub,fill='#235c5c')
d.text((x0,401),'15.91 x 15.10 mm',font=flabel,fill='#34516d')
d.text((x0,560),'8 signal pins',font=fsub,fill='#9a6a17')
d.text((x0,609),'drill 0.90 mm',font=flabel,fill='#34516d')
d.text((x0,660),'stagger 1.02 / 1.78 mm',font=flabel,fill='#34516d')
d.text((x0,820),'2 plastic locating posts',font=fsub,fill='#b6324a')
d.text((x0,869),'NPTH drill 3.20 mm',font=flabel,fill='#34516d')
d.text((x0,920),'Y = +4.32 mm',font=flabel,fill='#34516d')
d.text((x0,1080),'Front / jack opening',font=fsub,fill='#168a8a')
d.text((x0,1133),'toward +Y',font=flabel,fill='#34516d')
d.text((110,1650),'Important: pin numbers 1-8 are retained; mount holes have no copper / no net.',font=fsub,fill='#17293a')
d.text((110,1710),'Dimensions based on supplied mechanical drawing. ERC / DRC / physical-fit NOT tested.',font=flabel,fill='#a02f45')
out=ROOT/'RJ45_8P8C_Corrected_Layout_20261025.png'
im.save(out,optimize=True)
print('CREATED',out)
