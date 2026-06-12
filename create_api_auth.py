import os

auth_js = """
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
"""

middleware_js = """
// api/middleware.js
const SECRET_TOKEN = process.env.GITHUB_TOKEN ? process.env.GITHUB_TOKEN.substring(0, 15) : 'dev-secret-token';

function requireAuth(handler) {
  return async (req, res) => {
    // Only check auth for POST/PUT/DELETE
    if (req.method === 'GET') {
      return handler(req, res);
    }

    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'Unauthorized: Missing token' });
    }

    const token = authHeader.split(' ')[1];
    const expectedToken = `oo-auth-${SECRET_TOKEN}`;

    if (token !== expectedToken) {
      return res.status(403).json({ error: 'Forbidden: Invalid token' });
    }

    // Authorized
    return handler(req, res);
  };
}

module.exports = requireAuth;
"""

with open(r'c:\tmp\Oliveoakk\api\auth.js', 'w', encoding='utf-8') as f:
    f.write(auth_js)
    
with open(r'c:\tmp\Oliveoakk\api\middleware.js', 'w', encoding='utf-8') as f:
    f.write(middleware_js)

print("Created api/auth.js and api/middleware.js")
