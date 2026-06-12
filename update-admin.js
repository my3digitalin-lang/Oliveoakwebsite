const fs = require('fs');

// Read as buffer then detect encoding issues
let html = fs.readFileSync('admin-base.html', 'utf8');

// ===== FIX ALL THE GARBLED EMOJI/TEXT =====
// The garbled sequences come from UTF-8 emoji being misread

// Fix button text in HTML
html = html.replace(/dYs\? Publish to Projects Page/g, '🚀 Publish to Projects Page');
html = html.replace(/dYs\? Publish to Blog Page/g, '🚀 Publish to Blog Page');

// Fix success/error messages in JS strings
html = html.replace(/['"].*?Published!.*?['"]/g, (m) => m.replace(/[^\x20-\x7E'",]/g, '').trim());

// Fix all the garbled toast messages with clean versions
html = html.replace(/showToast\('[^']*Fill in at least[^']*'\)/g, "showToast('❌ Fill in at least Project Name and Description.')");
html = html.replace(/showToast\('[^']*Fill in the Blog[^']*'\)/g, "showToast('❌ Fill in the Blog Title first.')");
html = html.replace(/showToast\('[^']*Project published[^']*'\)/g, "showToast('✅ Project published! It will appear on the Projects page within seconds.')");
html = html.replace(/showToast\('[^']*Blog published[^']*'\)/g, "showToast('✅ Blog published! It will appear on the Blog page within seconds.')");
html = html.replace(/showToast\('[^']*Project deleted[^']*'\)/g, "showToast('✅ Project deleted successfully!')");
html = html.replace(/showToast\('[^']*Firebase not configured[^']*'\)/g, "showToast('❌ Firebase not configured. Please add your credentials to firebase-config.js')");

// Fix the btn textContent in JS  
html = html.replace(/btn\.textContent = '[^']*Published![^']*'/g, "btn.textContent = '✅ Published!'");
html = html.replace(/btn\.textContent = '(dYs\?|🚀)? ?Publish to Projects Page'/g, "btn.textContent = '🚀 Publish to Projects Page'");
html = html.replace(/btn\.textContent = '(dYs\?|🚀)? ?Publish to Blog Page'/g, "btn.textContent = '🚀 Publish to Blog Page'");
html = html.replace(/btn\.textContent = 'Publishing\.\.\.'/g, "btn.textContent = 'Publishing...'");

// Fix the toast default text
html = html.replace(/<div id="toast">[^<]*<\/div>/g, '<div id="toast"></div>');

// ===== FIX PUBLISH PROJECT FUNCTION =====
// Change event.target to event.currentTarget so it always gets the button
html = html.replace(
  'const btn = event.target;\n    btn.textContent = \'Publishing...\';\n    btn.disabled = true;',
  "const btn = event.currentTarget || event.target;\n    btn.textContent = 'Publishing...';\n    btn.disabled = true;"
);

// ===== REMOVE DUPLICATE MANAGE PANEL =====
// Keep only the first occurrence of panel-manage
const firstIdx = html.indexOf('id="panel-manage"');
const secondIdx = html.indexOf('id="panel-manage"', firstIdx + 1);
if (secondIdx !== -1) {
  // Find the closing tag of the second panel
  const closeTag = '</div><!-- end manage panel -->';
  const closeIdx = html.indexOf(closeTag, secondIdx);
  if (closeIdx !== -1) {
    html = html.slice(0, html.lastIndexOf('<!-- ====== MANAGE TAB', secondIdx - 100)) + html.slice(closeIdx + closeTag.length);
  }
}

