
const { getFileContent, updateFileContent } = require('./github');
const requireAuth = require('./middleware');

async function handler(req, res) {
  const filePath = 'data/blogs.json';

  try {
  if (req.method === 'GET') {
    const { content } = await getFileContent(filePath);
    return res.status(200).json(content);
  }

  if (req.method === 'POST') {
    const newBlog = req.body;
    if (!newBlog.title || !newBlog.slug) return res.status(400).json({ error: 'Missing title or slug' });
    
    newBlog.id = newBlog.id || Date.now().toString();
    newBlog.createdAt = newBlog.createdAt || new Date().toISOString();
    newBlog.updatedAt = new Date().toISOString();

    const { content, sha } = await getFileContent(filePath);
    content.push(newBlog);

    await updateFileContent(filePath, JSON.stringify(content, null, 2), `CMS: Create blog ${newBlog.slug}`, sha);
    return res.status(201).json(newBlog);
  }

  if (req.method === 'PUT') {
    const updatedBlog = req.body;
    if (!updatedBlog.id) return res.status(400).json({ error: 'Missing id' });

    const { content, sha } = await getFileContent(filePath);
    const idx = content.findIndex(b => b.id === updatedBlog.id);
    if (idx === -1) return res.status(404).json({ error: 'Blog not found' });

    updatedBlog.updatedAt = new Date().toISOString();
    content[idx] = { ...content[idx], ...updatedBlog };

    await updateFileContent(filePath, JSON.stringify(content, null, 2), `CMS: Update blog ${updatedBlog.slug}`, sha);
    return res.status(200).json(content[idx]);
  }

  if (req.method === 'DELETE') {
    const { id } = req.query;
    if (!id) return res.status(400).json({ error: 'Missing id' });

    const { content, sha } = await getFileContent(filePath);
    const newContent = content.filter(b => b.id !== id);

    await updateFileContent(filePath, JSON.stringify(newContent, null, 2), `CMS: Delete blog ${id}`, sha);
    return res.status(200).json({ success: true });
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
  } catch (e) {
    console.error('Blogs handler error:', e);
    return res.status(500).json({ error: e.message || 'Server error saving blog' });
  }
}

module.exports = requireAuth(handler);
