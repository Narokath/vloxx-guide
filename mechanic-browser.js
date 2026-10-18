/* Phase mechanic browsers keep advanced simulators mounted while switching descriptions. */
(()=>{'use strict';
document.querySelectorAll('.mechanic-menu').forEach(menu=>{
 const tabs=[...menu.querySelectorAll('[data-mechanic]')];
 const select=tab=>{tabs.forEach(b=>{const active=b===tab;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;document.getElementById(b.dataset.mechanic).hidden=!active;});};
 tabs.forEach((tab,i)=>{tab.onclick=()=>select(tab);tab.onkeydown=e=>{let next;if(e.key==='ArrowDown'||e.key==='ArrowRight')next=(i+1)%tabs.length;else if(e.key==='ArrowUp'||e.key==='ArrowLeft')next=(i+tabs.length-1)%tabs.length;else if(e.key==='Home')next=0;else if(e.key==='End')next=tabs.length-1;else return;e.preventDefault();select(tabs[next]);tabs[next].focus();};});
});
function reveal(hash){if(!hash)return;let target;try{target=document.getElementById(decodeURIComponent(hash.slice(1)));}catch{return;}if(!target)return;for(let node=target;node;node=node.parentElement){if(node.classList?.contains('mechanic-panel'))document.querySelector('[data-mechanic="'+node.id+'"]')?.click();}for(let el=target;el;el=el.parentElement)if(el.tagName==='DETAILS')el.open=true;}
document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',()=>reveal(a.getAttribute('href'))));addEventListener('hashchange',()=>reveal(location.hash));reveal(location.hash);
const full=document.getElementById('green-fullsize'),dialog=document.getElementById('strategy-lightbox');if(full&&dialog)full.onclick=()=>dialog.showModal();
})();
