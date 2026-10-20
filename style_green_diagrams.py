"""Editable WRDL formations, redrawn from the guild reference in the guide style."""
from pathlib import Path
import html,textwrap
OUT=Path(__file__).resolve().parent/'diagrams'
BG='#0a0e18';SURFACE='#101524';GOLD='#e8c976';INK='#eae6da';MUTED='#a8aaaf';GREEN='#54c991';PURPLE='#b986ea';RED='#f2827b'
W,H=720,1520
PANELS=[
 ('p1','P1 · Staff','100–70%',[
 'Fixate always gets a green. Both healers join that player; if a healer is fixated, the floater joins them to make three.',
 'Melee stand closest to Vloxx to get the other two greens. Ranged players stay farther away.',
 'If two melee players get greens, both start moving right. The player in front goes to ranged; the other stays with melee.',
 'A ranged player who gets a green stays with ranged. If melee has only two people, a ranged player without a green moves to melee.']),
 ('p2','P2 · Spear','70–40%',[
 'Keep all three greens between the red lines: melee at the front, healers back left and ranged back right.',
 'Both healers join fixate. If a healer is fixated, the floater joins them so that green has three people.',
 'If two melee players get greens, both head back right. The player in front goes to ranged; the other stays at the front with melee.',
 'A ranged player who gets a green stays back right. If melee has only two people, a ranged player without a green moves to the front.']),
 ('p3','P3 · Sword','40–10%',[
 'Fixate stands inside Vloxx’s hitbox, just in front of his centre. Both healers stand just behind his centre, inside fixate’s green.',
 'The players with the other two greens move behind Vloxx, to the left and right. Move far enough back that neither circle overlaps fixate’s green.',
 'Everyone else joins their assigned green. Stand toward the middle of the formation while staying inside only your own circle.']),
 ('p4-bunker','P4 · Bunker','CM ONLY',[
 'Use this formation in CM only. In LCM, P4 Spears cannot be blocked; use the Boneskinner formation instead.',
 'Place melee directly behind Vloxx, with healers left and ranged right. Overlap all three greens inside the purple projectile-block circle.',
 'Stand with your assigned group, inside your own green and outside any overlap with another green. Keep projectile blocks active to protect everyone from Spears.']),
 ('p4-boneskinner','P4 · Boneskinner','CM / LCM',[
 'Line up behind Vloxx: melee nearest him, healers in the middle and ranged at the back. Keep at least three people in each green.',
 'Move left together to leave the Spear circles and third-wave Puddles behind. Move with the players in your green so everyone remains inside it.'])]

def text(x,y,label,size=28,fill=INK,anchor='start',weight=400):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{html.escape(label)}</text>'
def circle(x,y,r,fill,stroke='none',sw=1,extra=''):
 return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def path(d,color=GOLD,width=3,fill='none',extra=''):
 return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def boss(x,y,r=60,front='up'):
 dy=-1 if front=='up' else 1
 return circle(x,y,r,'#69707b55','#969ca8',2)+path(f'M{x-11} {y+dy*(r-2)}L{x} {y+dy*(r+17)}L{x+11} {y+dy*(r-2)}',GOLD,2,GOLD)+text(x,y+9,'Vloxx',27,INK,'middle',500)
def green(x,y,r):
 return circle(x,y,r,'#54c99120',GREEN,2.5)
def dot(x,y,marked=False,fix=False):
 s=circle(x,y,9,INK,GREEN if marked else BG,2.5 if marked else 2)
 if fix:s+=path(f'M{x} {y-43}l14 18-14 18-14-18Z',PURPLE,2,PURPLE)
 return s
def label(x,y,name):return text(x,y,name,28,GREEN,'middle',500)
def group(x,y,r,name,n,fix=False,towards='up'):
 offsets=[(0,0),(-24,-20),(24,-20),(0,-38)] if towards=='up' else [(0,0),(24,-22),(40,0),(12,-40)]
 return green(x,y,r)+''.join(dot(x+dx,y+dy,i==0,fix and i==0) for i,(dx,dy) in enumerate(offsets[:n]))+label(x,y+r-30,name)
