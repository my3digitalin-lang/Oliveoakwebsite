
// api/contacts.js
// Stores client enquiries submitted from the public website into data/contacts.json (in GitHub).
//  - POST  : PUBLIC (anyone on the site can submit a contact form)
//  - GET    : ADMIN ONLY (list leads in the dashboard)
//  - DELETE : ADMIN ONLY (remove a lead by id)
const { getFileContent, updateFileContent } = require('./github');

const SECRET_TOKEN = process.env.GITHUB_TOKEN ? process.env.GITHUB_TOKEN.substring(0, 15) : 'dev-secret-token';

function isAuthed(req) {
  const authHeader = req.headers.authorization || '';
  if (!authHeader.startsWith('Bearer ')) return false;
  const token = authHeader.split(' ')[1];
  return token === `oo-auth-${SECRET_TOKEN}`;
}

function clean(v, max = 500) {
  if (v === undefined || v === null) return '';
  return String(v).trim().slice(0, max);
}

module.exports = async function handler(req, res) {
  const filePath = 'data/contacts.json';

  // ---- Public submission ----
  if (req.method === 'POST') {
    const body = req.body || {};

    // Honeypot: bots fill hidden fields. Silently accept & drop.
    if (clean(body.company)) return res.status(201).json({ success: true });

    const name = clean(body.name, 120);
    const phone = clean(body.phone, 40);
    const email = clean(body.email, 160);
    if (!name || (!phone && !email)) {
      return res.status(400).json({ error: 'Name and a phone or email are required.' });
    }

    const lead = {
      id: Date.now().toString(),
      name,
      phone,
      email,
      service: clean(body.service, 80),
      budget: clean(body.budget, 80),
      message: clean(body.message, 2000),
      source: clean(body.source, 120) || 'website',
      createdAt: new Date().toISOString()
    };

    try {
      const { content, sha } = await getFileContent(filePath);
      const list = Array.isArray(content) ? content : [];
      list.push(lead);
      await updateFileContent(filePath, JSON.stringify(list, null, 2), `Lead: ${name}`, sha);
      return res.status(201).json({ success: true });
    } catch (e) {
      console.error('Contact save error:', e);
      return res.status(500).json({ error: 'Could not save enquiry.' });
    }
  }

  // ---- Admin-only below ----
  if (!isAuthed(req)) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  if (req.method === 'GET') {
    const { content } = await getFileContent(filePath);
    return res.status(200).json(Array.isArray(content) ? content : []);
  }

  if (req.method === 'PUT') {
    const body = req.body || {};
    if (!body.id) return res.status(400).json({ error: 'Missing id' });
    const { content, sha } = await getFileContent(filePath);
    const list = Array.isArray(content) ? content : [];
    const idx = list.findIndex(c => c.id === body.id);
    if (idx === -1) return res.status(404).json({ error: 'Lead not found' });
    // Only allow updating known fields
    if (body.stage !== undefined) list[idx].stage = clean(body.stage, 40);
    if (body.notes !== undefined) list[idx].notes = clean(body.notes, 4000);
    if (body.lastContactedAt !== undefined) list[idx].lastContactedAt = clean(body.lastContactedAt, 40);
    try {
      await updateFileContent(filePath, JSON.stringify(list, null, 2), `Lead: ${list[idx].name} -> ${list[idx].stage}`, sha);
      return res.status(200).json(list[idx]);
    } catch (e) {
      console.error('Lead update error:', e);
      return res.status(500).json({ error: 'Could not update lead.' });
    }
  }

  if (req.method === 'DELETE') {
    const { id } = req.query;
    if (!id) return res.status(400).json({ error: 'Missing id' });
    const { content, sha } = await getFileContent(filePath);
    const list = (Array.isArray(content) ? content : []).filter(c => c.id !== id);
    await updateFileContent(filePath, JSON.stringify(list, null, 2), `Lead: delete ${id}`, sha);
    return res.status(200).json({ success: true });
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
};
