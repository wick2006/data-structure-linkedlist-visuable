// app.js - 前端与后端 API 交互并渲染链表
// 依赖：页面设置 window.LINKLIST_BASE = "./api/" （index.html 已注入）
(function(){
  const base = (window.LINKLIST_BASE || "./api/");

  // DOM
  const el = id => document.getElementById(id);
  const btnCreate = el('btnCreate');
  const btnDestroy = el('btnDestroy');
  const btnInsertHead = el('btnInsertHead');
  const btnInsertTail = el('btnInsertTail');
  const btnInsertAt = el('btnInsertAt');
  const btnDeleteValue = el('btnDeleteValue');
  const btnDeleteAt = el('btnDeleteAt');
  const btnReverse = el('btnReverse');
  const btnSearch = el('btnSearch');
  const btnSnapshot = el('btnSnapshot');

  const initialInput = el('initialInput');
  const valueInput = el('valueInput');
  const indexInput = el('indexInput');
  const delValueInput = el('delValueInput');
  const delIndexInput = el('delIndexInput');
  const searchValueInput = el('searchValueInput');

  const currentIdEl = el('currentId');
  const currentSizeEl = el('currentSize');
  const visArea = el('visArea');
  const logArea = el('logArea');

  let currentId = null;
  let lastList = [];

  function log(msg){
    const d = document.createElement('div');
    d.textContent = `${new Date().toLocaleTimeString()}  ${msg}`;
    logArea.prepend(d);
  }

  // helper fetch JSON
  async function postJSON(path, body){
    const res = await fetch(base + path, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body || {})
    });
    return res.json();
  }
  async function getJSON(path){
    const res = await fetch(base + path);
    return res.json();
  }

  function render(list){
  const prev = lastList || [];
  visArea.innerHTML = '';

  // 辅助：比较两个数组是否相等
  const arrEqual = (a, b) => {
    if (!a || !b || a.length !== b.length) return false;
    for (let i = 0; i < a.length; ++i) if (a[i] !== b[i]) return false;
    return true;
  };

  // 计算哪些索引应当视为 'added'（新创建），哪些视为 'moved' / unchanged
  const added = new Set();
  const removed = new Set();

  if (list.length === prev.length + 1) {
    // 可能是插入（头/尾/中间）
    if (arrEqual(list.slice(1), prev)) {
      // 插入头
      added.add(0);
    } else if (arrEqual(list.slice(0, prev.length), prev)) {
      // 插入尾
      added.add(list.length - 1);
    } else {
      // 找到第一个不同的位置
      let i = 0;
      while (i < prev.length && prev[i] === list[i]) i++;
      // 检查是不是在 i 插入（新[i]，后面的元素与 prev[i..] 对齐）
      if (arrEqual(list.slice(i+1), prev.slice(i))) {
        added.add(i);
      } else {
        // 兜底：标记所有值不同的位置为 added
        for (let k=0; k<list.length; ++k) if (prev[k] === undefined || prev[k] !== list[k]) added.add(k);
      }
    }
  } else if (list.length === prev.length - 1) {
    // 可能是删除（头/尾/中间）
    if (arrEqual(prev.slice(1), list)) {
      // 删除头：标记删除 0（可以 animate 已删除效果）
      removed.add(0);
    } else if (arrEqual(prev.slice(0, list.length), list)) {
      // 删除尾
      removed.add(prev.length - 1);
    } else {
      // 找到第一个不同的位置
      let i = 0;
      while (i < list.length && list[i] === prev[i]) i++;
      if (arrEqual(prev.slice(i+1), list.slice(i))) {
        removed.add(i);
      } else {
        // 兜底：标记值不同的位置
        for (let k=0; k<prev.length; ++k) if (list[k] === undefined || prev[k] !== list[k]) removed.add(k);
      }
    }
  } else {
    // 长度相同：只把值真正不同的节点标为 added (或高亮)
    for (let k=0; k<list.length; ++k) {
      if (prev[k] === undefined || prev[k] !== list[k]) {
        added.add(k);
      }
    }
  }

  // 渲染节点（但不要把“移动”节点也当作 added）
  list.forEach((v, idx) => {
    const n = document.createElement('div');
    n.className = 'node';
    const idxSpan = document.createElement('div');
    idxSpan.className = 'idx';
    idxSpan.textContent = idx;
    const val = document.createElement('div');
    val.className = 'val';
    val.textContent = v;
    n.appendChild(idxSpan);
    n.appendChild(val);

    // 只对真正 new 的索引标记 added 动画
    if (added.has(idx)) {
      n.classList.add('added');
      setTimeout(()=> n.classList.remove('added'), 700);
    }

    // 对被删除的索引做淡出样式（它不会出现在新列表中，但我们可以作为提示）
    if (removed.has(idx)) {
      n.classList.add('removed');
      setTimeout(()=> n.remove(), 400);
    }

    visArea.appendChild(n);
  });

  // 记录并更新状态
  lastList = list.slice();
  currentSizeEl.textContent = String(list.length);
}

  // API wrappers (return updated list when appropriate)
  async function createList(initial){
    const body = {};
    if (Array.isArray(initial)) body.initial = initial;
    const data = await postJSON('create/', body);
    currentId = data.id;
    currentIdEl.textContent = currentId;
    log('已创建链表 ' + currentId);
    render(data.list || []);
  }

  async function destroyList(){
    if(!currentId) return;
    const data = await postJSON('destroy/', {id: currentId});
    if (data.ok) {
      log('已销毁链表 ' + currentId);
      currentId = null;
      currentIdEl.textContent = '—';
      render([]);
    } else {
      log('销毁失败：id 未找到');
    }
  }

  async function insertHead(val){
    if(!currentId) return alert('请先创建链表');
    const data = await postJSON('insert_head/', {id: currentId, value: Number(val)});
    log('插入头 -> ' + val);
    render(data.list || []);
  }
  async function insertTail(val){
    if(!currentId) return alert('请先创建链表');
    const data = await postJSON('insert_tail/', {id: currentId, value: Number(val)});
    log('插入尾 -> ' + val);
    render(data.list || []);
  }
  async function insertAt(idx, val){
    if(!currentId) return alert('请先创建链表');
    const data = await postJSON('insert_at/', {id: currentId, index: Number(idx), value: Number(val)});
    log(`插入位置 ${idx} -> ${val}`);
    render(data.list || []);
  }
  async function deleteValue(val){
    if(!currentId) return alert('请先创建链表');
    const data = await postJSON('delete_value/', {id: currentId, value: Number(val)});
    log(`删除值 ${val} 结果: ${data.result}`);
    render(data.list || []);
  }
  async function deleteAt(idx){
    if(!currentId) return alert('请先创建链表');
    const data = await postJSON('delete_at/', {id: currentId, index: Number(idx)});
    log(`删除索引 ${idx} 结果: ${data.ok}`);
    render(data.list || []);
  }
  async function reverseList(){
    if(!currentId) return alert('请先创建链表');
    const data = await postJSON('reverse/', {id: currentId});
    log('链表反转');
    render(data.list || []);
  }
 async function searchValue(val) {
    if (!currentId) 
        return alert('请先创建链表');

    if (val === "" || isNaN(Number(val))) 
        return alert('请输入有效的数字');

    val = Number(val);

    let res;
    try {
        res = await getJSON(
            `search/?id=${encodeURIComponent(currentId)}&value=${encodeURIComponent(val)}`
        );
    } catch (err) {
        console.error(err);
        return alert("请求搜索接口失败，请检查服务端或网络");
    }

    if (res.error) {
        log(`搜索 ${val} -> 错误：${res.error}`);
        return alert(`搜索失败：${res.error}`);
    }

    const index = res.index;

    // === 判断是否找到 ===
    if (index === -1 || index === null || index === undefined) {
        log(`搜索 ${val} -> 未找到`);
        return alert(`未找到值 ${val}（返回索引 = -1）`);
    }

    log(`搜索 ${val} -> 索引 ${index}`);
    alert(`找到值 ${val}，所在索引为：${index}`);
}

  async function snapshot(){
    if(!currentId) return alert('请先创建链表');
    const res = await getJSON(`snapshot/?id=${encodeURIComponent(currentId)}`);
    render(res.list || []);
    log('刷新快照');
  }

  // 事件绑定
  btnCreate.addEventListener('click', async ()=> {
    const v = initialInput.value.trim();
    const initial = v ? v.split(',').map(x=>Number(x.trim())).filter(x=>!isNaN(x)) : undefined;
    await createList(initial);
  });
  btnDestroy.addEventListener('click', destroyList);
  btnInsertHead.addEventListener('click', ()=> insertHead(valueInput.value.trim()));
  btnInsertTail.addEventListener('click', ()=> insertTail(valueInput.value.trim()));
  btnInsertAt.addEventListener('click', ()=> {
    insertAt(indexInput.value.trim(), valueInput.value.trim());
  });
  btnDeleteValue.addEventListener('click', ()=> deleteValue(delValueInput.value.trim()));
  btnDeleteAt.addEventListener('click', ()=> deleteAt(delIndexInput.value.trim()));
  btnReverse.addEventListener('click', reverseList);
  btnSearch.addEventListener('click', ()=> searchValue(searchValueInput.value.trim()));
  btnSnapshot.addEventListener('click', snapshot);

  // 页面加载时可选自动创建一个空链表
  window.addEventListener('load', ()=> {
    // nothing
  });

})();
