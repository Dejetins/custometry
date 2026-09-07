// Preserve installed dependency notices in the shipped Web artifact.
// This includes build dependencies; it is not a license-policy acceptance gate.
import { readdir, readFile, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const sections = [];
async function packageNotice(directory) {
  let metadata;
  try { metadata = JSON.parse(await readFile(path.join(directory, 'package.json'), 'utf8')); }
  catch (error) { if (error.code === 'ENOENT') return; throw error; }
  const entries = await readdir(directory, { withFileTypes: true });
  const names = entries.filter(entry => entry.isFile() && /^(licen[cs]e|copying|notice)([.-]|$)/i.test(entry.name))
    .map(entry => entry.name).sort();
  const texts = await Promise.all(names.map(async name => `${name}\n${await readFile(path.join(directory, name), 'utf8')}`));
  sections.push(`${metadata.name}@${metadata.version}\nDeclared license: ${JSON.stringify(metadata.license ?? 'UNKNOWN')}\n${texts.join('\n\n') || 'No root license text found; review required.'}`);
}

for (const item of (await readdir('node_modules/.pnpm', { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name, 'en'))) {
  if (!item.isDirectory() || item.name === 'node_modules') continue;
  const directory = path.join('node_modules/.pnpm', item.name, 'node_modules');
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue; // Symlinks refer to another inventoried package.
    const target = path.join(directory, entry.name);
    if (entry.name.startsWith('@')) {
      for (const child of await readdir(target, { withFileTypes: true })) {
        if (child.isDirectory()) await packageNotice(path.join(target, child.name));
      }
    } else await packageNotice(target);
  }
}
if (!sections.length) throw new Error('No dependency notices collected');
await mkdir('apps/web/dist/notices', { recursive: true });
await writeFile('apps/web/dist/notices/THIRD-PARTY.txt', sections.sort().join('\n\n---\n\n') + '\n');
