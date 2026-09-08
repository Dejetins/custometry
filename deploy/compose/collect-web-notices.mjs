// Preserve notices for the dependencies in the actual emitted Rollup graph.
import { createHash } from 'node:crypto';
import { readdir, readFile, realpath, writeFile } from 'node:fs/promises';
import path from 'node:path';

const sha256 = value => createHash('sha256').update(value).digest('hex');
const root = await realpath('.');
async function sourcePath(relative) {
  if (path.isAbsolute(relative) || relative.split('/').includes('..')) throw new Error('Unsafe inventory path');
  const actual = await realpath(relative);
  if (!actual.startsWith(root + path.sep)) throw new Error('Inventory escapes source');
  return actual;
}
const inventory = JSON.parse(await readFile('apps/web/dist/notices/runtime-modules.json', 'utf8'));
if (inventory.schema_version !== 1 || !inventory.packages?.length || !inventory.modules?.length) throw new Error('Missing runtime module inventory');
const packageRoots = new Set(inventory.packages.map(item => item.root));
const modulePackages = new Set(inventory.modules.map(item => item.package).filter(item => item !== null));
if (packageRoots.size !== inventory.packages.length || packageRoots.size !== modulePackages.size || [...modulePackages].some(item => !packageRoots.has(item))) throw new Error('Incomplete package coverage');
if (!Object.keys(inventory.chunks).length) throw new Error('Empty chunk inventory');
for (const module of inventory.modules) {
  if (!module.chunks?.length || module.chunks.some(name => !(name in inventory.chunks))) throw new Error('Missing module chunk');
  if (sha256(await readFile(await sourcePath(module.path))) !== module.sha256) throw new Error('Bundled source changed');
}
for (const [name, digest] of Object.entries(inventory.chunks)) {
  if (sha256(await readFile(await sourcePath('apps/web/dist/' + name))) !== digest) throw new Error('Emitted chunk changed');
}
const owned = new Map([
  ['apps/web', '@custometry/web'], ['packages/contracts', '@custometry/contracts'],
  ['packages/localization', '@custometry/localization'], ['packages/ui-foundation', '@custometry/ui-foundation'],
]);
const sections = [];
const packages = [];
for (const item of inventory.packages) {
  const directory = await sourcePath(item.root);
  const raw = await readFile(path.join(directory, 'package.json'));
  const metadata = JSON.parse(raw);
  if (sha256(raw) !== item.metadata_sha256 || metadata.name !== item.name || metadata.version !== item.version) throw new Error('Package identity changed');
  const firstParty = owned.get(item.root) === item.name;
  const names = firstParty ? ['LICENSE'] : (await readdir(directory, { withFileTypes: true }))
    .filter(entry => entry.isFile() && /^(licen[cs]e|copying|notice)([.-]|$)/i.test(entry.name))
    .map(entry => entry.name).sort();
  const notices = [];
  const texts = [];
  for (const name of names) {
    const filename = firstParty ? 'LICENSE' : item.root + '/' + name;
    const data = await readFile(await sourcePath(filename));
    if (!data.length) throw new Error('Empty dependency notice');
    notices.push({ path: filename, sha256: sha256(data), size_bytes: data.length });
    texts.push(name + '\n' + data.toString('utf8'));
  }
  const license = firstParty ? 'Apache-2.0' : (metadata.license ?? 'UNKNOWN');
  sections.push(`${item.name}@${item.version}\nDeclared license: ${JSON.stringify(license)}\n${texts.join('\n\n') || 'No root license text found; review required.'}`);
  packages.push({ ...item, license, notices });
}
await writeFile('apps/web/dist/notices/THIRD-PARTY.txt', sections.sort().join('\n\n---\n\n') + '\n');
await writeFile('apps/web/dist/notices/runtime-packages.json', JSON.stringify({ schema_version: 1, packages }, null, 2) + '\n');
