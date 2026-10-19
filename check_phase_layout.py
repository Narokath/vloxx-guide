from html.parser import HTMLParser
from pathlib import Path
import collections
class Inspect(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.tabs=[];self.ids={};self.frames={};self.panels=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if 'id' in d:self.ids[d['id']]=d
  if 'data-mechanic' in d:self.tabs.append(d)
  if 'mechanic-panel' in d.get('class','').split():self.panels.append(d)
  if t=='iframe':self.frames[d['id']]=[x for _,x in self.stack]
  if t not in ('input','img','meta','link','br','hr','source','wbr','area','base','embed','param','track'):self.stack.append((t,d))
 def handle_endtag(self,t):
  if self.stack:
   assert self.stack[-1][0]==t,(t,self.stack[-1][0])
   self.stack.pop()
p=Inspect();p.feed(Path('Vloxx_Guide.html').read_text(encoding='utf8'));assert not p.stack
assert len(p.tabs)==len(p.panels)==24
for tab in p.tabs:
 panel=p.ids[tab['data-mechanic']];assert panel['aria-labelledby']==tab['id'];assert ('hidden' in panel)==(tab['aria-selected']=='false')
for name in ['excision-frame','p4-frame']:
 assert any('advanced-section' in d.get('class','').split() for d in p.frames[name])
assert any('mode-cm' in d.get('class','').split() for d in p.frames['p4-frame'])
assert 'echo-play' in p.ids and 'green-image' in p.ids
print('PASS: balanced HTML; 24 mechanic tabs/panels linked; simulations in advanced sections; crossover CM-only; green and playback controls preserved.')
