"""Original vector diagrams; geometry remains editable and crisp at any scale."""
from pathlib import Path
import html
OUT=Path('diagrams');OUT.mkdir(exist_ok=True)
BG='#10131d';INK='#e7e0d0';MUTED='#a9acb2';GOLD='#dcb976';GREEN='#54c991';PURPLE='#b986ea';RED='#f2827b'
def text(x,y,s,size=24,fill=INK,anchor='middle',weight=400):return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{fill}" font-weight="{weight}">{html.escape(s)}</text>'
def circle(x,y,r,fill,stroke='none',sw=1):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def boss(x,y,r=58,front='up'):
 dy=-1 if front=='up' else 1
 facing=(f'<path d="M{x-10} {y+dy*(r-2)} L{x} {y+dy*(r+16)} L{x+10} {y+dy*(r-2)}" fill="{GOLD}" stroke="{GOLD}" stroke-width="2" stroke-linejoin="round"/>' if front else '')
 return circle(x,y,r,'#69707b55','#969ca8',2)+facing+text(x,y+8,'Vloxx',25)

def dot(x,y,label='',fix=False,target=False):
 s=circle(x,y,9,INK,GREEN if target or fix else BG,2.5 if target or fix else 2)
 if label:s+=text(x,y+34,label,20,MUTED)
 if fix:s+=f'<path d="M{x} {y-40} l13 17 -13 17 -13 -17Z" fill="{PURPLE}"/>'
 return s
def green(x,y,r=100):return circle(x,y,r,'#54c99113',GREEN,2.5)
def lead(points,color=GOLD):return '<polyline points="'+points+'" fill="none" stroke="'+color+'" stroke-width="2"/>'
def simple_group(x,y,role,n,fix=False,r=100,compact=False):
 s=green(x,y,r)+text(x,y-(65 if fix else 35),role,25,GREEN)
 offsets=([(0,0),(-24,10),(24,10),(0,-22)] if fix else [(0,0),(-24,-18),(24,-18),(0,22)])[:n] if compact else [(0,0),(-26,28),(26,28),(0,56)][:n]
 for i,(dx,dy) in enumerate(offsets):s+=dot(x+dx,y+dy,fix=fix and i==0,target=i==0)
 return s
def draw(phase,mode):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 760" role="img" aria-labelledby="title desc"><title id="title">P{phase} green placement — {mode}</title><desc id="desc">Green circles, player dots and a purple fixate diamond. Each dot belongs to one green. Labels explain the assigned formation.</desc><rect width="720" height="760" rx="12" fill="{BG}"/><g font-family="Segoe UI,Arial,sans-serif">'
 title=['Staff · split around Vloxx','Spear · stay in one wedge','Sword · fixate front, groups behind','Final Form · compact triangle' if mode=='CM' else 'Final Form · resolve, then move'][phase-1]
 s+=text(32,42,f'P{phase} / {mode}',18,GOLD,'start',600)+text(32,82,title,28,INK,'start',500)
 if phase==1:
  s+=boss(360,210,60,'down')+simple_group(210,280,'Melee',4,compact=True)+simple_group(510,280,'Ranged',3,compact=True)+simple_group(360,470,'Healers + F',3,True,compact=True)
  s+=text(360,620,'The faster non-fixate holder takes the right green.',21,MUTED)
 elif phase==2:
  s+=f'<path d="M360 160 L100 580 M360 160 L660 580" fill="none" stroke="{RED}" stroke-width="5"/>'
  s+=boss(360,175,56,'down')+simple_group(360,355,'Melee',4,r=80,compact=True)+simple_group(280,550,'Healers + F',3,True,r=88,compact=True)+simple_group(440,550,'Ranged',3,r=88,compact=True)
  s+=text(360,652,'Keep all three circles between the red lanes.',21,MUTED)
 elif phase==3:
  # World coordinates: fixate (0,-40); rear holders (+/-180,450).
  # Scale .5. 240-radius greens; fixate green is disjoint from both rear greens.
  s+='<g transform="translate(0,25)">'
  s+=boss(360,220,75,'up')
  s+=green(360,200,120)+green(270,445,120)+green(450,445,120)
  s+=dot(360,200,fix=True)+dot(347.5,265)+dot(372.5,265)
  for x,y in [(270,445),(310,382),(300,410),(288,390)]:s+=dot(x,y,target=(x,y) in [(270,445),(450,445)])
  for x,y in [(450,445),(410,382),(420,410)]:s+=dot(x,y,target=(x,y) in [(270,445),(450,445)])
  s+=text(502,163,'Fixate',23,PURPLE)+lead('462,166 382,190',PURPLE)+text(180,255,'Healers',23,GREEN)+lead('235,250 310,265')
  s+=text(255,610,'Melee',25,GREEN)+text(465,610,'Ranged',25,GREEN)
  s+=text(360,651,'Rear greens back up. Soakers stay near the centre line.',21,MUTED)+'</g>'
 elif mode=='CM':
  scale=.64;ox,oy=360,400;pt=lambda x,y:(ox+x*scale,oy+y*scale)
  s+=boss(360,148,55,'up')
  centers=[(0,-190),(-165,95),(165,95)]
  for p in centers:s+=green(*pt(*p),240*scale)
  s+=circle(ox,oy,240*scale,'#b986ea0a',PURPLE,3)
  for x,y in [(0,-190),(-25,-210),(25,-210),(0,-225)]:s+=dot(*pt(x,y),target=(x,y) in [(0,-190),(165,95)])
  for i,(x,y) in enumerate([(-165,95),(-170,130),(-150,145)]):s+=dot(*pt(x,y),fix=i==0)
  for x,y in [(165,95),(170,130),(150,145)]:s+=dot(*pt(x,y),target=(x,y) in [(0,-190),(165,95)])
  s+=text(360,237,'Melee',25,GREEN)+text(160,577,'Healers + F',25,GREEN)+text(552,577,'Ranged',25,GREEN)
  s+=text(565,339,'Cloud',22,PURPLE)+lead('548,348 501,374',PURPLE)
  s+=text(360,644,'Overlap circle edges. Keep players in one green only.',21,MUTED)
 else:
  s+=boss(470,145,55,'up')
  # Spaced groups with a clear collective direction to the left.
  s+=simple_group(470,310,'Melee',4,r=77,compact=True)+simple_group(470,475,'Healers + F',3,True,r=77,compact=True)+simple_group(470,620,'Ranged',3,r=77,compact=True)
  s+=f'<path d="M290 460 H120 m24 -15 l-24 15 24 15" fill="none" stroke="{GOLD}" stroke-width="5"/>'
  s+=text(175,407,'Resolve greens',23,GOLD)+text(175,439,'then shift left',23,GOLD)
  s+=text(175,535,'Leave the spear',21,MUTED)+text(175,565,'circles behind.',21,MUTED)
 s+=circle(48,725,8,INK)+text(67,732,'Player',18,MUTED,'start')+f'<path d="M220 710 l10 14 -10 14 -10 -14Z" fill="{PURPLE}"/>'+text(240,732,'Fixate',18,MUTED,'start')+circle(401,725,12,'none',GREEN,2)+text(423,732,'Green circle',18,MUTED,'start')
 s+='</g></svg>'
 (OUT/f'p{phase}-{mode.lower()}.svg').write_text(s,encoding='utf8')
for mode in ('CM','LCM'):
 for p in range(1,5):draw(p,mode)
print('Wrote 8 original vector placement diagrams.')