// ===== FIX: Rename custom alert function to showToast =====
// The existing code already uses showToast - just make sure alert() isn't overridden
html = html.replace(/function alert\(msg\)/g, 'function showToast(msg)');
// Make sure all alert( calls use showToast(
html = html.replace(/\balert\(/g, 'showToast(');

// ===== FIX DELETE FUNCTION =====
// Replace existing deleteProject with a fixed version  
const oldDeleteRegex = /async function deleteProject\(docId(?:, btnEl)?\) \{[\s\S]*?\n  \}/;
const newDelete = `async function deleteProject(docId, btnEl) {
    if (btnEl) { btnEl.textContent = 'Deleting...'; btnEl.disabled = true; }
    try {
      await db.collection('projects').doc(docId).delete();
      showToast('✅ Project deleted successfully!');
      setTimeout(() => loadManageData(), 1000);
    } catch(e) {
      console.error(e);
      showToast('❌ Delete failed: ' + e.message);
      if (btnEl) { btnEl.textContent = 'Delete'; btnEl.disabled = false; }
    }
  }`;
html = html.replace(oldDeleteRegex, newDelete);

// ===== FIX MANAGE PANEL DELETE BUTTON =====
// Ensure delete buttons pass 'this'
html = html.replace(/onclick="deleteProject\('\$\{doc\.id\}'\)"/g, "onclick=\"deleteProject('${doc.id}', this)\"");

// ===== ADD MANAGE TAB BUTTON if missing =====
if (!html.includes('id="tab-manage"')) {
  html = html.replace(
    /<button class="tab-btn" id="tab-project" onclick="switchTab\('project'\)">.*?<\/button>/,
    (m) => m + '\n      <button class="tab-btn" id="tab-manage" onclick="switchTab(\'manage\')">🗑️ Manage Projects</button>'
  );
}

// ===== ADD MANAGE PANEL if missing =====
if (!html.includes('panel-manage')) {
  html = html.replace('</div><!-- end project panel -->', `</div><!-- end project panel -->

    <!-- ====== MANAGE TAB ====== -->
    <div id="panel-manage" style="display:none;">
      <div style="max-width:900px;">
        <div class="form-card">
          <div class="form-card-title">🗑️ Manage Live Projects</div>
          <p style="color:rgba(248,243,234,.5);font-size:14px;margin-bottom:20px;">View and remove projects currently on the database.</p>
          <div id="manage-project-list" style="display:flex;flex-direction:column;gap:12px;">
            <p>Loading projects...</p>
          </div>
        </div>
      </div>
    </div><!-- end manage panel -->`);
}

// ===== UPDATE switchTab to handle manage tab =====
html = html.replace(
  /function switchTab\(t\) \{[\s\S]*?document\.getElementById\('tab-' \+ t\)\.classList\.add\('active'\);\s*\}/,
  `function switchTab(t) {
    document.getElementById('panel-blog').style.display = t === 'blog' ? 'block' : 'none';
    document.getElementById('panel-project').style.display = t === 'project' ? 'block' : 'none';
    const managePanel = document.getElementById('panel-manage');
    if (managePanel) managePanel.style.display = t === 'manage' ? 'block' : 'none';
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('tab-' + t).classList.add('active');
    if (t === 'manage') loadManageData();
  }`
);

// ===== ADD loadManageData function if missing =====
if (!html.includes('function loadManageData')) {
  const manageScripts = `
  async function loadManageData() {
    if (!initFirebase()) return;
    const list = document.getElementById('manage-project-list');
    list.innerHTML = '<p style="color:rgba(248,243,234,.5)">Loading...</p>';
    try {
      const snap = await db.collection('projects').orderBy('createdAt', 'desc').get();
      if (snap.empty) { list.innerHTML = '<p>No projects found.</p>'; return; }
      let out = '';
      snap.forEach(doc => {
        const d = doc.data();
        out += \`<div style="display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,.03);padding:16px;border-radius:12px;border:1px solid rgba(200,169,126,.1);">
          <div><strong style="font-size:15px;color:#f8f3ea;display:block;">\${d.name || 'Untitled'}</strong>
          <span style="font-size:12px;color:rgba(248,243,234,.5);">Category: \${d.category||'N/A'} | Year: \${d.year||'N/A'}</span></div>
          <button onclick="deleteProject('\${doc.id}', this)" style="background:#c0392b;border:none;color:#fff;padding:8px 18px;border-radius:8px;cursor:pointer;font-size:13px;">Delete</button>
        </div>\`;
      });
      list.innerHTML = out;
    } catch(e) { console.error(e); list.innerHTML = '<p style="color:#e74c3c;">Error: ' + e.message + '</p>'; }
  }`;
  html = html.replace('</script>\n</body>', manageScripts + '\n</script>\n</body>');
}

fs.writeFileSync('admin.html', html, 'utf8');
console.log('admin.html fully rebuilt and fixed!');
console.log('Checking: publish button text =', html.includes('🚀 Publish to Projects Page') ? 'OK' : 'MISSING');
console.log('Checking: manage tab =', html.includes('tab-manage') ? 'OK' : 'MISSING');
console.log('Checking: loadManageData =', html.includes('loadManageData') ? 'OK' : 'MISSING');
console.log('Checking: deleteProject =', html.includes('deleteProject') ? 'OK' : 'MISSING');
