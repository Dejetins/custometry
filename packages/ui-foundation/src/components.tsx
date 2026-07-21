import type { PropsWithChildren } from "react";
import styled from "styled-components";

import { themeCssProperties, type ThemeId } from "./themes";

const ThemeBoundaryRoot = styled.div`
  min-height: 100%;
  color: var(--custometry-text);
  background: var(--custometry-canvas);
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;

  *, *::before, *::after {
    box-sizing: border-box;
  }

  :focus-visible {
    outline: 2px solid var(--custometry-focus);
    outline-offset: 2px;
  }
`;

export function SemanticThemeBoundary({
  children,
  themeId,
}: PropsWithChildren<{ readonly themeId: ThemeId }>): React.JSX.Element {
  return (
    <ThemeBoundaryRoot
      data-theme={themeId}
      style={themeCssProperties(themeId)}
    >
      {children}
    </ThemeBoundaryRoot>
  );
}

export const FoundationPanel = styled.section`
  color: var(--custometry-text);
  background: var(--custometry-surface);
  border: 1px solid var(--custometry-line);
  border-radius: 10px;
  box-shadow: var(--custometry-shadow-panel);
`;

export const FoundationButton = styled.button`
  min-height: 36px;
  padding: 0 12px;
  color: var(--custometry-text-strong);
  background: var(--custometry-surface-raised);
  border: 1px solid var(--custometry-line);
  border-radius: 7px;
  cursor: pointer;

  &:hover {
    border-color: var(--custometry-line-strong);
  }

  &[aria-pressed="true"] {
    color: var(--custometry-on-accent);
    background: var(--custometry-accent);
    border-color: var(--custometry-accent);
  }
`;
