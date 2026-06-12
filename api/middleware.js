
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
