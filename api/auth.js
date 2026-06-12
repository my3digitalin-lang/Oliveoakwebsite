
// api/auth.js
// A simple login handler that checks password and returns a dummy "token"
// For a simple static site CMS, we can use a basic symmetric token since it runs securely in Vercel.

const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD;
const SECRET_TOKEN = process.env.GITHUB_TOKEN ? process.env.GITHUB_TOKEN.substring(0, 15) : 'dev-secret-token';

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { password } = req.body || {};

  if (!ADMIN_PASSWORD) {
    return res.status(500).json({ error: 'ADMIN_PASSWORD not configured on server.' });
  }

  if (password === ADMIN_PASSWORD) {
    // Return a simple pseudo-token that middleware can verify
    // In production, you'd use a real JWT library, but we'll use a static derived token for simplicity
    const token = `oo-auth-${SECRET_TOKEN}`;
    return res.status(200).json({ token });
  }

  return res.status(401).json({ error: 'Invalid password' });
};
