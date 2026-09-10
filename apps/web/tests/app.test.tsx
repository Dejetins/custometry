import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import "../src/i18n";
import i18n from "../src/i18n";
import { App } from "../src/App";

beforeEach(() => {
  void i18n.changeLanguage("en");
  vi.stubGlobal("fetch", vi.fn().mockImplementation(async (input: RequestInfo | URL) => {
    if (String(input).includes("help-index")) {
      return {
        ok: true,
        json: async () => ({
          documents: [
            { path: "docs/index.md", title: "Custometry documentation", visibility: "public", locale: "en" },
            { path: "docs/internal.md", title: "Internal", visibility: "authenticated", locale: "en" },
          ],
        }),
      };
    }
    return { ok: true, status: 200, json: async () => ({
      schema_version: "custometry-installation-status/v1", state: "ready_for_bootstrap",
      next_action: "bootstrap_not_available", version: "test",
      components: { database: "ready", schema: "ready", storage: "ready" },
    }) };
  }));
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("Foundation shell", () => {
  it("renders the installation entry with operational readiness", async () => {
    render(<MemoryRouter initialEntries={["/"]}><App /></MemoryRouter>);
    expect(screen.getByRole("heading", { level: 1 })).toBeInTheDocument();
    expect(await screen.findByText("Installation is ready")).toHaveAttribute("role", "status");
    expect(screen.getByText("test")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Open installation help" })).toHaveAttribute(
      "href", "/docs/install/local/#first-run-status",
    );
  });

  it("labels unimplemented product routes as planned", () => {
    render(<MemoryRouter initialEntries={["/w/northwind-retail/overview"]}><App /></MemoryRouter>);
    expect(screen.getByText("UI-CORE-001 · MVP")).toBeInTheDocument();
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Workspace Overview");
    expect(screen.getByText("Planned surface")).toBeInTheDocument();
  });

  it("renders only public articles from the shipped Help index", async () => {
    render(<MemoryRouter initialEntries={["/help"]}><App /></MemoryRouter>);
    expect(await screen.findByText("Custometry documentation")).toBeInTheDocument();
    expect(screen.queryByText("Internal")).not.toBeInTheDocument();
  });

  it("localizes the installation entry into Russian", async () => {
    await i18n.changeLanguage("ru");
    render(<MemoryRouter initialEntries={["/"]}><App /></MemoryRouter>);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Установка");
    expect(await screen.findByText("Установка готова")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Открыть справку по установке" })).toHaveAttribute(
      "href", "/docs/ru/install/local/#first-run-status",
    );
  });

  it("does not expose an English route title on a Russian planned surface", async () => {
    await i18n.changeLanguage("ru");
    render(<MemoryRouter initialEntries={["/w/northwind-retail/overview"]}><App /></MemoryRouter>);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(
      "Обзор рабочего пространства",
    );
    expect(screen.queryByText("Workspace Overview")).not.toBeInTheDocument();
  });

  it("exposes every route through the mobile More menu", () => {
    render(<MemoryRouter initialEntries={["/w/northwind-retail/overview"]}><App /></MemoryRouter>);
    const moreButton = screen.getByRole("button", { name: "More sections" });
    fireEvent.click(moreButton);
    const menu = screen.getByRole("dialog", { name: "All sections" });
    expect(within(menu).getByRole("link", { name: "Administration" })).toBeInTheDocument();
    expect(moreButton).toHaveAttribute("aria-expanded", "true");
    fireEvent.click(within(menu).getByRole("button", { name: "Close menu" }));
    expect(moreButton).toHaveAttribute("aria-expanded", "false");
  });
});
