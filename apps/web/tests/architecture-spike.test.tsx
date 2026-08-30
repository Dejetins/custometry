import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import "../src/i18n";
import { App } from "../src/App";

class EventSourceStub {
  public static instances: EventSourceStub[] = [];
  private readonly listeners = new Map<string, Array<(event: MessageEvent<string>) => void>>();

  public constructor(public readonly url: string) {
    EventSourceStub.instances.push(this);
  }

  public addEventListener(type: string, listener: EventListenerOrEventListenerObject): void {
    const callback = listener as (event: MessageEvent<string>) => void;
    this.listeners.set(type, [...(this.listeners.get(type) ?? []), callback]);
  }

  public emit(type: string, payload: unknown): void {
    const event = new MessageEvent(type, { data: JSON.stringify(payload) });
    for (const listener of this.listeners.get(type) ?? []) listener(event);
  }

  public close(): void {}
}

function jsonResponse(payload: unknown): Pick<Response, "json" | "ok" | "status"> {
  return { ok: true, status: 200, json: async () => payload };
}

beforeEach(() => {
  window.localStorage.clear();
  EventSourceStub.instances = [];
  vi.stubGlobal("EventSource", EventSourceStub);
  vi.stubGlobal("fetch", vi.fn().mockImplementation((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.includes("cancellable-summary")) {
      return new Promise((_resolve, reject) => {
        init?.signal?.addEventListener("abort", () => reject(new DOMException("aborted", "AbortError")));
      });
    }
    if (url.includes("workspace-summary")) {
      return Promise.resolve(jsonResponse({
        workspace_id: "northwind-retail",
        revision: 1,
        result_count: 12,
        freshness: "authoritative",
      }));
    }
    return Promise.resolve(jsonResponse({ status: "ready", version: "test" }));
  }));
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("W20 route-bounded architecture spike", () => {
  it("keeps the legacy planned surface as the default rollback path", () => {
    render(<MemoryRouter initialEntries={["/w/northwind-retail/analytics/sales"]}><App /></MemoryRouter>);
    expect(screen.getByText("Planned surface")).toBeInTheDocument();
    expect(screen.getByTestId("open-architecture-spike")).toHaveAttribute(
      "href",
      "/w/northwind-retail/analytics/sales?view=linear-spike",
    );
  });

  it("separates MobX presentation state from Query REST and SSE snapshots", async () => {
    render(
      <MemoryRouter initialEntries={["/w/northwind-retail/analytics/sales?view=linear-spike"]}>
        <App />
      </MemoryRouter>,
    );
    await waitFor(() => expect(screen.getByTestId("server-revision")).toHaveTextContent("1"));
    expect(screen.getByTestId("server-transport")).toHaveTextContent("rest");
    expect(screen.getByTestId("theme-id")).toHaveTextContent("graphite");

    fireEvent.click(screen.getByRole("button", { name: "paper" }));
    expect(screen.getByTestId("theme-id")).toHaveTextContent("paper");
    expect(screen.getByTestId("server-revision")).toHaveTextContent("1");

    EventSourceStub.instances[0]?.emit("workspace-snapshot", {
      workspace_id: "northwind-retail",
      revision: 2,
      result_count: 13,
      freshness: "authoritative",
    });
    await waitFor(() => expect(screen.getByTestId("server-revision")).toHaveTextContent("2"));
    expect(screen.getByTestId("server-transport")).toHaveTextContent("sse");
    expect(screen.getByTestId("theme-id")).toHaveTextContent("paper");
  });

  it("persists bounded keyboard panel geometry and observes REST cancellation", async () => {
    render(
      <MemoryRouter initialEntries={["/w/northwind-retail/analytics/sales?view=linear-spike"]}>
        <App />
      </MemoryRouter>,
    );
    await screen.findByTestId("server-revision");
    const separator = screen.getByRole("separator", { name: "Resize spike sidebar" });
    fireEvent.keyDown(separator, { key: "ArrowRight" });
    expect(screen.getByTestId("sidebar-width")).toHaveTextContent("248px");
    expect(window.localStorage.getItem("custometry-spike-sidebar-width")).toBe("248");
    fireEvent.keyDown(separator, { key: "Home" });
    expect(screen.getByTestId("sidebar-width")).toHaveTextContent("240px");

    fireEvent.click(screen.getByRole("button", { name: "Prove REST cancellation" }));
    await waitFor(() => expect(screen.getByTestId("cancel-state")).toHaveTextContent("observed"));
  });

  it("rolls back through the same canonical route without losing history", async () => {
    render(
      <MemoryRouter initialEntries={["/w/northwind-retail/analytics/sales?view=linear-spike"]}>
        <App />
      </MemoryRouter>,
    );
    await screen.findByTestId("server-revision");
    fireEvent.click(screen.getByTestId("rollback-link"));
    expect(await screen.findByText("Sales result could not be loaded")).toBeInTheDocument();
    expect(screen.queryByText("Planned surface")).not.toBeInTheDocument();
  });
});
