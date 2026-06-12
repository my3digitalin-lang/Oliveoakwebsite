const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// remove premium loader HTML
content = content.replace(/<div id="premium-loader">[\s\S]*?<div id="loader-pct"[^>]*>0%<\/div>\s*<\/div>\s*<\/div>/, '');

// remove premium loader CSS
content = content.replace(/#premium-loader \{[\s\S]*?#premium-loader\.done \{[\s\S]*?\}\n/g, '');

// also remove the CSS for .loader-content down to .loader-pct
content = content.replace(/\.loader-content \{[\s\S]*?\.loader-pct \{[\s\S]*?\}\n/g, '');

// remove updateLoader done call
content = content.replace(/if \(loaded >= TOTAL\) \{\s*document\.getElementById\('premium-loader'\)\.classList\.add\('done'\);\s*\}/g, '');

// Wait, the user said "remove that loading interface at the start"
// Does he mean the entire load wait? Or just the premium loader?
// If we just remove it, it's fine. 

fs.writeFileSync('index.html', content);
console.log('Removed premium loader completely');
