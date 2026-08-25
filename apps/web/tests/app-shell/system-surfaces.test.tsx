import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import "../../src/i18n";
import i18n from "../../src/i18n";
import { App } from "../../src/App";

beforeEach(() => {
  window.localStorage.clear();
  window.sessionStorage.clear();
  void i18n.changeLanguage("en");
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => ({ version: "fixture" }) }));
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("W31 system presentation", () => {
  it.each([
    ["w31-forbidden", "UI-SYS-001", "This surface is not available"],
    ["w31-session-expired", "UI-SYS-003", "Your session has expired"],
    ["w31-maintenance", "UI-SYS-004", "Part of Custometry is under maintenance"],
    ["w31-upgrade-required", "UI-SYS-005", "A client upgrade is required"],
  ])("renders the %s contract fixture truthfully", (view, surfaceId, title) => {
    render(<MemoryRouter initialEntries={[`/w/northwind-retail/overview?view=${view}`]}><App /></MemoryRouter>);
    expect(screen.getByRole("heading", { level: 1, name: title })).toBeInTheDocument();
    expect(document.querySelector(`[data-system-surface="${surfaceId}"]`)).toBeInTheDocument();
    expect(screen.getByRole("note")).toHaveTextContent("No backend authorization");
  });

  it("clears only protected presentation fixture data on session expiry", () => {
    window.sessionStorage.setItem("custometry-protected-presentation:workspace", "secret fixture");
    window.sessionStorage.setItem("unrelated", "preserved");
    render(<MemoryRouter initialEntries={["/w/northwind-retail/overview?view=w31-session-expired"]}><App /></MemoryRouter>);
    expect(window.sessionStorage.getItem("custometry-protected-presentation:workspace")).toBeNull();
    expect(window.sessionStorage.getItem("unrelated")).toBe("preserved");
  });

  it("keeps route identity while switching locale", async () => {
    render(<MemoryRouter initialEntries={["/w/northwind-retail/overview"]}><App /></MemoryRouter>);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Workspace Overview");
    fireEvent.click(screen.getByRole("button", { name: "Switch language" }));
    expect(await screen.findByRole("heading", { level: 1 })).toHaveTextContent("Обзор рабочего пространства");
    expect(screen.getByRole("link", { name: "Обзор" })).toHaveAttribute("href", "/w/northwind-retail/overview");
  });

  it("places the skip link before repeated application chrome", () => {
    render(<MemoryRouter initialEntries={["/w/northwind-retail/overview"]}><App /></MemoryRouter>);
    const shellBoundary = document.querySelector("[data-theme]");
    expect(shellBoundary?.querySelector("a")).toHaveClass("skip-link");
    expect(screen.getByRole("link", { name: "Overview" })).toHaveAttribute("aria-current", "page");
  });
});