def diagram(name):
 s=''
 if name=='p1':
  s+=boss(360,260,62,'down')
  s+=group(200,380,105,'Melee',4,towards='in')+group(520,380,105,'Ranged',3)+group(360,630,105,'Healers',3,True)
  # Movement is shown by the arrow; explanatory text stays below.
  s+=path('M310 380H410M393 368L410 380L393 392',GOLD,4)
 elif name=='p2':
  s+=path('M320 244.282L25 755.237M400 244.282L695 755.237',RED,5)
  s+=boss(360,175,56,'down')
  s+=group(360,410,100,'Melee',4)+group(260,650,100,'Healers',3,True)+group(460,650,100,'Ranged',3)
  s+=path('M399 505L421 555M407 541L421 555L421 535',GOLD,4)
 elif name=='p3':
  s+=path('M360 150V740','#424a58',2,extra='stroke-dasharray="9 10"')
  s+=green(360,265,120)+green(270,530,120)+green(450,530,120)+boss(360,285,72,'up')
  s+=dot(360,265,True,True)+dot(347.5,330)+dot(372.5,330)
  for i,(x,y) in enumerate([(270,530),(310,467),(300,495),(288,475)]):s+=dot(x,y,i==0)
  for i,(x,y) in enumerate([(450,530),(410,467),(420,495)]):s+=dot(x,y,i==0)
  s+=label(360,185,'Healers')+label(255,610,'Melee')+label(465,610,'Ranged')
 elif name=='p4-bunker':
  s+=path('M360 210V760','#424a58',2,extra='stroke-dasharray="9 10"')+boss(360,160,55,'up')
  r=153.6;pt=lambda x,y:(360+x*.64,500+y*.64)
  for x,y in [(0,-190),(-165,95),(165,95)]:s+=green(*pt(x,y),r)
  s+=circle(360,500,r,'#b986ea0b',PURPLE,3)
  for i,(x,y) in enumerate([(0,-190),(-25,-210),(25,-210),(0,-225)]):s+=dot(*pt(x,y),i==0)
  for i,(x,y) in enumerate([(-165,95),(-170,130),(-150,145)]):s+=dot(*pt(x,y),i==0,i==0)
  for i,(x,y) in enumerate([(165,95),(170,130),(150,145)]):s+=dot(*pt(x,y),i==0)
  s+=label(360,310,'Melee')+label(225,665,'Healers')+label(495,665,'Ranged')
  s+=text(676,242,'Projectile Block',28,PURPLE,'end',500)+path('M600 260L360 500M363 484L360 500L376 497',GOLD,2.5)
 else:
  s+=boss(470,155,55,'up')+group(470,310,88,'Melee',4)+group(470,505,88,'Healers',3,True)+group(470,700,88,'Ranged',3)
  s+=text(215,444,'Move left',27,GOLD,'middle',500)+text(215,478,'together',27,GOLD,'middle',500)
  s+=path('M355 515H120M143 497L120 515L143 533',GOLD,4)
 return s

def wrap(note,width=52):
 if len(note)<=width:return [note]
 words=note.split();options=[]
 for i in range(2,len(words)-1):
  a,b=' '.join(words[:i]),' '.join(words[i:])
  if max(len(a),len(b))<=width:options.append((abs(len(a)-len(b)),[a,b]))
 if options:return min(options,key=lambda o:o[0])[1]
 candidates=[textwrap.wrap(note,w) for w in range(max(24,width-18),width+1)]
 return min(candidates,key=lambda lines:(any(len(line.split())<2 for line in lines),len(lines),max(map(len,lines))-min(map(len,lines))))

inners={}
for name,title,tag,notes in PANELS:
 body=f'<rect width="{W}" height="{H}" fill="{BG}"/><rect x="20" y="20" width="680" height="1480" rx="7" fill="{SURFACE}" stroke="#343a48"/>'
 body+=text(44,65,title,36,GOLD,weight=600)+text(44,98,tag,19,MUTED,weight=500)+path('M44 116H676','#454331',1.5)
 body+=diagram(name)
 body+=path('M44 866H676','#343a48',1.5)+text(58,909,'Placement',27,GOLD,weight=500)
 y=954
 for note in notes:
  lines=wrap(note);assert len(lines)<=4,(name,note,lines)
  body+=circle(62,y-9,3.5,GOLD)
  for line in lines:body+=text(82,y,line,23);y+=30
  y+=12
 assert y-45<=1485,(name,y)
 inners[name]=body
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)} green formation</title><desc id="desc">{html.escape(" ".join(notes))}</desc><g font-family="IBM Plex Sans,Segoe UI,Arial,sans-serif">{body}</g></svg>'
 (OUT/f'green-strategy-{name}.svg').write_text(svg,encoding='utf8')
legend=circle(2790,55,8,INK)+text(2808,62,'Player',20,MUTED)+circle(2930,55,8,INK,GREEN,2.5)+text(2948,62,'Green player',20,MUTED)+path('M3150 41l10 14-10 14-10-14Z',PURPLE,2,PURPLE)+text(3170,62,'Fixate',20,MUTED)+circle(3290,55,11,'none',GREEN,2.5)+text(3310,62,'Green',20,MUTED)
full=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3600 1630" width="3600" height="1630" role="img" aria-labelledby="title"><title id="title">WRDL green strategy · P1–P4</title><rect width="3600" height="1630" fill="{BG}"/><g font-family="IBM Plex Sans,Segoe UI,Arial,sans-serif">'+text(44,54,'NEXUS OF ETERNITY · WRDL GREEN STRATEGY',32,GOLD,weight=600)+text(44,88,'Fixate always gets a green. Melee stand closest to bait the other two; ranged and healers stay farther back. Three players per green; stay in one circle only.',22,MUTED)+legend
for i,(name,*_) in enumerate(PANELS):full+=f'<g transform="translate({i*720},110)">{inners[name]}</g>'
full+='</g></svg>'
(OUT/'green-strategy-full.svg').write_text(full,encoding='utf8')
print('Redrew the five guild-reference formations and complete overview as native vectors.')
