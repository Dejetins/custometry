/** Record Rollup's included modules and their installed package identities. */
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, realpathSync, writeFileSync } from "node:fs";
import path from "node:path";
import type { Plugin } from "vite";

const sha256 = (value: string | Uint8Array) => createHash("sha256").update(value).digest("hex");

export function supplyInventory(): Plugin {
  let root = "";
  let outputDirectory = "";
  return {
    name: "custometry-supply-inventory",
    apply: "build",
    configResolved(config) {
      root = realpathSync(path.resolve(config.root, "../.."));
      outputDirectory = path.resolve(config.root, config.build.outDir);
    },
    writeBundle(_options, bundle) {
      const packages = new Map<string, { name: string; version: string; root: string; metadata_sha256: string }>();
      const modules: { path: string; sha256: string; package: string | null; chunks: string[] }[] = [];
      const included = new Map<string, string[]>();
      for (const [file, output] of Object.entries(bundle)) {
        if (output.type !== "chunk") continue;
        for (const id of Object.keys(output.modules)) {
          included.set(id, [...(included.get(id) ?? []), file]);
        }
      }
      for (const [id, chunks] of [...included].sort(([a], [b]) => a.localeCompare(b, "en"))) {
        // Rollup virtual wrappers have no separate upstream file or package.
        if (id.startsWith("\0")) continue;
        const filename = realpathSync(id.split("?")[0]);
        const relative = path.relative(root, filename);
        if (relative.startsWith("../") || path.isAbsolute(relative)) throw new Error("Module outside supply source");
        let directory = path.dirname(filename);
        let identity: string | null = null;
        while (directory !== root && directory.startsWith(root + path.sep)) {
          const manifest = path.join(directory, "package.json");
          if (existsSync(manifest)) {
            const raw = readFileSync(manifest);
            const metadata = JSON.parse(raw.toString());
            if (metadata.name && metadata.version) {
              identity = path.relative(root, directory);
              packages.set(identity, { name: metadata.name, version: metadata.version, root: identity, metadata_sha256: sha256(raw) });
              break;
            }
          }
          directory = path.dirname(directory);
        }
        if (relative.includes("node_modules/") && identity === null) throw new Error("Unidentified bundled dependency");
        modules.push({ path: relative, sha256: sha256(readFileSync(filename)), package: identity, chunks: chunks.sort() });
      }
      if (!modules.length || !packages.size) throw new Error("Empty Web module inventory");
      const chunks = Object.fromEntries(Object.entries(bundle)
        .filter(([, item]) => item.type === "chunk")
        .map(([name]) => [name, sha256(readFileSync(path.join(outputDirectory, name)))]));
      mkdirSync(path.join(outputDirectory, "notices"), { recursive: true });
      writeFileSync(path.join(outputDirectory, "notices/runtime-modules.json"),
        JSON.stringify({ schema_version: 1, selection: "Rollup emitted chunk modules", packages: [...packages.values()].sort((a, b) => a.root.localeCompare(b.root, "en")), modules, chunks }, null, 2) + "\n");
    },
  };
}
