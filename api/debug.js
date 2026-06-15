module.exports = async function handler(req, res) {
  const token = process.env.GITHUB_TOKEN;
  const repo = process.env.GITHUB_REPO;
  const pass = process.env.ADMIN_PASSWORD;

  // Test the GitHub API connection
  let githubStatus = 'not tested';
  let githubError = null;
  
  if (token && repo) {
    try {
      const response = await fetch(`https://api.github.com/repos/${repo}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/vnd.github.v3+json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        githubStatus = `Connected! Repo: ${data.full_name}, Private: ${data.private}`;
      } else {
        const errText = await response.text();
        githubStatus = `Error ${response.status}`;
        githubError = errText;
      }
    } catch (e) {
      githubStatus = 'Connection failed';
      githubError = e.message;
    }
  }

  res.json({
    hasToken: !!token,
    tokenPrefix: token ? token.substring(0, 8) + '...' : 'MISSING',
    repo: repo || 'MISSING',
    hasPassword: !!pass,
    githubStatus,
    githubError
  });
};
