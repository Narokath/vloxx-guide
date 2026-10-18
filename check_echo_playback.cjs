const fs=require('fs'),vm=require('vm'),assert=require('assert'),{EchoModel:M}=require('./echo-model.js');
const els={};function $(id){return els[id]??={value:'',innerHTML:'',textContent:'',style:{}};}
let rangeValue='0';Object.defineProperty($('echo-time'),'value',{get:()=>rangeValue,set:v=>{rangeValue=String(Math.round(Math.max(0,Math.min(18,Number(v)))/.05)*.05);}});
const defaults={'echo-route':'orbit','echo-fix-route':'move','echo-first':'0','echo-radius':'90','echo-speed':'200','echo-rate':'1','echo-field-1':'cpc','echo-field-2':'feedback','echo-x-1':'0','echo-x-2':'0','echo-y-1':'-200','echo-y-2':'0','echo-at-1':'.5','echo-at-2':'3'};for(const [id,v] of Object.entries(defaults))$(id).value=v;
let now=0,next=1;const queue=new Map(),ctx={window:{EchoModel:M},document:{getElementById:$,body:{dataset:{mode:'CM'}}},performance:{now:()=>now},requestAnimationFrame:fn=>{const id=next++;queue.set(id,fn);return id;},cancelAnimationFrame:id=>queue.delete(id)};
vm.runInNewContext(fs.readFileSync('echo-controller.js','utf8'),ctx);
function step(ms){now+=ms;const tasks=[...queue.values()];queue.clear();for(const f of tasks)f(now);}
for(const [mode,fps,rate] of [['CM',60,1],['CM',144,.5],['LCM',144,1],['LCM',60,.5]]){
 ctx.document.body.dataset.mode=mode;ctx.window.refreshEcho();$('echo-reset').onclick();$('echo-rate').value=String(rate);const before=$('echo-map').innerHTML;$('echo-play').onclick();
 for(let i=0;i<fps;i++)step(1000/fps);
 assert(Math.abs(+$('echo-time').value-rate)<.06,`${mode} ${fps}fps ${rate}x stalled`);assert.notEqual($('echo-map').innerHTML,before);assert.equal($('echo-play').textContent,'Pause');
 $('echo-play').onclick();const paused=$('echo-time').value;step(1000);assert.equal($('echo-time').value,paused);assert.equal(queue.size,0);
 $('echo-play').onclick();step(200);assert(+$('echo-time').value>+paused);step(40000);assert.equal(+$('echo-time').value,18);assert.equal($('echo-play').textContent,'Play');assert.equal(queue.size,0);
 $('echo-play').onclick();step(200);assert(+$('echo-time').value<1);$('echo-reset').onclick();assert.equal(+$('echo-time').value,0);assert.equal(queue.size,0);
 $('echo-time').value=4;$('echo-time').oninput();$('echo-play').onclick();step(200);assert(+$('echo-time').value>4);$('echo-play').onclick();
}
console.log('PASS: quantised range regression at 60/144fps, CM/LCM, normal/half speed; animation changes, pause/resume, end, replay, reset and scrub.');
