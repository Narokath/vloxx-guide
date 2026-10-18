/* Echoing rehearsal: geometry and search are shared by the UI and verification. */
(function(root){'use strict';
const TAU=Math.PI*2,DT=.05,END=18,deg=x=>x*Math.PI/180,dist=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
const offsets=Array.from({length:9},(_,i)=>[(i%3-1)*24,(Math.floor(i/3)-1)*24]);
function dodging(t,ds){return ds.some(s=>t>=s&&t<s+.75);}
function clock(t,ds){return t+ds.reduce((n,s)=>n+Math.max(0,Math.min(.75,t-s))*190/210,0);}
function route(t,spec,ds=[]){const u=clock(t,ds),a=deg(spec.angle),r=spec.radius;
 if(spec.type==='hold'&&spec.fix)return[0,-180];
 if(spec.fix){const side=spec.side||1,width=spec.width||300,depth=spec.depth||180,way=[[0,-180],[side*width,-depth],[-side*width,-depth],[0,-180]];let travel=u*210;for(let i=1;i<way.length;i++){if(i===3){const wait=(spec.wait||0)*210;if(travel<wait)return way[i-1];travel-=wait;}const d=dist(way[i-1],way[i]);if(travel<=d)return way[i-1].map((x,j)=>x+(way[i][j]-x)*travel/d);travel-=d;}return way.at(-1);}
 // Every squad route includes a scored return to the rear stack.
 const outward=v=>{if(spec.type==='hold')return[r*Math.cos(a),r*Math.sin(a)];if(spec.type==='range'){const rr=Math.min(780,r+v*210);return[rr*Math.cos(a),rr*Math.sin(a)];}const arc=deg(280),travel=v*210,turn=Math.min(arc,travel/r),rr=r+Math.max(0,Math.min(780-r,travel-r*arc)),ang=a-turn;return[rr*Math.cos(ang),rr*Math.sin(ang)];};
 const returnAt=spec.returnAt||7;if(u<=returnAt)return outward(u);const from=outward(returnAt),target=[0,220],length=dist(from,target),progress=Math.min(1,(u-returnAt)*210/(length||1));return progress===1?target:from.map((x,i)=>x+(target[i]-x)*progress);

}
function validDodges(spec,ds){return ds.every(start=>{let length=0,p=route(start,spec,ds);for(let t=start+.025;t<=start+.75001;t+=.025){const q=route(t,spec,ds);length+=dist(p,q);p=q;}return length>=290;});}
function missiles(cfg,fix,ds){return Array.from({length:8},(_,i)=>{const at=1+.6*i,angle=deg(cfg.first-40*i),o=[500*Math.cos(angle),500*Math.sin(angle)],aim=route(at,fix,ds),d=dist(o,aim)||1;return{id:i,at,o,v:aim.map((x,j)=>(x-o[j])/d*cfg.speed),end:at+12};});}
function missilePoint(m,t){return m.o.map((x,j)=>x+m.v[j]*(t-m.at));}
function interception(m,f){if(f.kind==='off')return Infinity;const dur=f.kind==='cpc'?8:6,lo=Math.max(m.at,f.at),hi=Math.min(m.end,f.at+dur);if(lo>hi)return Infinity;const p=missilePoint(m,lo),v=m.v,q=[p[0]-f.x,p[1]-f.y],aa=v[0]**2+v[1]**2,bb=2*(q[0]*v[0]+q[1]*v[1]),cc=q[0]**2+q[1]**2-240**2;
 if(cc<=0)return lo;const disc=bb*bb-4*aa*cc;if(disc<0)return Infinity;const dt=(-bb-Math.sqrt(disc))/(2*aa);return dt>=0&&lo+dt<=hi?lo+dt:Infinity;}
function contacts(cfg,ms,spec,ds,fields,group){const events=new Map(),os=group?offsets:[[0,0]],cuts=ms.map(m=>cfg.mode==='CM'?Math.min(...fields.map(f=>interception(m,f)),Infinity):Infinity);const add=(id,t)=>{if(!events.has(id))events.set(id,[]);events.get(id).push(t);};
 for(let i=0;i<8;i++){const t=1+.6*i,p=route(t,spec,ds),a=deg(cfg.first-40*i);os.forEach((o,j)=>{const q=[p[0]+o[0],p[1]+o[1]];if(Math.hypot(...q)<=625+18&&q[0]*Math.cos(a)+q[1]*Math.sin(a)>=-18)add('slash '+(i+1)+' / '+(j+1),t);});}
 for(let t=1;t<=END;t+=DT){const p=route(t,spec,ds);ms.forEach((m,i)=>{if(t<m.at||t>m.end||t>=cuts[i])return;const q=missilePoint(m,t);os.forEach((o,j)=>{if(dist([p[0]+o[0],p[1]+o[1]],q)<=cfg.redRadius+18)add('red '+(i+1)+' / '+(j+1),t);});});}
 return [...events].map(([id,times])=>({id,times,uncovered:times.filter(t=>!dodging(t,ds))}));}
const score=es=>es.reduce((n,e)=>n+(e.uncovered.length?1:0),0);
function bestDodges(cfg,ms,spec,fields,group){let ds=[],es=contacts(cfg,ms,spec,ds,fields,group);
 for(let pass=0;pass<2;pass++){const times=[...new Set(es.flatMap(e=>e.uncovered).map(t=>Math.max(0,Math.round((t-.1)*10)/10)))];let best={s:score(es),ds,es};for(const t of times){if(ds.some(v=>Math.abs(v-t)<.85))continue;const cand=[...ds,t].sort((a,b)=>a-b);if(!validDodges(spec,cand))continue;const test=contacts(cfg,ms,spec,cand,fields,group),s=score(test);if(s<best.s)best={s,ds:cand,es:test};}if(best.ds===ds)break;ds=best.ds;es=best.es;}
 return{ds,events:es,hits:score(es),spec};}
function plan(cfg,fields){const fixSpecs=cfg.fixRoute==='hold'?[{fix:true,type:'hold'}]:[1,-1].flatMap(side=>[300,450].flatMap(width=>[180,360,600].flatMap(depth=>[0,2,4].map(wait=>({fix:true,type:'move',side,width,depth,wait})))));if(cfg.fixRoute!=='hold')fixSpecs.push(...[1,-1].map(side=>({fix:true,type:'move',side,width:480,depth:540,wait:4})));let bestFix;
 for(const spec of fixSpecs){const baseMs=missiles(cfg,spec,[]),base=contacts(cfg,baseMs,spec,[],[],false),seed=bestDodges(cfg,baseMs,spec,[],false);const times=[...new Set(base.flatMap(e=>[e.times[0]-.05,e.times.at(-1)-.7]).map(t=>Math.max(0,Math.round(t*20)/20)))].slice(0,24),schedules=[[],seed.ds,[1.5,2.75],...times.map(t=>[t])];for(let i=0;i<times.length;i++)for(let j=i+1;j<times.length;j++)if(Math.abs(times[i]-times[j])>=.85)schedules.push([times[i],times[j]].sort((a,b)=>a-b));
 for(const ds of schedules){if(!validDodges(spec,ds))continue;const ms=missiles(cfg,spec,ds),events=contacts(cfg,ms,spec,ds,[],false),p={spec,ds,ms,events,hits:score(events),slashes:events.filter(e=>e.id.startsWith('slash')&&e.uncovered.length).length};if(!bestFix||p.hits<bestFix.hits||p.hits===bestFix.hits&&(p.slashes<bestFix.slashes||p.slashes===bestFix.slashes&&p.ds.length<bestFix.ds.length))bestFix=p;}}
 bestFix.events=contacts(cfg,bestFix.ms,bestFix.spec,bestFix.ds,fields,false);bestFix.hits=score(bestFix.events);
 const specs=cfg.squadRoute==='hold'?[{type:'hold',radius:220,angle:cfg.first+180}]:cfg.squadRoute==='range'?[{type:'range',radius:220,angle:cfg.first+180}]:[180,220,260].flatMap(radius=>[-20,0,20].map(delta=>({type:'orbit',radius,angle:cfg.first+180+delta})));
 const returningSpecs=specs.flatMap(spec=>[6,7,8,10].map(returnAt=>({...spec,returnAt})));
 let squad;for(const spec of returningSpecs){const p=bestDodges(cfg,bestFix.ms,spec,fields,true);if(!squad||p.hits<squad.hits||p.hits===squad.hits&&p.ds.length<squad.ds.length)squad=p;}
 return{fix:bestFix,squad,ms:bestFix.ms,cuts:bestFix.ms.map(m=>cfg.mode==='CM'?Math.min(...fields.map(f=>interception(m,f)),Infinity):Infinity)};}
function optimize(cfg,fields,current){const ms=current.ms,deadlines=ms.map((m,i)=>Math.min(m.end,...[...current.fix.events,...current.squad.events].filter(e=>e.id.startsWith('red '+(i+1)+' /')).flatMap(e=>e.times)));if(cfg.mode!=='CM')return fields.map(f=>({...f,kind:'off'}));const sets=fields.map(f=>{if(f.kind==='off')return[{...f,mask:0}];const list=[];for(let x=-600;x<=600;x+=100)for(let y=-600;y<=400;y+=100)for(let at=0;at<=6;at+=.5){const c={...f,x,y,at},mask=ms.reduce((b,m,i)=>b|(interception(m,c)<deadlines[i]?1<<i:0),0);list.push({...c,mask});}return list.sort((a,b)=>pop(b.mask)-pop(a.mask)||Math.hypot(a.x,a.y)-Math.hypot(b.x,b.y)||a.at-b.at).filter((v,i,a)=>a.findIndex(w=>w.mask===v.mask)===i);});let best=null;for(const a of sets[0])for(const b of sets[1]){const count=pop(a.mask|b.mask),cost=Math.hypot(a.x,a.y)+Math.hypot(b.x,b.y)+20*(a.at+b.at);if(!best||count>best.count||count===best.count&&cost<best.cost)best={a,b,count,cost};}return[best.a,best.b].map(({mask,...f})=>f);}
function pop(n){let c=0;while(n){n&=n-1;c++;}return c;}
root.EchoModel={END,route,missiles,missilePoint,interception,contacts,plan,optimize,dodging,offsets,score};
})(typeof module==='object'?module.exports:window);

