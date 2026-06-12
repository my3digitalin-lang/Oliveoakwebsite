
const { uploadFileBinary, getFileSha, deleteFile } = require('./github');
const requireAuth = require('./middleware');

// We need to accept large payloads for images (default Vercel limit is 4.5MB which is fine since we cap at 2MB client-side)
// We will set body size limit in vercel.json if needed, but standard limit is enough.

async function handler(req, res) {
  if (req.method === 'POST') {
    // Expected body: { type: 'project' | 'blog', filename: 'image.webp', base64: 'UklGRi...' }
    const { type, filename, base64 } = req.body;
    
    if (!type || !filename || !base64) {
      return res.status(400).json({ error: 'Missing type, filename, or base64 data' });
    }

    const folder = type === 'project' ? 'projects' : 'blogs';
    const filePath = `public/uploads/${folder}/${filename}`;

    try {
      // Check if file already exists to get its SHA (to overwrite if necessary)
      const existingSha = await getFileSha(filePath);

      await uploadFileBinary(filePath, base64, `CMS: Upload image ${filename}`, existingSha);
      
      return res.status(200).json({ url: `/${filePath}` });
    } catch (e) {
      return res.status(500).json({ error: e.message });
    }
  }
  
  if (req.method === 'DELETE') {
    // Expected body: { filePath: 'public/uploads/projects/image.webp' }
    const { filePath } = req.body;
    if (!filePath || !filePath.startsWith('public/uploads/')) {
      return res.status(400).json({ error: 'Invalid file path' });
    }
    try {
      const sha = await getFileSha(filePath);
      if (sha) {
        await deleteFile(filePath, `CMS: Delete image ${filePath}`, sha);
      }
      return res.status(200).json({ success: true });
    } catch (e) {
      return res.status(500).json({ error: e.message });
    }
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
}

// Next.js/Vercel config to allow larger payloads
module.exports = requireAuth(handler);
module.exports.config = {
  api: {
    bodyParser: {
      sizeLimit: '4mb',
    },
  },
};
