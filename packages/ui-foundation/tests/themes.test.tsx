import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import {
  defaultStaticThemeId,
  defaultUiThemeId,
  SemanticThemeBoundary,
  semanticThemes,
  themeIds,
} from "../src";

describe("semantic theme registry", () => {
  it("ships exactly the accepted ordered theme IDs and defaults", () => {
    expect(themeIds).toEqual(["abyss", "graphite", "frost", "paper"]);
    expect(Object.keys(semanticThemes)).toEqual(themeIds);
    expect(defaultUiThemeId).toBe("graphite");
    expect(defaultStaticThemeId).toBe("paper");
  });

  it("exposes only project-owned semantic CSS properties", () => {
    render(
      <SemanticThemeBoundary themeId="abyss">
        <span>content</span>
      </SemanticThemeBoundary>,
    );
    const boundary = screen.getByText("content").parentElement;
    expect(boundary).toHaveAttribute("data-theme", "abyss");
    expect(boundary).toHaveStyle({ "--custometry-canvas": "#03080d" });
  });
});
