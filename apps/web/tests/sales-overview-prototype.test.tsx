import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import "../src/i18n";
import { App } from "../src/App";

function setViewport(width: number): void {
  Object.defineProperty(window, "innerWidth", { configurable: true, value: width, writable: true });
  window.dispatchEvent(new Event("resize"));
}

beforeEach(() => {
  window.localStorage.clear();
  setViewport(1440);
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ status: "ready", version: "test" }),
  }));
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

function renderPrototype(entry = "/w/northwind-retail/analytics/sales?view=html-prototype"): void {
  render(
    <MemoryRouter initialEntries={[entry]}>
      <App />
    </MemoryRouter>,
  );
}

describe("UI-AN-003 HTML review prototype", () => {
  it("mounts the isolated accepted sales view without replacing the fallback route", () => {
    renderPrototype();
    expect(screen.getByTestId("sales-html-prototype")).toBeInTheDocument();
    expect(screen.getByRole("heading", { level: 1, name: "Sales overview" })).toBeInTheDocument();
    expect(screen.queryByText("Planned surface")).not.toBeInTheDocument();
  });

  it("switches between chart and data while keeping the compact result-trust trigger", () => {
    renderPrototype();
    const trustName = /Result trust: Retail sales v24\. Trusted/;
    expect(screen.getByRole("button", { name: trustName })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Show data view" }));
    expect(screen.getByLabelText("Revenue monthly data")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: trustName })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Show chart view" }));
    expect(screen.getByLabelText("Revenue trend chart")).toBeInTheDocument();
  });

  it("opens complete Result Trust details without restoring standalone Dataset or trust rows", () => {
    renderPrototype();
    fireEvent.click(screen.getByRole("button", { name: /Result trust: Retail sales v24\. Trusted/ }));
    const drawer = screen.getByRole("complementary", { name: "Result trust details" });
    expect(within(drawer).getByText("Retail sales v24")).toBeInTheDocument();
    expect(within(drawer).getByText("Within 24-hour SLA")).toBeInTheDocument();
    expect(within(drawer).getByText(/certified sales mart/)).toBeInTheDocument();
    fireEvent.click(within(drawer).getByRole("button", { name: "Close result trust" }));
    expect(screen.queryByRole("complementary", { name: "Result trust details" })).not.toBeInTheDocument();

    const inspector = screen.getByRole("complementary", { name: "Context panel" });
    expect(within(inspector).queryByRole("button", { name: /Dataset/ })).not.toBeInTheDocument();
    expect(within(inspector).queryByRole("button", { name: /Result trust/i })).not.toBeInTheDocument();
  });

  it("supports filter and fixed-header context review interactions", () => {
    renderPrototype();
    fireEvent.click(screen.getByRole("button", { name: "Filter view" }));
    expect(screen.getByText("Channel · All")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Hide context panel" }));
    expect(screen.queryByRole("complementary", { name: "Context panel" })).not.toBeInTheDocument();
    const restoreContext = screen.getByRole("button", { name: "Show context panel" });
    expect(restoreContext).toHaveAttribute("aria-expanded", "false");
    fireEvent.click(restoreContext);
    const restoredInspector = screen.getByRole("complementary", { name: "Context panel" });
    expect(screen.getByRole("button", { name: "Hide context panel" })).toHaveAttribute("aria-expanded", "true");
    expect(within(restoredInspector).queryByRole("button", { name: /context panel/i })).not.toBeInTheDocument();
  });

  it("keeps Search and Notifications below identity and Help and user menu in the sidebar footer", () => {
    renderPrototype();
    const workspace = screen.getByRole("complementary", { name: "Workspace navigation" });
    const utilities = within(workspace).getByLabelText("Sidebar utilities");
    const workspaceNavigation = within(workspace).getByRole("navigation", { name: "Primary navigation" });
    expect(within(utilities).getByRole("button", { name: "Search" })).toHaveTextContent("Search⌘K");
    expect(within(utilities).getByRole("button", { name: "Notifications" })).toHaveTextContent("Notifications");
    expect(utilities.compareDocumentPosition(workspaceNavigation) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();

    fireEvent.click(within(workspace).getByRole("button", { name: "Help" }));
    expect(screen.getByRole("button", { name: "Keyboard shortcuts" })).toBeInTheDocument();
    fireEvent.click(within(workspace).getByRole("button", { name: "Help" }));
    fireEvent.click(within(workspace).getByRole("button", { name: "User menu" }));
    expect(screen.getByRole("button", { name: "Profile" })).toBeInTheDocument();
  });

  it("marks Sales current and uses distinct Sales, Products, and Forecasts icons", () => {
    renderPrototype();
    const sales = screen.getByRole("button", { name: "Sales" });
    const products = screen.getByRole("button", { name: "Products" });
    const forecasts = screen.getByRole("button", { name: "Forecasts" });
    expect(sales).toHaveAttribute("aria-current", "page");
    expect(sales.querySelector("svg")).toHaveClass("lucide-chart-line");
    expect(products.querySelector("svg")).toHaveClass("lucide-package");
    expect(forecasts.querySelector("svg")).toHaveClass("lucide-trending-up");
  });

  it("supports expanded, resized, collapsed, hidden, and restored sidebar states", () => {
    renderPrototype();
    const root = screen.getByTestId("sales-html-prototype");
    const separator = screen.getByRole("separator", { name: "Resize sidebar" });
    expect(separator).toHaveAttribute("aria-valuenow", "224");
    fireEvent.keyDown(separator, { key: "ArrowRight" });
    expect(screen.getByRole("separator", { name: "Resize sidebar" })).toHaveAttribute("aria-valuenow", "232");

    fireEvent.click(screen.getByRole("button", { name: "Collapse sidebar" }));
    expect(root).toHaveClass("sales-prototype--sidebar-collapsed");
    expect(screen.queryByRole("separator", { name: "Resize sidebar" })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Expand sidebar" }));
    expect(root).toHaveClass("sales-prototype--sidebar-expanded");

    fireEvent.click(screen.getByRole("button", { name: "Hide sidebar" }));
    expect(root).toHaveClass("sales-prototype--sidebar-hidden");
    expect(screen.queryByRole("complementary", { name: "Workspace navigation" })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Show navigation" }));
    expect(screen.getByRole("complementary", { name: "Workspace navigation" })).toBeInTheDocument();
  });

  it("opens route-backed chart and breakdown Focus Explore states", () => {
    renderPrototype();
    fireEvent.click(screen.getByRole("button", { name: "Expand chart" }));
    expect(screen.getByRole("main", { name: "Sales Focus Explore" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { level: 1, name: "Revenue trend" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Data" }));
    expect(screen.getByLabelText("Revenue monthly data")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Close Focus Explore" }));
    expect(screen.getByRole("heading", { level: 1, name: "Sales overview" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Expand table" }));
    expect(screen.getByRole("heading", { level: 1, name: "By channel" })).toBeInTheDocument();
    expect(screen.getByRole("table", { name: "By channel" })).toBeInTheDocument();
  });

  it("switches channel, store, and product coverage with contribution", () => {
    renderPrototype();
    expect(screen.getByText("46.5%")).toBeInTheDocument();
    const channelRegion = screen.getByRole("region", { name: "By channel" });
    fireEvent.click(within(channelRegion).getByRole("button", { name: "By channel" }));
    fireEvent.click(within(channelRegion).getByRole("button", { name: "By store" }));
    expect(screen.getByRole("table", { name: "By store" })).toBeInTheDocument();
    expect(screen.getByText("Moscow Central")).toBeInTheDocument();

    const storeRegion = screen.getByRole("region", { name: "By store" });
    fireEvent.click(within(storeRegion).getByRole("button", { name: "By store" }));
    fireEvent.click(within(storeRegion).getByRole("button", { name: "By product" }));
    expect(screen.getByRole("table", { name: "By product" })).toBeInTheDocument();
    expect(screen.getByText("Home electronics")).toBeInTheDocument();
  });

  it("opens notifications and keeps external actions review-only", () => {
    renderPrototype();
    const notifications = screen.getByRole("button", { name: "Notifications" });
    fireEvent.click(notifications);
    expect(screen.getByText("No new data alerts")).toBeInTheDocument();
    fireEvent.click(notifications);

    fireEvent.click(screen.getByRole("button", { name: "Copy link" }));
    expect(screen.getByRole("status")).toHaveTextContent("Prototype link ready to copy");
    fireEvent.click(screen.getByRole("button", { name: "Download table" }));
    expect(screen.getByRole("status")).toHaveTextContent("Download is disabled in this prototype");
  });

  it("switches table comparisons between percentage and absolute values", () => {
    renderPrototype();
    const comparisonDisplay = screen.getByRole("group", { name: "Comparison display" });
    const percentage = within(comparisonDisplay).getByRole("button", { name: "Show percentage comparison" });
    const absolute = within(comparisonDisplay).getByRole("button", { name: "Show absolute comparison" });
    expect(percentage).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByText("+13.6%")).toBeInTheDocument();
    fireEvent.click(absolute);
    expect(absolute).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByText("+138.0M")).toBeInTheDocument();
  });

  it("defaults to a non-scaled compact shell at 1024 pixels", () => {
    setViewport(1024);
    renderPrototype();
    expect(screen.getByTestId("sales-html-prototype")).toHaveClass("sales-prototype--sidebar-collapsed");
    expect(screen.queryByRole("complementary", { name: "Context panel" })).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Show context panel" })).toBeInTheDocument();
  });
});
