import os

github_js = """
// Utility to interact with GitHub REST API
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_REPO = process.env.GITHUB_REPO; // format: owner/repo

async function githubRequest(path, method = 'GET', body = null) {
  const url = `https://api.github.com/repos/${GITHUB_REPO}${path}`;
  const options = {
    method,
    headers: {
      'Authorization': `Bearer ${GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'Content-Type': 'application/json'
    }
  };
  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);
  if (!response.ok) {
    const err = await response.text();
    console.error('GitHub API Error:', url, response.status, err);
    throw new Error(`GitHub API Error: ${response.statusText}`);
  }
  return response.json();
}

async function getFileContent(filePath) {
  try {
    const data = await githubRequest(`/contents/${filePath}`);
    const content = Buffer.from(data.content, 'base64').toString('utf8');
    return { content: JSON.parse(content), sha: data.sha };
  } catch (error) {
    console.warn(`File ${filePath} not found or error, returning empty.`);
    return { content: [], sha: null };
  }
}

async function updateFileContent(filePath, contentStr, message, sha = null) {
  const body = {
    message: message,
    content: Buffer.from(contentStr, 'utf8').toString('base64')
  };
  if (sha) {
    body.sha = sha;
  }
  return await githubRequest(`/contents/${filePath}`, 'PUT', body);
}

async function uploadFileBinary(filePath, base64Content, message, sha = null) {
  const body = {
    message: message,
    content: base64Content // expects pure base64 string without data:image/xxx;base64, prefix
  };
  if (sha) {
    body.sha = sha;
  }
  return await githubRequest(`/contents/${filePath}`, 'PUT', body);
}

async function deleteFile(filePath, message, sha) {
  if (!sha) return null;
  return await githubRequest(`/contents/${filePath}`, 'DELETE', {
    message: message,
    sha: sha
  });
}

async function getFileSha(filePath) {
  try {
    const data = await githubRequest(`/contents/${filePath}`);
    return data.sha;
  } catch (e) {
    return null;
  }
}

module.exports = {
  getFileContent,
  updateFileContent,
  uploadFileBinary,
  deleteFile,
  getFileSha
};
"""

with open(r'c:\tmp\Oliveoakk\api\github.js', 'w', encoding='utf-8') as f:
    f.write(github_js)
    
print("Created api/github.js")
