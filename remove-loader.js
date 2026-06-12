const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// remove premium loader HTML
content = content.replace(/<div id="premium-loader">[\s\S]*?<\/div><!-- \/premium-loader -->\n?/g, '');

// remove premium loader CSS
content = content.replace(/#premium-loader \{[\s\S]*?#premium-loader\.done \{[\s\S]*?\}\n?/g, '');

// remove updateLoader done call
content = content.replace(/if \(loaded >= TOTAL\) \{\s*document\.getElementById\('premium-loader'\)\.classList\.add\('done'\);\s*\}/g, '');

fs.writeFileSync('index.html', content);
console.log('Removed premium loader');
