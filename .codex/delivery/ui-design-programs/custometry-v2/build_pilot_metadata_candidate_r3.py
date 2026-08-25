#!/usr/bin/env python3
"""Derive the r3 metadata-only pilot candidate from the exact accepted v2 bytes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[4]
PROGRAM = ROOT / ".codex/delivery/ui-design-programs/custometry-v2"
SOURCE_ROOT = PROGRAM / "evidence/pilot-candidate-v2"
SOURCE = SOURCE_ROOT / "ru/source.html"
CANDIDATE_ROOT = PROGRAM / "evidence/pilot-candidate-v3-metadata"
CANDIDATE = CANDIDATE_ROOT / "ru/source.html"
RECEIPT = CANDIDATE_ROOT / "derivation-receipt.json"


METADATA_SCRIPT = r'''
<script id="ui-standard-metadata-r3">
(() => {
  const safe = value => String(value || "default").trim().toLowerCase().replace(/[^a-z0-9._-]+/g, "-").replace(/^-|-$/g, "") || "default";
  const domPath = node => {
    const parts = [];
    let current = node;
    while (current && current !== document.body) {
      if (!current.parentElement) return `detached.${safe(current.localName || current.tagName)}`;
      const siblings = [...current.parentElement.children].filter(item => item.tagName === current.tagName);
      parts.unshift(`${current.tagName.toLowerCase()}.${siblings.indexOf(current) + 1}`);
      current = current.parentElement;
    }
    return `body.${parts.join(".")}`;
  };
  const region = node => {
    const id = node.id || "";
    const classes = node.classList || [];
    if (classes.contains("app-shell")) return "shell.application";
    if (classes.contains("rail")) return "shell.primary-rail";
    if (id === "nav-context-panel") return "shell.context-navigation";
    if (classes.contains("page-header")) return "shell.page-header";
    if (classes.contains("report-tabs")) return "shell.route-tabs";
    if (classes.contains("command-bar")) return "shell.command-bar";
    if (id === "report-main") return "shell.main-content";
    if (id === "context-drawer") return "shell.context-drawer";
    if (id === "focus-surface") return "shell.focus-surface";
    if (node.tagName === "DIALOG") return `overlay.${safe(id || node.getAttribute("aria-labelledby"))}`;
    return null;
  };
  const component = node => {
    const classes = node.classList || [];
    if (classes.contains("report-tab")) return "navigation.tab";
    if (classes.contains("rail-button")) return "navigation.rail-action";
    if (classes.contains("menu-row")) return "navigation.menu-item";
    if (classes.contains("context-chip")) return "control.context-chip";
    if (classes.contains("icon-button")) return "action.icon-button";
    if (classes.contains("text-button")) return "action.text-button";
    if (classes.contains("compact-control")) return "control.compact";
    if (classes.contains("block-choice")) return "control.choice";
    if (classes.contains("panel")) return "surface.panel";
    if (classes.contains("echart")) return "data.chart";
    if (node.tagName === "BUTTON") return "action.button";
    if (node.tagName === "A") return "navigation.link";
    if (node.tagName === "INPUT") return `input.${safe(node.type || "text")}`;
    if (node.tagName === "SELECT") return "input.select";
    if (node.tagName === "TEXTAREA") return "input.textarea";
    if (node.tagName === "DETAILS") return "control.disclosure";
    if (node.tagName === "TABLE") return "data.table";
    if (node.tagName === "DIALOG") return "surface.dialog";
    return null;
  };
  const variant = node => {
    const explicit = [...node.attributes].find(attr => /^data-(?:view|toolbar-menu|export-scope|chart-settings-scope|nav-root)$/.test(attr.name));
    if (explicit) return `${safe(explicit.name.slice(5))}.${safe(explicit.value)}`;
    const classes = [...(node.classList || [])].filter(name => !/^(is-|has-)/.test(name));
    return classes.length ? safe(classes.slice(0, 3).join(".")) : safe(node.getAttribute("role") || node.tagName);
  };
  const state = node => {
    if (node.matches(":disabled,[aria-disabled='true']")) return "disabled";
    if (node.getAttribute("aria-selected") === "true") return "selected";
    if (node.getAttribute("aria-pressed") === "true") return "pressed";
    if (node.getAttribute("aria-current")) return "current";
    if (node.matches("[open]") || node.getAttribute("aria-expanded") === "true") return "expanded";
    if (node.getAttribute("aria-invalid") === "true") return "error";
    return "default";
  };
  const size = node => {
    const classes = node.classList || [];
    if (classes.contains("icon-button") || classes.contains("rail-button")) return "icon";
    if (classes.contains("compact-control") || classes.contains("context-chip")) return "compact";
    if (classes.contains("text-button")) return "text";
    return "standard";
  };
  const icon = node => {
    const name = String(node.localName || node.tagName).toLowerCase();
    if (name === "use") return safe((node.getAttribute("href") || "").replace(/^#/, ""));
    if (name === "svg") {
      const use = node.querySelector("use");
      return use ? safe((use.getAttribute("href") || "").replace(/^#/, "")) : "inline-svg";
    }
    return null;
  };
  const annotate = node => {
    if (!(node instanceof Element) || !node.isConnected || node.id === "ui-standard-metadata-r3") return;
    node.setAttribute("data-ui-standard-id", `pilot-v3:${domPath(node)}`);
    node.setAttribute("data-ui-element", safe(node.getAttribute("role") || node.tagName));
    node.setAttribute("data-ui-anchor", "pilot-v3-responsive-web");
    node.setAttribute("data-ui-state", state(node));
    const regionId = region(node);
    const componentId = component(node);
    const iconId = icon(node);
    if (regionId) node.setAttribute("data-ui-region", regionId);
    if (componentId) {
      node.setAttribute("data-ui-component", componentId);
      node.setAttribute("data-ui-variant", variant(node));
      node.setAttribute("data-ui-size", size(node));
      const parentRegion = node.closest("[data-ui-region]");
      node.setAttribute("data-ui-slot", `${parentRegion ? parentRegion.getAttribute("data-ui-region") : "content"}.${safe(node.getAttribute("role") || node.tagName)}`);
    }
    if (iconId) node.setAttribute("data-ui-icon", iconId);
    node.setAttribute("data-ui-reusable", (componentId || regionId || iconId) ? "true" : "false");
  };
  const annotateTree = root => {
    if (root instanceof Element) annotate(root);
    for (const node of root.querySelectorAll ? root.querySelectorAll("*") : []) annotate(node);
  };
  annotateTree(document.body);
  requestAnimationFrame(() => annotateTree(document.body));
  new MutationObserver(records => {
    for (const record of records) {
      if (record.type === "childList") for (const node of record.addedNodes) annotateTree(node);
      else if (record.target instanceof Element) annotate(record.target);
    }
  }).observe(document.body, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ["aria-selected", "aria-pressed", "aria-current", "aria-expanded", "aria-invalid", "disabled", "open", "class"]
  });
})();
</script>
'''.strip()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    source_bytes = SOURCE.read_bytes()
    marker = b"</body>"
    if source_bytes.count(marker) != 1:
        raise ValueError("accepted source must contain exactly one closing body tag")
    candidate_bytes = source_bytes.replace(marker, METADATA_SCRIPT.encode("utf-8") + marker)
    CANDIDATE.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATE.write_bytes(candidate_bytes)
    source_assets = SOURCE_ROOT / "assets"
    candidate_assets = CANDIDATE_ROOT / "assets"
    candidate_assets.mkdir(parents=True, exist_ok=True)
    assets = []
    for source_asset in sorted(source_assets.iterdir()):
        if not source_asset.is_file():
            continue
        target_asset = candidate_assets / source_asset.name
        shutil.copyfile(source_asset, target_asset)
        if digest(source_asset) != digest(target_asset):
            raise ValueError(f"candidate asset copy differs: {source_asset.name}")
        assets.append({"path": str(target_asset.relative_to(ROOT)), "sha256": digest(target_asset)})
    receipt = {
        "schema_id": "codex.ui-pilot-metadata-derivation/v1",
        "candidate_id": "custometry-pilot-candidate-v3-metadata",
        "source": {"path": str(SOURCE.relative_to(ROOT)), "sha256": digest(SOURCE)},
        "candidate": {"path": str(CANDIDATE.relative_to(ROOT)), "sha256": digest(CANDIDATE)},
        "builder": {
            "path": str(Path(__file__).resolve().relative_to(ROOT)),
            "sha256": digest(Path(__file__).resolve()),
            "method": "byte_exact_source_plus_one_terminal_non_rendering_metadata_script",
        },
        "metadata_script_sha256": hashlib.sha256(METADATA_SCRIPT.encode("utf-8")).hexdigest(),
        "asset_copies": assets,
        "allowed_difference": "one terminal script whose only DOM mutations are data-ui-* attributes",
        "forbidden_differences": [
            "visible_text", "marketing_copy", "dom_element_order", "css", "assets", "fonts",
            "network_behavior", "focus_behavior", "responsive_behavior", "product_semantics",
        ],
        "owner_authority": "candidate_only_pending_exact_G0_owner_acceptance",
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
