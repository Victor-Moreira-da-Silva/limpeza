import {readFileSync} from 'node:fs';
for(const f of ['frontend/index.html','frontend/src/app.js','frontend/src/style.css']){if(!readFileSync(f,'utf8').trim())throw Error(f+' vazio');console.log('ok '+f)}
