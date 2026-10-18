"""Build the self-contained guide using only checked-in project files."""
from pathlib import Path
import base64, json
HERE=Path(__file__).resolve().parent
def data(path,mime):
 return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
def html_data(s):
 return 'data:text/html;base64,'+base64.b64encode(s.encode()).decode()
def build():
 sim=(HERE/'excision-simulator.html').read_text(encoding='utf8')
 p4=(HERE/'p4-simulator.html').read_text(encoding='utf8')
 body=(HERE/'guide-body.html').read_text(encoding='utf8')
 replacements={'{{EXCISION_SIM}}':html_data(sim),'{{P4_SIM}}':html_data(p4),'{{GREEN_P1_CM}}':data(HERE/'diagrams/green-strategy-p1.svg','image/svg+xml')}
 strategy_image=data(HERE/'diagrams/green-strategy-full.svg','image/svg+xml')
 replacements.update({'{{GREEN_STRATEGY_FULL}}':'" data-green-full="true'})
 for panel in ('P1','P2','P3','BUNKER','BONESKINNER'):
  name=panel.lower() if panel.startswith('P') else 'p4-'+panel.lower()
  key=panel[1:]+'-CM' if panel.startswith('P') else '4-CM' if panel=='BUNKER' else '4-LCM'
  replacements['{{GREEN_STRATEGY_'+panel+'}}']='" data-green-strategy="'+key
 replacements['{{GREEN_P1_CM}}']='" data-green-strategy="1-CM'
 for k,v in replacements.items():assert k in body;body=body.replace(k,v)
 body=body.replace('src="" data-green','data-green')
 diagrams={str(phase)+'-'+mode:(HERE/('diagrams/green-strategy-'+('p'+str(phase) if phase<4 else 'p4-bunker' if mode=='CM' else 'p4-boneskinner')+'.svg')).read_text(encoding='utf8').replace(strategy_image,'@@IMAGE@@') for mode in ('CM','LCM') for phase in range(1,5)}
 doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Vloxx CM and LCM encounter guide with green placements and sword simulations."><title>Vloxx — CM &amp; LCM Guide</title><style>'+(HERE/'guide.css').read_text(encoding='utf8')+'</style></head><body data-mode="CM">'+body+'<script id="diagrams-data" type="application/json">'+json.dumps(diagrams)+'</script><script id="strategy-image-data" type="application/json">'+json.dumps(strategy_image)+'</script><script>'+(HERE/'echo-model.js').read_text(encoding='utf8')+'\n'+(HERE/'guide.js').read_text(encoding='utf8')+'\n'+(HERE/'echo-controller.js').read_text(encoding='utf8')+'\n'+(HERE/'mechanic-browser.js').read_text(encoding='utf8')+'\n'+(HERE/'weapon-movement-sim.js').read_text(encoding='utf8')+'</script></body></html>'
 assert '{{' not in doc
 (HERE/'Vloxx_Guide.html').write_text(doc,encoding='utf8')
 print('Built Vloxx_Guide.html')
if __name__=='__main__':build()
