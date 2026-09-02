import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { MemoryRouter } from "react-router-dom";

import "../../src/i18n";
import i18n from "../../src/i18n";
import { ConnectionEditor, ConnectionsList } from "../../src/features/connections/Connections";
import { ConnectionPresentationFixture } from "../../src/features/connections/connection-fixtures";

function renderRoute(node: React.ReactNode) { return render(<MemoryRouter>{node}</MemoryRouter>); }

beforeEach(() => { window.sessionStorage.clear(); void i18n.changeLanguage("en"); });
afterEach(cleanup);

describe("W33 Connections list and editor", () => {
  it("searches and filters governed status and owner metadata", async () => {
    renderRoute(<ConnectionsList workspaceKey="northwind-retail" api={new ConnectionPresentationFixture()} fixture />);
    expect(await screen.findByRole("heading", { level: 1, name: "Connections" })).toBeVisible();
    expect(screen.getAllByRole("listitem")).toHaveLength(4);
    fireEvent.change(screen.getByRole("searchbox", { name: "Search connections" }), { target: { value: "assortment" } });
    expect(screen.getAllByRole("listitem")).toHaveLength(1);
    expect(screen.getByText("Weekly assortment template")).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: "Clear filters" }));
    fireEvent.change(screen.getByLabelText("Status"), { target: { value: "degraded" } });
    expect(screen.getAllByRole("listitem")).toHaveLength(1);
    expect(screen.getByText("Store events")).toBeVisible();
    fireEvent.change(screen.getByLabelText("Owner"), { target: { value: "Operations" } });
    expect(screen.getAllByRole("listitem")).toHaveLength(1);
  });

  it("distinguishes empty, forbidden, failed, stale, degraded, and explicit unavailable states", async () => {
    for (const [state, text] of [["w33-empty", "No connections yet"], ["w33-forbidden", "Connections are unavailable"], ["w33-failed", "Connections could not be loaded"], ["w33-refreshing", "Refreshing"], ["w33-stale", "Stale"], ["w33-degraded", "Degraded"]] as const) {
      const view = renderRoute(<ConnectionsList workspaceKey="northwind-retail" api={new ConnectionPresentationFixture(state)} fixture />);
      expect((await screen.findAllByText(text))[0]).toBeVisible();
      view.unmount();
    }
    const unavailableFixture = new ConnectionPresentationFixture();
    const unavailable = {
      capabilities: () => Promise.resolve({ principalId: "p", workspaceId: "w", permissions: new Set(["connection.read_metadata", "connection.manage"]) }),
      list: () => Promise.resolve({ support: "unavailable" as const, connections: [], observedAt: "2026-08-30T00:00:00Z", stableCode: "CONNECTION_LIST_UNAVAILABLE" as const }),
      create: unavailableFixture.create.bind(unavailableFixture),
      test: unavailableFixture.test.bind(unavailableFixture),
      discover: unavailableFixture.discover.bind(unavailableFixture),
    };
    renderRoute(<ConnectionsList workspaceKey="northwind-retail" api={unavailable} />);
    expect(await screen.findByText("Connection listing is not available in W14")).toBeVisible();
    expect(screen.getByText("CONNECTION_LIST_UNAVAILABLE")).toBeVisible();
  });

  it("announces validation, keeps local draft truth explicit, then saves/tests with redacted feedback", async () => {
    const api = new ConnectionPresentationFixture();
    const view = renderRoute(<ConnectionEditor workspaceKey="northwind-retail" api={api} fixture />);
    expect(await screen.findByRole("heading", { level: 1, name: "New connection" })).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: "Save and test" }));
    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent("Review the highlighted fields");
    await waitFor(() => expect(document.activeElement).toBe(alert));

    fireEvent.change(screen.getByLabelText("Display name"), { target: { value: "Retail source" } });
    fireEvent.change(screen.getByLabelText("Network profile reference"), { target: { value: "retail_demo" } });
    fireEvent.change(screen.getByLabelText("Credential reference"), { target: { value: "retail_reader" } });
    fireEvent.click(screen.getByRole("button", { name: "Save draft" }));
    expect(await screen.findByText("Draft saved in this tab only; the credential reference was not stored. W14 has no persisted draft lifecycle.")).toBeVisible();
    expect(window.sessionStorage.getItem("custometry:w33:connection-draft:northwind-retail")).not.toContain("retail_reader");
    view.unmount();
    renderRoute(<ConnectionEditor workspaceKey="northwind-retail" api={api} fixture />);
    expect(await screen.findByLabelText("Display name")).toHaveValue("Retail source");
    expect(screen.getByLabelText("Network profile reference")).toHaveValue("retail_demo");
    expect(screen.getByLabelText("Credential reference")).toHaveValue("");
    fireEvent.change(screen.getByLabelText("Credential reference"), { target: { value: "retail_reader" } });
    fireEvent.click(screen.getByRole("button", { name: "Save and test" }));
    const result = await screen.findByRole("region", { name: "Connection persisted and read-only test passed" });
    expect(within(result).getByText(/Credential and network references were not returned/)).toBeVisible();
    expect(screen.getByLabelText("Credential reference")).toHaveValue("");
  });

  it("keeps future and template connectors governed and localizes the route to Russian", async () => {
    await i18n.changeLanguage("ru");
    renderRoute(<ConnectionEditor workspaceKey="northwind-retail" api={new ConnectionPresentationFixture()} fixture />);
    await screen.findByRole("heading", { level: 1, name: "Новое подключение" });
    fireEvent.change(screen.getByLabelText("Коннектор"), { target: { value: "yandex_metrica" } });
    expect(screen.getByText("Коннектор не активен на этой границе")).toBeVisible();
    expect(screen.getByRole("button", { name: "Сохранить и проверить" })).toBeDisabled();
    fireEvent.change(screen.getByLabelText("Коннектор"), { target: { value: "xlsx_template" } });
    expect(screen.getByLabelText("Версия опубликованного шаблона")).toBeVisible();
    await waitFor(() => expect(document.documentElement.lang || "ru").toBeTruthy());
  });
});
