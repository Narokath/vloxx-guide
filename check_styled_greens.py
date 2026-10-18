from pathlib import Path
import xml.etree.ElementTree as ET,re,math
for name in ['p1','p2','p3','p4-bunker','p4-boneskinner']:
 root=ET.parse(Path('diagrams')/f'green-strategy-{name}.svg').getroot();dots=[];greens=[];fields=[];holders=[]
 def walk(node,dx=0,dy=0):
  match=re.search(r'translate\(([-.\d]+)[ ,]+([-.\d]+)\)',node.get('transform',''))
  if match:dx+=float(match[1]);dy+=float(match[2])
  if node.tag.endswith('circle'):
   p=(float(node.get('cx'))+dx,float(node.get('cy'))+dy);r=float(node.get('r'))
   if r==9 and node.get('fill')=='#eae6da':
    if node.get('stroke')=='#54c991':
     assert float(node.get('stroke-width'))==2.5
     holders.append(p)
    else:assert node.get('stroke')=='#0a0e18'
    dots.append(p)
   if r>50 and node.get('stroke')=='#54c991':greens.append((*p,r))
   if r>50 and node.get('stroke')=='#b986ea':fields.append((*p,r))
  for child in node:walk(child,dx,dy)
 walk(root);assert len(dots)==10,(name,len(dots));assert len(greens)==3;assert len(holders)==3;assert all(any(math.dist(h,(x,y))<.01 for h in holders) for x,y,r in greens);counts=[0,0,0]
 for p in dots:
  memberships=[i for i,(x,y,r) in enumerate(greens) if math.dist(p,(x,y))<r]
  assert len(memberships)==1,(name,p,memberships);counts[memberships[0]]+=1
 assert min(counts)>=3,(name,counts)
 if name in ('p1','p2'):
  assert all(any(math.dist(p,(x,y))<.01 for p in dots) for x,y,r in greens),(name,'missing centred holder')
 if name=='p3':
  clearance=min(abs(math.dist(p,(x,y))-r) for p in dots for x,y,r in greens)
  assert clearance>=30,(name,'edge clearance',clearance)
 if name=='p2':
  for x,y,r in greens:
   lane_distance=(y-175)*.5-abs(x-360)*(3**.5/2)
   assert lane_distance-r>=10,(name,'green crosses lane',x,y,lane_distance-r)

 if name=='p4-bunker':assert all(math.dist(p,fields[0][:2])<fields[0][2] for p in dots)
 assert not any(n.tag.endswith('image') for n in root.iter());print(name,counts,'native vectors; exclusive soaks verified')
