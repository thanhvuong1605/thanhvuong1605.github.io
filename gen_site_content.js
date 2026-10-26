#!/usr/bin/env node
// Generate site_content.txt (context for the CV AI agent at /opt/cv-ai/) from
// the `commands` object in script.js, so the agent's knowledge never drifts
// from what the website actually shows. Run by deploy.sh; output goes to stdout.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const src = fs.readFileSync(path.join(__dirname, 'script.js'), 'utf8');
const start = src.indexOf('const commands = {');
const end = src.indexOf('\n};', start);
if (start === -1 || end === -1) {
    console.error('gen_site_content: could not locate `const commands = {...};` in script.js');
    process.exit(1);
}

const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(src.slice(start, end + 3) + '\nthis.__commands = commands;', sandbox);
const commands = sandbox.__commands;

function strip(html) {
    return html
        .replace(/<[^>]+>/g, ' ')
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&nbsp;/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
}

let out = '// Website commands and their text content. Auto-generated from script.js by gen_site_content.js — DO NOT EDIT BY HAND.\n\n';
for (const [name, html] of Object.entries(commands)) {
    out += name + ': ` ' + strip(html) + ' `\n\n';
}
process.stdout.write(out);
