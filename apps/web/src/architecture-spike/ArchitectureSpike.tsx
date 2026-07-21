import {
  FoundationButton,
  FoundationPanel,
  SemanticThemeBoundary,
  themeIds,
} from "@custometry/ui-foundation";
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { observer } from "mobx-react-lite";
import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";

import {
  beginDispatchMeasurement,
  recordNextPaint,
} from "./metrics";
import {
  fetchCancellableSnapshot,
  fetchWorkspaceSnapshot,
  subscribeToWorkspaceEvents,
  type WorkspaceSnapshot,
} from "./server-state";
import { sidebarGeometry, SpikeUiStore } from "./ui-store";

const snapshotQueryKey = ["architecture-spike", "workspace-snapshot"] as const;
const cancellableQueryKey = ["architecture-spike", "cancellable-snapshot"] as const;

const SpikeShell = styled.div<{ readonly $sidebarWidth: number }>`
  display: grid;
  grid-template-columns: ${({ $sidebarWidth }) => $sidebarWidth}px 8px minmax(0, 1fr);
  min-height: calc(100vh - 64px);
`;

const SpikeSidebar = styled.aside`
  padding: 16px 12px;
  overflow: hidden;
  background: var(--custometry-surface);
  border-right: 1px solid var(--custometry-line);

  h2, p { margin: 0; }
  p { margin-top: 8px; color: var(--custometry-muted); font-size: 12px; line-height: 1.45; }
`;

const ResizeHandle = styled.div`
  position: relative;
  cursor: col-resize;
  background: var(--custometry-canvas);
  touch-action: none;

  &::after {
    position: absolute;
    inset: 0 3px;
    content: "";
    background: var(--custometry-line);
  }

  &:hover::after, &:focus-visible::after {
    background: var(--custometry-accent);
  }
`;

const SpikeContent = styled.main`
  min-width: 0;
  padding: 18px;
  background: var(--custometry-canvas);
`;

const Header = styled.header`
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;

  h1 { margin: 0; color: var(--custometry-text-strong); font-size: 22px; }
  p { margin: 5px 0 0; color: var(--custometry-muted); font-size: 13px; }
`;

const Toolbar = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
`;

const EvidencePanel = styled(FoundationPanel)`
  padding: 16px;

  h2 { margin: 0 0 12px; color: var(--custometry-text-strong); font-size: 14px; }
  dl { display: grid; grid-template-columns: max-content 1fr; gap: 8px 12px; margin: 0; font-size: 13px; }
  dt { color: var(--custometry-muted); }
  dd { margin: 0; font-variant-numeric: tabular-nums; }
