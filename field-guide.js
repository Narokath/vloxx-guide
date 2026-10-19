/* Switch between a complete reading view and the original focused mechanic browser. */
(()=>{'use strict';const button=document.getElementById('reading-view');if(!button)return;
const panels=[...document.querySelectorAll('.mechanic-panel')];const original=panels.map(p=>({p,role:p.getAttribute('role'),label:p.getAttribute('aria-labelledby')}));
const overview=document.querySelector('.strategy-overview');if(overview){const details=document.createElement('details');details.className='field-formation-disclosure';const summary=document.createElement('summary');summary.textContent='View all green formations';overview.before(details);details.append(summary,overview);}
function apply(cards){document.body.dataset.reading=cards?'cards':'focused';button.setAttribute('aria-pressed',String(!cards));button.textContent=cards?'Browse one mechanic at a time':'Show all mechanic cards';
for(const {p,role,label} of original){if(cards){p.hidden=false;p.setAttribute('role','article');p.removeAttribute('aria-labelledby');}else{p.setAttribute('role',role);p.setAttribute('aria-labelledby',label);}}
if(!cards)document.querySelectorAll('.mechanic-menu').forEach(m=>m.querySelector('[aria-selected="true"]')?.click());}
button.onclick=()=>apply(document.body.dataset.reading!=='cards');
document.addEventListener('click',e=>{if(document.body.dataset.reading==='cards'&&e.target.closest?.('[data-mechanic]'))e.stopImmediatePropagation();},true);
// Do not treat a collapsed shared-formation disclosure as an anchor destination.
function revealGreens(){if(location.hash==='#greens'&&overview)overview.parentElement.open=true;}
addEventListener('hashchange',revealGreens);apply(false);revealGreens();})();
