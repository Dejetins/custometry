import styled from "styled-components";

/** Versioned pilot inheritance, scoped until subsequent consumers migrate. */
export const installationFoundationVersion = "pilot-entry/v1";
export const InstallationFrame = styled.div`
  --entry-canvas: #070708;
  --entry-surface: #111214;
  --entry-soft: #151619;
  --entry-module: #1a1b1e;
  --entry-border: #303136;
  --entry-text: #f0f0f2;
  --entry-secondary: #a7a7ad;
  --entry-focus: #8bd2e8;
  min-height: 100dvh;
  padding: 8px;
  background: var(--entry-canvas);
  color: var(--entry-text);
  color-scheme: dark;
  font: 14px/1.35 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  -webkit-font-smoothing: antialiased;
  & * { box-sizing: border-box; }
  & :is(button, select) { font: inherit; }
  & :focus-visible { outline: 2px solid var(--entry-focus); outline-offset: 2px; }
  & svg { flex-shrink: 0; width: 17px; height: 17px; stroke-width: 1.75; }
  & h1 { margin: 0; font-size: 17px; font-weight: 620; letter-spacing: -.02em; }
  & h2 { margin: 0; font-size: 14px; font-weight: 600; }
  & p { margin: 0; }
  & .entry-secondary { color: var(--entry-secondary); }
  & .entry-skip { position: absolute; inset-block-start: 8px; inset-inline-start: 16px; transform: translateY(-160%); padding: 8px 12px; background: var(--entry-module); z-index: 2; }
  & .entry-skip:focus { transform: none; }
`;
export const InstallationPanel = styled.section`
  min-width: 0;
  padding: 20px;
  background: var(--entry-surface);
  border: 1px solid var(--entry-border);
  border-radius: 10px;
`;
export const InstallationButton = styled.button`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-height: 32px;
  padding: 6px 10px;
  border: 1px solid transparent;
  border-radius: 7px;
  color: #071014;
  background: #8ccfe3;
  font-weight: 650;
  &:hover { background: #a5dcec; }
  &[aria-disabled="true"] { cursor: wait; }
`;
export const InstallationLink = styled.a`
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 32px;
  padding: 6px 9px;
  border-radius: 7px;
  color: var(--entry-secondary);
  text-decoration: none;
  &:hover { color: var(--entry-text); background: #222327; }
`;
export const InstallationStatusMark = styled.span<{ $state: "ready" | "not_ready" | "unknown" }>`
  display: inline-flex;
  gap: 6px;
  align-items: center;
  color: ${({ $state }) => $state === "ready" ? "#62c7aa" : $state === "not_ready" ? "#f07d87" : "#a7a7ad"};
`;
