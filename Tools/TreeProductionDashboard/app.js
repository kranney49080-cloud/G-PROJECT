const defaultAssets = [
  {id:'standing', icon:'🌳', title:'Standing Hero Tree', purpose:'Master trunk + major branch design', unlocks:'Unlocks scale, silhouette, palette, pivots and all derived states.', status:'in-progress', core:true},
  {id:'oblique', icon:'🔄', title:'Oblique / Side View', purpose:'Depth reference for the trunk and major branches', unlocks:'Unlocks hybrid / 3D construction and believable thickness.', status:'waiting', core:true},
  {id:'felled', icon:'🪓', title:'Cut / Felled Tree', purpose:'Falling and post-cut visual state', unlocks:'Unlocks the harvesting transition and simplified falling asset.', status:'waiting', core:true},
  {id:'stump', icon:'🪵', title:'Stump', purpose:'Persistent post-harvest world state', unlocks:'Unlocks regrowth, stump collision and harvested-state continuity.', status:'waiting', core:true},
  {id:'cutsurface', icon:'🟠', title:'Cut Surface', purpose:'Painterly fresh-cut cross section', unlocks:'Unlocks stump top and felled-trunk cut-face consistency.', status:'waiting', core:true},
  {id:'localcanopy', icon:'🍃', title:'Local Canopy', purpose:'Tree-owned branch / leaf cards', unlocks:'Removes with the tree to create a believable canopy opening.', status:'locked', core:false},
  {id:'sharedcanopy', icon:'🌲', title:'Shared Forest Canopy', purpose:'Large overhead 2.5D canopy layers', unlocks:'Builds the forest ceiling while remaining independent of one tree.', status:'locked', core:false},
  {id:'logs', icon:'🪵', title:'Harvested Logs', purpose:'Optional physical wood resource pieces', unlocks:'Use only if harvested wood exists physically in the world.', status:'optional', core:false},
  {id:'damage', icon:'⚔️', title:'Chop Damage Marks', purpose:'Axe marks and progressive damage feedback', unlocks:'Polish layer after the base harvest loop works.', status:'optional', core:false}
];

const statuses = ['in-progress','waiting','locked','complete','optional'];
const labels = { 'in-progress':'In progress', waiting:'Waiting', locked:'Locked', complete:'Complete', optional:'Optional' };
const key = 'treeProductionBoard.v1';

function loadState(){
  try { return JSON.parse(localStorage.getItem(key)) || {}; }
  catch { return {}; }
}

let state = loadState();
if(!state.assets) state.assets = structuredClone(defaultAssets);
if(typeof state.notes !== 'string') state.notes = '';

const grid = document.querySelector('#assetGrid');
const template = document.querySelector('#assetTemplate');
const progressBar = document.querySelector('#progressBar');
const progressText = document.querySelector('#progressText');
const currentMilestone = document.querySelector('#currentMilestone');
const notes = document.querySelector('#notes');
const saveState = document.querySelector('#saveState');

function save(){
  localStorage.setItem(key, JSON.stringify(state));
  saveState.textContent = 'Saved locally';
}

function nextMilestone(){
  const core = state.assets.filter(a=>a.core);
  const next = core.find(a=>a.status !== 'complete');
  return next ? `Finish: ${next.title}` : 'Core tree asset set complete';
}

function render(){
  grid.innerHTML='';
  for(const asset of state.assets){
    const node = template.content.firstElementChild.cloneNode(true);
    node.querySelector('.asset-icon').textContent = asset.icon;
    node.querySelector('.asset-title').textContent = asset.title;
    node.querySelector('.asset-purpose').textContent = asset.purpose;
    node.querySelector('.asset-unlocks').textContent = asset.unlocks;
    const badge = node.querySelector('.status-badge');
    badge.textContent = labels[asset.status];
    badge.className = `status-badge status-${asset.status}`;

    node.querySelector('.status-cycle').addEventListener('click', ()=>{
      const i = statuses.indexOf(asset.status);
      asset.status = statuses[(i+1)%statuses.length];
      save(); render();
    });
    node.querySelector('.approve').addEventListener('click', ()=>{
      asset.status='complete';
      save(); render();
    });
    grid.appendChild(node);
  }

  const core = state.assets.filter(a=>a.core);
  const done = core.filter(a=>a.status==='complete').length;
  progressText.textContent = `${done} / ${core.length}`;
  progressBar.style.width = `${(done/core.length)*100}%`;
  currentMilestone.textContent = nextMilestone();
}

notes.value = state.notes;
let timer;
notes.addEventListener('input',()=>{
  state.notes = notes.value;
  saveState.textContent = 'Saving…';
  clearTimeout(timer);
  timer=setTimeout(save,250);
});

document.querySelector('#resetBtn').addEventListener('click',()=>{
  if(!confirm('Reset all tree-board statuses and notes?')) return;
  state = {assets: structuredClone(defaultAssets), notes:''};
  notes.value='';
  save(); render();
});

render();
