import type { CSSProperties } from "react";

export const themeIds = ["abyss", "graphite", "frost", "paper"] as const;
export type ThemeId = (typeof themeIds)[number];

export const defaultUiThemeId: ThemeId = "graphite";
export const defaultStaticThemeId: ThemeId = "paper";

export interface SemanticThemeTokens {
  readonly colorScheme: "dark" | "light";
  readonly canvas: string;
  readonly surface: string;
  readonly surfaceRaised: string;
  readonly line: string;
  readonly lineStrong: string;
  readonly text: string;
  readonly textStrong: string;
  readonly muted: string;
  readonly accent: string;
  readonly accentStrong: string;
  readonly focus: string;
  readonly onAccent: string;
  readonly positive: string;
  readonly warning: string;
  readonly negative: string;
  readonly shadowPanel: string;
}

export const semanticThemes: Readonly<Record<ThemeId, SemanticThemeTokens>> = {
  abyss: {
    colorScheme: "dark",
    canvas: "#03080d",
    surface: "#0a1621",
    surfaceRaised: "#0e1d2a",
    line: "#28465b",
    lineStrong: "#47718b",
    text: "#c8d5de",
    textStrong: "#f2f7fa",
    muted: "#8297a7",
    accent: "#68b9d7",
    accentStrong: "#97d5e8",
    focus: "#8dd9ef",
    onAccent: "#041016",
    positive: "#66c7a7",
    warning: "#e7bd72",
    negative: "#ef8e98",
    shadowPanel: "0 16px 44px rgba(0, 0, 0, 0.26)",
  },
  graphite: {
    colorScheme: "dark",
    canvas: "#081018",
    surface: "#111e2a",
    surfaceRaised: "#162534",
    line: "#365066",
    lineStrong: "#55748c",
    text: "#d5dee6",
    textStrong: "#f5f8fa",
    muted: "#8fa2b2",
    accent: "#79c3df",
    accentStrong: "#a8dded",
    focus: "#8ad8f2",
    onAccent: "#07131a",
    positive: "#70c9aa",
    warning: "#e2b76b",
    negative: "#ed8792",
    shadowPanel: "0 12px 36px rgba(0, 0, 0, 0.18)",
  },
  frost: {
    colorScheme: "light",
    canvas: "#edf3f6",
    surface: "#ffffff",
    surfaceRaised: "#e8f0f4",
    line: "#9db2bf",
    lineStrong: "#6e8999",
    text: "#334b5a",
    textStrong: "#132b39",
    muted: "#5f7887",
    accent: "#16769a",
    accentStrong: "#0b5e7d",
    focus: "#096b91",
    onAccent: "#ffffff",
    positive: "#18765f",
    warning: "#8a650d",
    negative: "#a43f4b",
    shadowPanel: "0 14px 36px rgba(30, 69, 88, 0.08)",
  },
  paper: {
    colorScheme: "light",
    canvas: "#f4f5f6",
    surface: "#ffffff",
    surfaceRaised: "#eef1f3",
    line: "#a7b2b9",
    lineStrong: "#707f88",
    text: "#34434c",
    textStrong: "#15242c",
    muted: "#667780",
    accent: "#126e91",
    accentStrong: "#075776",
    focus: "#075f82",
    onAccent: "#ffffff",
    positive: "#176f5a",
    warning: "#80600d",
    negative: "#9b3d48",
    shadowPanel: "0 12px 32px rgba(25, 41, 50, 0.08)",
  },
};

export function isThemeId(value: string | null): value is ThemeId {
  return value !== null && (themeIds as readonly string[]).includes(value);
}

export type SemanticCssProperties = CSSProperties & {
  readonly [key: `--custometry-${string}`]: string;
};

export function themeCssProperties(themeId: ThemeId): SemanticCssProperties {
  const tokens = semanticThemes[themeId];
  return {
    colorScheme: tokens.colorScheme,
    "--custometry-canvas": tokens.canvas,
    "--custometry-surface": tokens.surface,
    "--custometry-surface-raised": tokens.surfaceRaised,
    "--custometry-line": tokens.line,
    "--custometry-line-strong": tokens.lineStrong,
    "--custometry-text": tokens.text,
    "--custometry-text-strong": tokens.textStrong,
    "--custometry-muted": tokens.muted,
    "--custometry-accent": tokens.accent,
    "--custometry-accent-strong": tokens.accentStrong,
    "--custometry-focus": tokens.focus,
    "--custometry-on-accent": tokens.onAccent,
    "--custometry-positive": tokens.positive,
    "--custometry-warning": tokens.warning,
    "--custometry-negative": tokens.negative,
    "--custometry-shadow-panel": tokens.shadowPanel,
  };
}
