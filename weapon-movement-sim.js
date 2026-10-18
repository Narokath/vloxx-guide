(function(root){'use strict';
const END=16,DT=.02,START=[-600,0],distance=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
function players(t,scenario='swap'){if(scenario==='static')return[{name:'A',p:[600,-180]},{name:'B',p:[-300,220]},{name:'C',p:[0,300]}];const u=(t%10)/10,x=u<.5?650-2000*u:-350+2000*(u-.5);return[{name:'A',p:[x,-180]},{name:'B',p:[300-x,200]},{name:'C',p:[-150,320]}];}
function simulate(input){const cfg={at:1,duration:5,speed:240,interval:2,range:350,scenario:'swap',...input};let p=[...START],goal=null,committed=null,snapshot=null,cast=null,nextSample=0;const frames=[],events=[];
 for(let i=0;i<=END/DT;i++){const t=i*DT,imm=cfg.duration>0&&t>=cfg.at&&t<cfg.at+cfg.duration,ps=players(t,cfg.scenario);let moving=false;
  if(cast&&t>=cast.until)cast=null;
  if(t+1e-8>=nextSample){nextSample+=cfg.interval;const furthest=ps.reduce((a,b)=>distance(p,b.p)>distance(p,a.p)?b:a);snapshot={name:furthest.name,p:[...furthest.p],at:t,origin:[...p]};
   if(cast)events.push({t,kind:'sample',state:`Recorded ${snapshot.name}; current cast continues`});
   else if(distance(p,snapshot.p)<=cfg.range){goal=null;committed=null;cast={until:t+1,p:[...snapshot.p],name:snapshot.name};events.push({t,kind:'cast',state:`In range: cast at recorded ${snapshot.name} position`});}
   else if(imm)events.push({t,kind:'blocked',state:`Recorded ${snapshot.name}; Immobilize blocks a new movement command${goal?' · previous path continues':''}`});
   else{const d=distance(p,snapshot.p),travel=d-cfg.range;goal=p.map((x,j)=>x+(snapshot.p[j]-x)*travel/d);committed={...snapshot,p:[...snapshot.p]};events.push({t,kind:'commit',state:`Recorded ${snapshot.name}; new path to casting range accepted`});}}
  if(goal&&!cast){const d=distance(p,goal),step=Math.min(d,cfg.speed*DT);if(d>.001){p=p.map((x,j)=>x+(goal[j]-x)*step/d);moving=true;}if(d<=step+.001){p=[...goal];goal=null;cast={until:t+1,p:[...committed.p],name:committed.name};events.push({t,kind:'cast',state:`Reached casting range: cast at recorded ${committed.name} position`});}}
  const state=cast?'Casting at recorded '+cast.name+' position':goal?'Following committed path to recorded '+committed.name:imm?'Stationary · waiting for a movement check':'Stationary · waiting for next sample';
  frames.push({t,p:[...p],players:ps,snapshot:snapshot?{...snapshot,p:[...snapshot.p]}:null,goal:goal?[...goal]:null,committed:committed?{...committed,p:[...committed.p]}:null,cast:cast?{...cast,p:[...cast.p]}:null,state,imm,moving,nextSample});}return{frames,events,cfg};}
root.WeaponMovementModel={simulate,players,END,DT,START};if(typeof module==='object')module.exports=root.WeaponMovementModel;if(!root.document)return;
const $=id=>document.getElementById(id);let result,playing=false,raf=0,last=0,playTime=0;
const val=(id,lo,hi,fallback)=>{const n=Number($(id).value);return Number.isFinite(n)?Math.max(lo,Math.min(hi,n)):fallback;};
function config(){return{at:val('weapon-imm-at',0,16,1),duration:val('weapon-imm-duration',0,12,5),speed:240,interval:val('weapon-interval',.25,5,2),range:val('weapon-range',100,600,350),scenario:$('weapon-players').value};}
function stop(){playing=false;cancelAnimationFrame(raf);$('weapon-play').textContent='Play';}
function refresh(){stop();result=simulate(config());draw();}
const pt=p=>[390+p[0]*.38,220+p[1]*.38];
function draw(){const t=+$('weapon-time').value,f=result.frames[Math.min(result.frames.length-1,Math.floor((t+1e-6)/DT))],cfg=result.cfg;let s='';
 const circle=(p,r,fill,stroke,ex='')=>`<circle cx="${p[0]}" cy="${p[1]}" r="${r}" fill="${fill}" stroke="${stroke}" ${ex}/>`;
 const label=(p,txt,col='#e3dece',sz=14)=>`<text x="${p[0]}" y="${p[1]}" text-anchor="middle" font-size="${sz}" style="fill:${col}">${txt}</text>`;
 s+=circle(pt([0,0]),36,'#69738022','#7b818b')+label(pt([0,0]),'Vloxx');
 for(const player of f.players){const q=pt(player.p);s+=circle(q,7,'#86bfe8','#dbeaf5')+label([q[0],q[1]+24],'Player '+player.name,'#86bfe8');}
 if(f.snapshot){const q=pt(f.snapshot.p);s+=circle(q,10,'none','#cad0db','stroke-dasharray="3 3"')+circle(q,cfg.range*.38,'none','#454854','stroke-dasharray="4 6"')+label([q[0],q[1]-20],`Recorded ${f.snapshot.name} · ${f.snapshot.at.toFixed(2)} s`,'#cad0db',12);}
 const q=pt(f.p);if(f.goal){const g=pt(f.goal);s+=`<path d="M${q.join(' ')} L${g.join(' ')}" stroke="#dfb96d" stroke-width="2" stroke-dasharray="5 5"/>`+circle(g,5,'none','#dfb96d')+label([g[0],g[1]+22],'Committed destination','#dfb96d',11);}
 if(f.cast){const to=pt(f.cast.p);s+=`<path d="M${q.join(' ')} L${to.join(' ')}" stroke="#54c991" stroke-width="3"/>`+circle(to,13,'none','#54c991')+label([to[0],to[1]-35],'Cast at recorded position','#54c991',12);}
 let path='';for(let i=0;i<result.frames.length&&result.frames[i].t<=t;i+=5){const p=pt(result.frames[i].p);path+=(path?'L':'M')+p.join(' ');}s+=`<path d="${path}" fill="none" stroke="#dfb96d" stroke-opacity=".4"/>`+circle(q,11,'#dfb96d','#fff0c5')+(f.imm?circle(q,20,'none','#b78aff','stroke-width="3"'):'')+label([q[0],q[1]-28],'Staff','#dfb96d');
 s+=label([390,25],f.state,'#dfb96d',16)+label([390,49],f.imm?'IMMOBILIZE ACTIVE · existing path is not cancelled':'Immobilize inactive',f.imm?'#b78aff':'#9298a3',12);
 s+=`<rect x="45" y="393" width="690" height="8" fill="#30343f"/><rect x="${45+cfg.at/END*690}" y="393" width="${Math.max(0,Math.min(END,cfg.at+cfg.duration)-cfg.at)/END*690}" height="8" fill="#b78aff"/>`;
 for(const e of result.events)if(['commit','blocked','sample'].includes(e.kind)){const x=45+e.t/END*690;s+=`<line x1="${x}" x2="${x}" y1="382" y2="401" stroke="${e.kind==='blocked'?'#f2827b':'#54c991'}"/>`;}
 s+=`<line x1="${45+t/END*690}" y1="377" x2="${45+t/END*690}" y2="411" stroke="#fff0c5"/>`+label([390,435],'Purple: Immobilize · green/red ticks: position checks · white: recorded position','#a6a8aa',12);
 $('weapon-map').innerHTML=s;$('weapon-clock').value=t.toFixed(2)+' s';$('weapon-status').textContent=`${f.state}. Next furthest-player sample: ${f.nextSample.toFixed(2)} s.`;
 $('weapon-evidence').textContent='Proposed Staff behaviour: sample the furthest player; issue a path only if not immobilized; keep an already committed path. Exact sampling cadence, target weighting and casting geometry remain unconfirmed.';
 $('weapon-events').innerHTML=result.events.filter(e=>e.t<=t+.001).map(e=>`<li><strong>${e.t.toFixed(2)} s</strong> · ${e.state}</li>`).join('');}
 $('weapon-preset').onchange=()=>{const presets={before:[0,4],during:[1,5],handoff:[1.8,4],none:[0,0]},v=presets[$('weapon-preset').value];$('weapon-imm-at').value=v[0];$('weapon-imm-duration').value=v[1];$('weapon-time').value=0;refresh();};
 ['weapon-imm-at','weapon-imm-duration','weapon-interval','weapon-range','weapon-players'].forEach(id=>$(id).onchange=refresh);$('weapon-time').oninput=()=>{stop();draw();};$('weapon-reset').onclick=()=>{stop();$('weapon-time').value=0;draw();};
 $('weapon-play').onclick=()=>{if(playing){stop();return;}if(+$('weapon-time').value>=END)$('weapon-time').value=0;playTime=+$('weapon-time').value;last=performance.now();playing=true;$('weapon-play').textContent='Pause';const tick=now=>{if(!playing)return;playTime=Math.min(END,playTime+(now-last)/1000);last=now;$('weapon-time').value=playTime;draw();if(playTime>=END)stop();else raf=requestAnimationFrame(tick);};raf=requestAnimationFrame(tick);};refresh();
})(typeof window==='object'?window:globalThis);