`;

function isCancellation(error: unknown): boolean {
  return (
    (error instanceof DOMException && error.name === "AbortError") ||
    (error instanceof Error && /cancel/i.test(`${error.name} ${error.message}`))
  );
}

const SpikeWorkspace = observer(function SpikeWorkspace({
  fallbackHref,
}: {
  readonly fallbackHref: string;
}): React.JSX.Element {
  const queryClient = useQueryClient();
  const uiStore = useMemo(() => new SpikeUiStore(window.localStorage), []);
  const [cancelState, setCancelState] = useState<"idle" | "pending" | "observed" | "failed">("idle");
  const [dragOrigin, setDragOrigin] = useState<{ readonly pointerX: number; readonly width: number } | null>(null);
  const snapshotQuery = useQuery({
    queryKey: snapshotQueryKey,
    queryFn: ({ signal }) => fetchWorkspaceSnapshot(signal),
    staleTime: 30_000,
  });

  useEffect(() => subscribeToWorkspaceEvents((snapshot) => {
    queryClient.setQueryData(snapshotQueryKey, snapshot);
  }), [queryClient]);

  useEffect(() => {
    const snapshot = snapshotQuery.data;
    if (!snapshot) return;
    recordNextPaint(snapshot.transport === "rest" ? "responseToPaint" : "sseToPaint", snapshot.receivedAt);
  }, [snapshotQuery.data]);

  useEffect(() => {
    if (!dragOrigin) return undefined;
    const onPointerMove = (event: PointerEvent): void => {
      uiStore.setSidebarWidth(dragOrigin.width + event.clientX - dragOrigin.pointerX);
    };
    const onPointerUp = (): void => setDragOrigin(null);
    window.addEventListener("pointermove", onPointerMove);
    window.addEventListener("pointerup", onPointerUp, { once: true });
    return () => {
      window.removeEventListener("pointermove", onPointerMove);
      window.removeEventListener("pointerup", onPointerUp);
    };
  }, [dragOrigin, uiStore]);

  const refreshSnapshot = (): void => {
    beginDispatchMeasurement();
    void snapshotQuery.refetch();
  };

  const proveCancellation = async (): Promise<void> => {
    setCancelState("pending");
    const request = queryClient.fetchQuery({
      queryKey: cancellableQueryKey,
      queryFn: ({ signal }) => fetchCancellableSnapshot(signal),
      staleTime: 0,
    });
    window.setTimeout(() => {
      void queryClient.cancelQueries({ queryKey: cancellableQueryKey, exact: true });
    }, 25);
    try {
      await request;
      setCancelState("failed");
    } catch (error: unknown) {
      setCancelState(isCancellation(error) ? "observed" : "failed");
    }
  };

  const snapshot: WorkspaceSnapshot | undefined = snapshotQuery.data;

  return (
    <SemanticThemeBoundary themeId={uiStore.themeId}>
      <SpikeShell $sidebarWidth={uiStore.sidebarWidth} data-testid="spike-shell">
        <SpikeSidebar>
          <h2>Architecture spike</h2>
          <p>MobX owns this panel width and theme preference. It does not own the snapshot at right.</p>
        </SpikeSidebar>
        <ResizeHandle
          aria-label="Resize spike sidebar"
          aria-orientation="vertical"
          aria-valuemax={sidebarGeometry.maximum}
          aria-valuemin={sidebarGeometry.minimum}
          aria-valuenow={uiStore.sidebarWidth}
          onDoubleClick={uiStore.resetSidebar}
          onKeyDown={(event) => {
            if (event.key === "ArrowLeft") uiStore.stepSidebar(-1);
            else if (event.key === "ArrowRight") uiStore.stepSidebar(1);
            else if (event.key === "Home") uiStore.resetSidebar();
            else return;
            event.preventDefault();
          }}
          onPointerDown={(event) => setDragOrigin({ pointerX: event.clientX, width: uiStore.sidebarWidth })}
          role="separator"
          tabIndex={0}
        />
        <SpikeContent>
          <Header>
            <div>
              <h1>Frontend architecture spike</h1>
              <p>Typed REST/SSE server state stays separate from presentation state.</p>
            </div>
            <Link className="secondary-button" data-testid="rollback-link" to={fallbackHref}>
              Roll back to legacy shell
            </Link>
          </Header>

          <Toolbar aria-label="Theme selection">
            {themeIds.map((themeId) => (
              <FoundationButton
                aria-pressed={uiStore.themeId === themeId}
                key={themeId}
                onClick={() => uiStore.setTheme(themeId)}
                type="button"
              >
                {themeId}
              </FoundationButton>
            ))}
            <FoundationButton onClick={refreshSnapshot} type="button">
              Refresh authoritative snapshot
            </FoundationButton>
            <FoundationButton onClick={() => void proveCancellation()} type="button">
              Prove REST cancellation
            </FoundationButton>
          </Toolbar>

          <Grid style={{ marginTop: 12 }}>
            <EvidencePanel aria-labelledby="server-state-title">
              <h2 id="server-state-title">TanStack Query server state</h2>
              <dl>
                <dt>Status</dt><dd data-testid="query-status">{snapshotQuery.status}</dd>
                <dt>Workspace</dt><dd>{snapshot?.workspaceId ?? "reserved"}</dd>
                <dt>Revision</dt><dd data-testid="server-revision">{snapshot?.revision ?? "—"}</dd>
                <dt>Results</dt><dd>{snapshot?.resultCount ?? "—"}</dd>
                <dt>Transport</dt><dd data-testid="server-transport">{snapshot?.transport ?? "pending"}</dd>
                <dt>Freshness</dt><dd>{snapshot?.freshness ?? "loading"}</dd>
              </dl>
            </EvidencePanel>
            <EvidencePanel aria-labelledby="client-state-title">
              <h2 id="client-state-title">MobX presentation state</h2>
              <dl>
                <dt>Theme</dt><dd data-testid="theme-id">{uiStore.themeId}</dd>
                <dt>Sidebar width</dt><dd data-testid="sidebar-width">{uiStore.sidebarWidth}px</dd>
                <dt>REST cancellation</dt><dd data-testid="cancel-state">{cancelState}</dd>
                <dt>Route identity</dt><dd>UI-AN-003</dd>
              </dl>
            </EvidencePanel>
          </Grid>
        </SpikeContent>
      </SpikeShell>
    </SemanticThemeBoundary>
  );
});

export function ArchitectureSpike({ fallbackHref }: { readonly fallbackHref: string }): React.JSX.Element {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: { retry: false, refetchOnWindowFocus: false },
    },
  }));
  return (
    <QueryClientProvider client={queryClient}>
      <SpikeWorkspace fallbackHref={fallbackHref} />
    </QueryClientProvider>
  );
}
