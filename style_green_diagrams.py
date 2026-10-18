"""Native vector redraw of the approved green formations in the guide palette."""
from pathlib import Path
import re,html,runpy,textwrap
runpy.run_path('make_diagrams.py')
OUT=Path('diagrams');BG='#0a0e18';GOLD='#e8c976';INK='#eae6da';MUTED='#a8aaaf'
PANELS=[('p1',1,'cm','P1 · Staff','100–70%', ['Bait greens close; faster holder takes right.','Melee left · ranged right · healers/fixate rear.','Floater joins fixate if a healer is fixated; otherwise melee.','Both healers avoid baiting their own greens.']),('p2',2,'cm','P2 · Spear','70–40%', ['Keep all greens inside the same safe wedge.','Melee front · healers + fixate back left · ranged back right.','Floater joins fixate if a healer is fixated; otherwise melee.']),('p3',3,'cm','P3 · Sword','40–10%', ['Fixate stays close in front; healers soak behind boss centre.','Back up rear greens to clear fixate’s green.','Rear soakers stay near the centre line in one green each.']),('p4-bunker',4,'cm','P4 · Bunker','CM ONLY', ['Keep melee and rear groups close behind Vloxx.','Overlap green edges inside the projectile field.','Keep every soaker in one green’s exclusive area.','Higher uptime; maintain the field rotation. Not viable in LCM.']),('p4-boneskinner',4,'lcm','P4 · Boneskinner','CM / LCM', ['Melee front · healers/fixate mid · ranged rear.','Keep all three greens soaked behind Vloxx.','Move left together out of spears and third-wave puddles.','Lower uptime; keep up with the group while resolving greens.'])]
def txt(x,y,s,size=22,fill=INK,weight=400,anchor='start'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{html.escape(s)}</text>'
def balanced_wrap(note,width=47):
 if len(note)<=width:return [note]
 words=note.split();options=[]
 for i in range(2,len(words)-1):
  a,b=' '.join(words[:i]),' '.join(words[i:])
  if max(len(a),len(b))<=width:
   score=abs(len(a)-len(b))
   if words[i-1].endswith((';','.',':')):score-=6
   options.append((score,[a,b]))
 return min(options,key=lambda v:v[0])[1] if options else textwrap.wrap(note,width=width)

def content(phase,mode):
 s=(OUT/f'p{phase}-{mode}.svg').read_text(encoding='utf8');body=s.split('<g font-family="Segoe UI,Arial,sans-serif">',1)[1].rsplit('</g></svg>',1)[0]
 body=re.sub(r'^<text.*?</text><text.*?</text>','',body,flags=re.S)
 body=body.split('<circle cx="48" cy="725"',1)[0]
 # Replace narrative annotations with consistent instruction cards below.
 body=re.sub(r'<text\b[^>]*\by="(?:620|644|651|652)"[^>]*>.*?</text>','',body)
 if phase==2:body=body.replace('M360 160 L100 580 M360 160 L660 580','M320 244.282 L65 685.955 M400 244.282 L655 685.955')
 if phase==4 and mode=='cm':
  head,tail=body.split('</text>',1);body=head+'</text><g transform="translate(0,100)">'+tail+'</g>'
 if phase==4 and mode=='lcm':
  body=re.sub(r'cy="(602|620|642|630)"',lambda m:'cy="'+str(int(m[1])+20)+'"',body)
  body=body.replace('y="585"','y="605"')
  body=body.replace('Resolve greens','Keep greens soaked').replace('then shift left','shift left together')
 body=body.replace('Cloud','Projectile Block').replace('462,166 382,190','430,166 382,190').replace('548,348 501,374','474,348 501,374')
 body=body.replace('#10131d',BG).replace('#e7e0d0',INK).replace('#dcb976',GOLD).replace('#a9acb2',MUTED)
 body=re.sub(r'font-size="[\d.]+"','font-size="28"',body)
 # Keep labels clear through positioning and leader lines, never text backplates.
 body=re.sub(r'<text\b[^>]*>(Healers \+ F|Fixate|Projectile Block)</text>','',body)
 body=re.sub(r'<polyline\b[^>]*/>','',body)
 if phase==3:body=re.sub(r'<text\b[^>]*>Healers</text>','',body)
 def callout(x,y,label,points,anchor='start'):
  return '<polyline points="'+points+'" fill="none" stroke="'+GOLD+'" stroke-width="2"/>'+txt(x,y,label,28,GOLD,500,anchor)
 def group_label(x,y,label):
  return txt(x,y,label,28,'#54c991',500,'middle')
 if phase==1:
  body=re.sub(r'<text\b[^>]*>(Melee|Ranged)</text>','',body)
  body+=group_label(210,350,'Melee')+group_label(510,350,'Ranged')+group_label(360,540,'Healers')
 elif phase==2:
  body=re.sub(r'<text\b[^>]*>(Melee|Ranged)</text>','',body)
  body+=group_label(360,415,'Melee')+group_label(280,615,'Healers')+group_label(440,615,'Ranged')
 elif phase==3:
  body=re.sub(r'<text\b[^>]*>(Melee|Ranged)</text>','',body)
  body+=group_label(360,140,'Healers')
  body+=group_label(255,525,'Melee')+group_label(465,525,'Ranged')
 elif mode=='cm':
  body=re.sub(r'<text\b[^>]*>Ranged</text>','',body)
  body+=group_label(225,665,'Healers')+group_label(495,665,'Ranged')
  body+=txt(668,245,'Projectile Block',28,'#b986ea',500,'end')
  body+=f'<path d="M600 260 L360 500 M363 484 L360 500 L376 497" fill="none" stroke="{GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
 else:
  body=re.sub(r'<text\b[^>]*>(Melee|Ranged)</text>','',body)
  body+=group_label(470,365,'Melee')+group_label(470,530,'Healers')+group_label(470,695,'Ranged')

 return body
inners={}
for name,phase,mode,title,tag,notes in PANELS:
 body=f'<rect width="720" height="1200" rx="8" fill="{BG}"/><rect x="20" y="20" width="680" height="1160" rx="6" fill="#101524" stroke="#343a48"/>'
 body+=txt(44,59,title,36,GOLD,600)+'<path d="M44 82H676" stroke="#454331"/>'
 body+=content(phase,mode)
 bullet_lines=[balanced_wrap(note) for note in notes]
 assert sum(map(len,bullet_lines))<=8,(name,bullet_lines)
 body+='<rect x="38" y="764" width="644" height="365" rx="5" fill="#151b2b" stroke="#353c49"/>'+txt(58,802,'PLACEMENT',20,GOLD,600)+'<path d="M58 816H662" stroke="#343a48"/>'
 y=851
 for lines in bullet_lines:
  body+=f'<circle cx="62" cy="{y-8}" r="3.5" fill="{GOLD}"/>'
  for line in lines:body+=txt(82,y,line,24);y+=31
  y+=12


 inners[name]=body
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 1200" width="720" height="1200" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)} green formation</title><desc id="desc">Ten players in three green groups. {html.escape(" ".join(notes))}</desc><g font-family="IBM Plex Sans,Segoe UI,Arial,sans-serif">{body}</g></svg>'
 (OUT/f'green-strategy-{name}.svg').write_text(svg,encoding='utf8')
legend='<circle cx="58" cy="1165" r="7" fill="#eae6da"/><circle cx="210" cy="1165" r="7" fill="#eae6da" stroke="#54c991" stroke-width="2.5"/><path d="M420 1154l8 11-8 11-8-11Z" fill="#b986ea"/><circle cx="565" cy="1165" r="10" fill="none" stroke="#54c991" stroke-width="2.5"/>'+txt(76,1172,'Player',20,MUTED)+txt(228,1172,'Green holder',20,MUTED)+txt(438,1172,'Fixate',20,MUTED)+txt(585,1172,'Green',20,MUTED)
full=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3600 1310" width="3600" height="1310" role="img" aria-labelledby="title"><title id="title">Complete WRDL green strategy, P1 to P4</title><rect width="3600" height="1310" fill="{BG}"/><g font-family="IBM Plex Sans,Segoe UI,Arial,sans-serif">'+txt(44,54,'GREEN STRATEGY · P1–P4',32,GOLD,600)+txt(44,88,'Three valid soakers per green. Stand in one circle only. Both healers avoid baiting separate greens.',21,MUTED)
full+='<g transform="translate(2770,-1110)">'+legend+'</g>'
for i,(name,*_) in enumerate(PANELS):full+=f'<g transform="translate({i*720},110)">{inners[name]}</g>'
full+='</g></svg>';(OUT/'green-strategy-full.svg').write_text(full,encoding='utf8');print('Redrew five phase panels and full overview as native vectors.')
