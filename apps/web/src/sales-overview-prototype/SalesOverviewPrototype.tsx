import {
  BarChart3,
  Bell,
  Building2,
  Calendar,
  ChevronDown,
  ChevronLeft,
  CircleHelp,
  Database,
  Ellipsis,
  FileText,
  Grid2X2,
  LayoutGrid,
  LineChart,
  LogOut,
  Package,
  PanelLeftClose,
  PanelLeftOpen,
  Search,
  Settings,
  ShieldCheck,
  Store,
  TrendingUp,
  UserRound,
  Users,
  X,
  type LucideIcon,
} from "lucide-react";
import {
  type CSSProperties,
  type PointerEvent as ReactPointerEvent,
  type Ref,
  useEffect,
  useRef,
  useState,
} from "react";
import { useLocation, useNavigate } from "react-router-dom";

import "./sales-overview-prototype.css";

type ChartMode = "chart" | "data";
type ChartType = "line" | "bar";
type ComparisonDisplay = "percentage" | "absolute";
type BreakdownMode = "channel" | "store" | "product";
type SidebarMode = "expanded" | "collapsed" | "hidden";
type FocusTarget = "revenue-trend" | "breakdown";

interface BreakdownRow {
  readonly label: string;
  readonly revenue: string;
  readonly contribution: string;
  readonly revenueDeltaPercent: string;
  readonly revenueDeltaAbsolute: string;
  readonly orders: string;
  readonly ordersDeltaPercent: string;
  readonly ordersDeltaAbsolute: string;
  readonly aov: string;
  readonly aovDeltaPercent: string;
  readonly aovDeltaAbsolute: string;
  readonly margin: string;
  readonly marginDelta: string;
}

const metrics = [
  { label: "Revenue", value: "₽2.48B", delta: "+12.4%", tone: "positive" },
  { label: "Orders", value: "1.84M", delta: "+8.7%", tone: "positive" },
  { label: "AOV", value: "₽1,348", delta: "+3.4%", tone: "positive" },
  { label: "Margin", value: "31.6%", delta: "−0.8 pp", tone: "negative" },
] as const;

const breakdownRows: Record<BreakdownMode, ReadonlyArray<BreakdownRow>> = {
  channel: [
    { label: "Online", revenue: "1,152,900,000", contribution: "46.5%", revenueDeltaPercent: "+13.6%", revenueDeltaAbsolute: "+138.0M", orders: "842,560", ordersDeltaPercent: "+9.3%", ordersDeltaAbsolute: "+71.7K", aov: "1,368", aovDeltaPercent: "+3.9%", aovDeltaAbsolute: "+51", margin: "32.1%", marginDelta: "−0.6 pp" },
    { label: "Mobile app", revenue: "768,400,000", contribution: "31.0%", revenueDeltaPercent: "+15.2%", revenueDeltaAbsolute: "+101.4M", orders: "520,310", ordersDeltaPercent: "+11.1%", ordersDeltaAbsolute: "+52.0K", aov: "1,476", aovDeltaPercent: "+3.7%", aovDeltaAbsolute: "+53", margin: "30.8%", marginDelta: "−1.0 pp" },
    { label: "In-store", revenue: "558,700,000", contribution: "22.5%", revenueDeltaPercent: "+7.4%", revenueDeltaAbsolute: "+38.5M", orders: "475,820", ordersDeltaPercent: "+5.8%", ordersDeltaAbsolute: "+26.1K", aov: "1,174", aovDeltaPercent: "+1.5%", aovDeltaAbsolute: "+17", margin: "31.8%", marginDelta: "−0.4 pp" },
    { label: "Total", revenue: "2,479,600,000", contribution: "100%", revenueDeltaPercent: "+12.4%", revenueDeltaAbsolute: "+273.6M", orders: "1,838,690", ordersDeltaPercent: "+8.7%", ordersDeltaAbsolute: "+147.2K", aov: "1,348", aovDeltaPercent: "+3.4%", aovDeltaAbsolute: "+44", margin: "31.6%", marginDelta: "−0.8 pp" },
  ],
  store: [
    { label: "Moscow Central", revenue: "812,400,000", contribution: "32.8%", revenueDeltaPercent: "+16.8%", revenueDeltaAbsolute: "+116.8M", orders: "574,320", ordersDeltaPercent: "+12.4%", ordersDeltaAbsolute: "+63.4K", aov: "1,414", aovDeltaPercent: "+3.9%", aovDeltaAbsolute: "+53", margin: "33.4%", marginDelta: "+0.2 pp" },
    { label: "Saint Petersburg", revenue: "706,200,000", contribution: "28.5%", revenueDeltaPercent: "+10.9%", revenueDeltaAbsolute: "+69.4M", orders: "518,760", ordersDeltaPercent: "+7.5%", ordersDeltaAbsolute: "+36.2K", aov: "1,361", aovDeltaPercent: "+3.2%", aovDeltaAbsolute: "+42", margin: "31.2%", marginDelta: "−0.7 pp" },
    { label: "Regional network", revenue: "961,000,000", contribution: "38.7%", revenueDeltaPercent: "+10.0%", revenueDeltaAbsolute: "+87.4M", orders: "745,610", ordersDeltaPercent: "+6.8%", ordersDeltaAbsolute: "+47.6K", aov: "1,289", aovDeltaPercent: "+2.9%", aovDeltaAbsolute: "+36", margin: "30.3%", marginDelta: "−1.3 pp" },
    { label: "Total", revenue: "2,479,600,000", contribution: "100%", revenueDeltaPercent: "+12.4%", revenueDeltaAbsolute: "+273.6M", orders: "1,838,690", ordersDeltaPercent: "+8.7%", ordersDeltaAbsolute: "+147.2K", aov: "1,348", aovDeltaPercent: "+3.4%", aovDeltaAbsolute: "+44", margin: "31.6%", marginDelta: "−0.8 pp" },
  ],
  product: [
    { label: "Home electronics", revenue: "984,100,000", contribution: "39.7%", revenueDeltaPercent: "+14.8%", revenueDeltaAbsolute: "+126.8M", orders: "492,810", ordersDeltaPercent: "+9.1%", ordersDeltaAbsolute: "+41.1K", aov: "1,997", aovDeltaPercent: "+5.2%", aovDeltaAbsolute: "+99", margin: "29.8%", marginDelta: "−0.5 pp" },
    { label: "Home & kitchen", revenue: "781,500,000", contribution: "31.5%", revenueDeltaPercent: "+11.6%", revenueDeltaAbsolute: "+81.2M", orders: "671,420", ordersDeltaPercent: "+8.4%", ordersDeltaAbsolute: "+52.0K", aov: "1,164", aovDeltaPercent: "+2.9%", aovDeltaAbsolute: "+33", margin: "34.2%", marginDelta: "−0.9 pp" },
    { label: "Personal care", revenue: "714,000,000", contribution: "28.8%", revenueDeltaPercent: "+10.1%", revenueDeltaAbsolute: "+65.6M", orders: "674,460", ordersDeltaPercent: "+8.6%", ordersDeltaAbsolute: "+54.1K", aov: "1,059", aovDeltaPercent: "+1.4%", aovDeltaAbsolute: "+15", margin: "31.1%", marginDelta: "−1.1 pp" },
    { label: "Total", revenue: "2,479,600,000", contribution: "100%", revenueDeltaPercent: "+12.4%", revenueDeltaAbsolute: "+273.6M", orders: "1,838,690", ordersDeltaPercent: "+8.7%", ordersDeltaAbsolute: "+147.2K", aov: "1,348", aovDeltaPercent: "+3.4%", aovDeltaAbsolute: "+44", margin: "31.6%", marginDelta: "−0.8 pp" },
  ],
};

const breakdownLabels: Record<BreakdownMode, { readonly title: string; readonly column: string }> = {
  channel: { title: "By channel", column: "Channel" },
  store: { title: "By store", column: "Store" },
  product: { title: "By product", column: "Product group" },
};

const sidebarGroups: ReadonlyArray<{
  readonly label: string;
  readonly items: ReadonlyArray<{ readonly label: string; readonly icon: LucideIcon; readonly active?: boolean }>;
}> = [
  { label: "WORKSPACE", items: [{ label: "Overview", icon: LayoutGrid }, { label: "Data", icon: Database }] },
  {
    label: "ANALYTICS",
    items: [
      { label: "Sales", icon: LineChart, active: true },
      { label: "Customers", icon: Users },
      { label: "Products", icon: Package },
      { label: "Forecasts", icon: TrendingUp },
    ],
  },
  { label: "OUTPUT", items: [{ label: "Reports", icon: FileText }] },
  { label: "ADMIN", items: [{ label: "Operations", icon: Building2 }, { label: "Settings", icon: Settings }] },
];

const contextFilters: ReadonlyArray<{ readonly label: string; readonly value: string; readonly icon: LucideIcon }> = [
  { label: "Period", value: "Jan–Jun 2026", icon: Calendar },
  { label: "Comparison", value: "vs LY", icon: LineChart },
  { label: "Stores", value: "All stores", icon: Store },
  { label: "Channels", value: "All channels", icon: Grid2X2 },
  { label: "Audience", value: "Executive", icon: Users },
];

function readSidebarMode(): SidebarMode {
  const stored = window.localStorage.getItem("custometry.sales.sidebar.mode");
  return stored === "collapsed" || stored === "hidden" ? stored : "expanded";
}

function readSidebarWidth(): number {
  const stored = Number(window.localStorage.getItem("custometry.sales.sidebar.width"));
  return Number.isFinite(stored) && stored >= 208 && stored <= 320 ? stored : 224;
}

function IconButton({
  buttonRef,
  children,
  expanded,
  label,
  onClick,
  pressed,
  quiet = false,
}: {
  readonly buttonRef?: Ref<HTMLButtonElement>;
  readonly children: React.ReactNode;
  readonly expanded?: boolean;
  readonly label: string;
  readonly onClick?: () => void;
  readonly pressed?: boolean;
  readonly quiet?: boolean;
}): React.JSX.Element {
  return (
    <button
      aria-expanded={expanded}
      aria-label={label}
      aria-pressed={pressed}
      className={quiet ? "sales-icon-button sales-icon-button--quiet" : "sales-icon-button"}
      onClick={onClick}
      ref={buttonRef}
      title={label}
      type="button"
    >
      {children}
    </button>
  );
}

function ExactIcon({ name }: { readonly name: "bookmark" | "context-actions" | "download" | "expand" | "filter" | "link" | "mail" }): React.JSX.Element {
  return <img alt="" aria-hidden="true" className="sales-exact-icon" src={`/ui-an-003-prototype/${name}.svg`} />;
}

function ChartPlot({ mode }: { readonly mode: ChartMode }): React.JSX.Element {
  if (mode === "data") {
    return (
      <div className="sales-chart-data" aria-label="Revenue monthly data">
        <div className="sales-chart-data__header"><span>Month</span><span>Revenue</span><span>vs LY</span></div>
        {[
          ["Jan 2026", "₽310M", "+34.8%"], ["Feb 2026", "₽350M", "+40.0%"], ["Mar 2026", "₽520M", "+30.0%"],
          ["Apr 2026", "₽390M", "+44.4%"], ["May 2026", "₽510M", "+45.7%"], ["Jun 2026", "₽550M", "+41.0%"],
        ].map(([month, revenue, delta]) => (
          <div className="sales-chart-data__row" key={month}><span>{month}</span><strong>{revenue}</strong><span>{delta}</span></div>
        ))}
      </div>
    );
  }

  return (
    <div className="sales-chart-visual" aria-label="Revenue trend chart">
      <span className="sales-chart-unit">Revenue (₽)</span>
      <div className="sales-y-labels" aria-hidden="true"><span>600M</span><span>450M</span><span>300M</span><span>150M</span><span>0</span></div>
      <div className="sales-grid-lines" aria-hidden="true"><i /><i /><i /><i /><i /></div>
      <img className="sales-revenue-line" src="/ui-an-003-prototype/revenue.svg" alt="" />
      <img className="sales-revenue-line sales-revenue-line--comparison" src="/ui-an-003-prototype/revenue-ly.svg" alt="" />
      <div className="sales-x-labels" aria-hidden="true"><span>Jan 2026</span><span>Feb 2026</span><span>Mar 2026</span><span>Apr 2026</span><span>May 2026</span><span>Jun 2026</span></div>
      <div className="sales-chart-legend"><span><i />Revenue</span><span><i />Revenue (LY)</span></div>
    </div>
  );
}

function ResultTrustTrigger({ onClick }: { readonly onClick: () => void }): React.JSX.Element {
  return (
    <button
      aria-label="Result trust: Retail sales v24. Trusted. Last updated 1 August 2026 at 12:42"
      className="sales-chart-meta"
      onClick={onClick}
      type="button"
    >
      <ShieldCheck aria-hidden="true" size={14} />
      <span>Retail sales v24</span>
      <img src="/ui-an-003-prototype/trust-status.svg" alt="" />
      <strong>Trusted</strong>
      <time dateTime="2026-08-01T12:42:00+03:00">Updated 1 Aug, 12:42</time>
    </button>
  );
}

function ComparisonToggle({ display, onChange }: { readonly display: ComparisonDisplay; readonly onChange: (display: ComparisonDisplay) => void }): React.JSX.Element {
  return (
    <div className="sales-compare-mode" role="group" aria-label="Comparison display">
      <button aria-label="Show percentage comparison" aria-pressed={display === "percentage"} onClick={() => onChange("percentage")} type="button">%</button>
      <button aria-label="Show absolute comparison" aria-pressed={display === "absolute"} onClick={() => onChange("absolute")} type="button">Abs</button>
    </div>
  );
}

function BreakdownTable({ display, mode }: { readonly display: ComparisonDisplay; readonly mode: BreakdownMode }): React.JSX.Element {
  const rows = breakdownRows[mode];
  return (
    <div className="sales-table-scroll">
      <div className="sales-table" role="table" aria-label={breakdownLabels[mode].title}>
        <div className="sales-table__row sales-table__row--head" role="row">
          <span>{breakdownLabels[mode].column}</span><span>Revenue (₽)</span><span>Contribution</span><span>vs LY</span><span>Orders</span><span>vs LY</span><span>AOV (₽)</span><span>vs LY</span><span>Margin</span><span>vs LY</span>
        </div>
        {rows.map((row, rowIndex) => {
          const cells = [
            row.label,
            row.revenue,
            row.contribution,
            display === "percentage" ? row.revenueDeltaPercent : row.revenueDeltaAbsolute,
            row.orders,
            display === "percentage" ? row.ordersDeltaPercent : row.ordersDeltaAbsolute,
            row.aov,
            display === "percentage" ? row.aovDeltaPercent : row.aovDeltaAbsolute,
            row.margin,
            row.marginDelta,
          ];
          return (
            <div className={rowIndex === rows.length - 1 ? "sales-table__row sales-table__row--total" : "sales-table__row"} key={row.label} role="row">
              {cells.map((cell, index) => <span className={index === 3 || index === 5 || index === 7 ? "sales-tone--positive" : index === 9 ? "sales-tone--negative" : ""} key={`${row.label}-${index}`}>{cell}</span>)}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function TrustDrawer({ onClose }: { readonly onClose: () => void }): React.JSX.Element {
  return (
    <aside className="sales-trust-drawer" aria-label="Result trust details">
      <header><div><span>RESULT TRUST</span><h2>Trusted result</h2></div><IconButton label="Close result trust" onClick={onClose} quiet><X aria-hidden="true" size={18} /></IconButton></header>
      <div className="sales-trust-status"><img src="/ui-an-003-prototype/trust-status.svg" alt="" /><strong>All required checks passed</strong><span>Updated 1 Aug 2026, 12:42 MSK</span></div>
      <dl>
        <div><dt>Dataset</dt><dd>Retail sales v24</dd></div>
        <div><dt>As of</dt><dd>31 Jul 2026</dd></div>
        <div><dt>Freshness</dt><dd>Within 24-hour SLA</dd></div>
        <div><dt>Quality</dt><dd>98.7% · no blocking rules</dd></div>
        <div><dt>Grain</dt><dd>Order item · daily</dd></div>
        <div><dt>Context</dt><dd>All stores · all channels · Executive</dd></div>
        <div><dt>Currency / timezone</dt><dd>RUB · Europe/Moscow</dd></div>
        <div><dt>Lineage</dt><dd>POS + mobile + web → certified sales mart</dd></div>
      </dl>
      <section><h3>Limitations</h3><p>Returns posted after the as-of date appear in the next refresh. Margin excludes pending supplier rebates.</p></section>
    </aside>
  );
}

export function SalesOverviewPrototype(): React.JSX.Element {
  const location = useLocation();
  const navigate = useNavigate();
  const [chartMode, setChartMode] = useState<ChartMode>("chart");
  const [chartType, setChartType] = useState<ChartType>("line");
  const [comparisonDisplay, setComparisonDisplay] = useState<ComparisonDisplay>("percentage");
  const [breakdownMode, setBreakdownMode] = useState<BreakdownMode>("channel");
  const [breakdownOpen, setBreakdownOpen] = useState(false);
  const [filterOpen, setFilterOpen] = useState(false);
  const [inspectorOpen, setInspectorOpen] = useState(() => window.innerWidth >= 1200);
  const [saved, setSaved] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const [noticeOpen, setNoticeOpen] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);
  const [userOpen, setUserOpen] = useState(false);
  const [trustOpen, setTrustOpen] = useState(false);
  const [sidebarMode, setSidebarMode] = useState<SidebarMode>(readSidebarMode);
  const [sidebarWidth, setSidebarWidth] = useState(readSidebarWidth);
  const [viewportWidth, setViewportWidth] = useState(() => window.innerWidth);
  const [resizing, setResizing] = useState(false);
  const resizeStart = useRef({ x: 0, width: 224 });
  const chartFocusTrigger = useRef<HTMLButtonElement>(null);
  const tableFocusTrigger = useRef<HTMLButtonElement>(null);
  const returnFocusTarget = useRef<FocusTarget | null>(null);
  const focusHeading = useRef<HTMLHeadingElement>(null);
  const focusParam = new URLSearchParams(location.search).get("focus");
  const focusTarget: FocusTarget | null = focusParam === "revenue-trend" || focusParam === "breakdown" ? focusParam : null;

  const announce = (message: string): void => {
    setToast(message);
    window.setTimeout(() => setToast(null), 1800);
  };

  const setAndPersistSidebarMode = (mode: SidebarMode): void => {
    setSidebarMode(mode);
    window.localStorage.setItem("custometry.sales.sidebar.mode", mode);
  };

  const openFocus = (target: FocusTarget): void => {
    returnFocusTarget.current = target;
    const search = new URLSearchParams(location.search);
    search.set("focus", target);
    navigate({ pathname: location.pathname, search: search.toString() });
  };

  const closeFocus = (): void => {
    const search = new URLSearchParams(location.search);
    search.delete("focus");
    navigate({ pathname: location.pathname, search: search.toString() });
  };

  useEffect(() => {
    const onResize = (): void => setViewportWidth(window.innerWidth);
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  useEffect(() => {
    if (viewportWidth < 900 && sidebarMode !== "hidden") setAndPersistSidebarMode("hidden");
    else if (viewportWidth < 1200 && sidebarMode === "expanded") setAndPersistSidebarMode("collapsed");
    if (viewportWidth < 1200) setInspectorOpen(false);
  }, [sidebarMode, viewportWidth]);

  useEffect(() => {
    window.localStorage.setItem("custometry.sales.sidebar.width", String(sidebarWidth));
  }, [sidebarWidth]);

  useEffect(() => {
    if (!resizing) return undefined;
    const onMove = (event: PointerEvent): void => {
      const next = Math.min(320, Math.max(208, resizeStart.current.width + event.clientX - resizeStart.current.x));
      setSidebarWidth(next);
    };
    const onUp = (): void => setResizing(false);
    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", onUp, { once: true });
    return () => {
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
    };
  }, [resizing]);

  useEffect(() => {
    if (focusTarget) window.requestAnimationFrame(() => focusHeading.current?.focus());
    else if (returnFocusTarget.current) {
      const target = returnFocusTarget.current;
      returnFocusTarget.current = null;
      window.requestAnimationFrame(() => (target === "revenue-trend" ? chartFocusTrigger : tableFocusTrigger).current?.focus());
    }
  }, [focusTarget]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent): void => {
      if (event.key !== "Escape") return;
      if (trustOpen) setTrustOpen(false);
      else if (focusTarget) closeFocus();
      else {
        setFilterOpen(false);
        setBreakdownOpen(false);
        setNoticeOpen(false);
        setHelpOpen(false);
        setUserOpen(false);
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [focusTarget, location.search, trustOpen]);

  const rootStyle = { "--sales-sidebar-width": `${sidebarWidth}px` } as CSSProperties;
  const rootClasses = [
    "sales-prototype",
    !inspectorOpen && "sales-prototype--inspector-closed",
    `sales-prototype--sidebar-${sidebarMode}`,
    focusTarget && "sales-prototype--focus",
    resizing && "sales-prototype--resizing",
  ].filter(Boolean).join(" ");

  if (focusTarget) {
    return (
      <div className={rootClasses} data-testid="sales-html-prototype" style={rootStyle}>
        <main className="sales-focus" aria-label="Sales Focus Explore">
          <header className="sales-focus__header">
            <div><span>FOCUS / EXPLORE</span><h1 ref={focusHeading} tabIndex={-1}>{focusTarget === "revenue-trend" ? "Revenue trend" : breakdownLabels[breakdownMode].title}</h1><p>Jan–Jun 2026&nbsp; · &nbsp;vs LY</p></div>
            <div className="sales-focus__actions">
              <ResultTrustTrigger onClick={() => setTrustOpen(true)} />
              <button className="sales-control" onClick={() => announce("Export is disabled in this prototype")} type="button"><ExactIcon name="download" /><span>Export</span></button>
              <IconButton label="Close Focus Explore" onClick={closeFocus}><X aria-hidden="true" size={18} /></IconButton>
            </div>
          </header>
          <div className="sales-focus__filters" aria-label="Applied context">
            <span>Period · Jan–Jun 2026</span><span>Comparison · vs LY</span><span>Stores · All</span><span>Channels · All</span><span>Audience · Executive</span>
            <button onClick={() => announce("Draft filters are planned for production")} type="button">Add filter</button>
          </div>
          {focusTarget === "revenue-trend" ? (
            <section className="sales-focus__content sales-focus__content--chart" aria-label="Focused revenue trend">
              <div className="sales-focus__toolbar">
                <button className={chartMode === "chart" ? "sales-text-tab sales-text-tab--active" : "sales-text-tab"} onClick={() => setChartMode("chart")} type="button">Chart</button>
                <button className={chartMode === "data" ? "sales-text-tab sales-text-tab--active" : "sales-text-tab"} onClick={() => setChartMode("data")} type="button">Data</button>
                <button className="sales-control sales-period" type="button"><ChevronDown aria-hidden="true" size={16} /><span>Monthly</span></button>
                <div className="sales-chart-type" role="group" aria-label="Chart type">
                  <button aria-label="Line chart" aria-pressed={chartType === "line"} onClick={() => setChartType("line")} type="button"><LineChart aria-hidden="true" size={16} /></button>
                  <button aria-label="Bar chart" aria-pressed={chartType === "bar"} onClick={() => setChartType("bar")} type="button"><BarChart3 aria-hidden="true" size={16} /></button>
                </div>
              </div>
              <ChartPlot mode={chartMode} />
            </section>
          ) : (
            <section className="sales-focus__content sales-focus__content--table" aria-label="Focused sales breakdown">
              <div className="sales-focus__toolbar"><ComparisonToggle display={comparisonDisplay} onChange={setComparisonDisplay} /></div>
              <BreakdownTable display={comparisonDisplay} mode={breakdownMode} />
            </section>
          )}
        </main>
        {trustOpen && <TrustDrawer onClose={() => setTrustOpen(false)} />}
        {toast && <div className="sales-toast" role="status">{toast}</div>}
      </div>
    );
  }

  return (
    <div className={rootClasses} data-testid="sales-html-prototype" style={rootStyle}>
      {sidebarMode !== "hidden" && (
        <aside className="sales-sidebar" aria-label="Workspace navigation">
          <div className="sales-sidebar__header">
            <div className="sales-sidebar__identity"><strong>CUSTOMETRY</strong><span>Northwind Retail <ChevronDown aria-hidden="true" size={14} /></span></div>
            <IconButton label={sidebarMode === "expanded" ? "Collapse sidebar" : "Expand sidebar"} onClick={() => setAndPersistSidebarMode(sidebarMode === "expanded" ? "collapsed" : "expanded")} quiet>
              {sidebarMode === "expanded" ? <PanelLeftClose aria-hidden="true" size={17} /> : <PanelLeftOpen aria-hidden="true" size={17} />}
            </IconButton>
          </div>
          <div className="sales-sidebar__utilities" aria-label="Sidebar utilities">
            <button aria-label="Search" className="sales-sidebar-utility" onClick={() => announce("Command palette is planned for production")} title="Search" type="button"><Search aria-hidden="true" size={16} /><span>Search</span><kbd aria-hidden="true">⌘K</kbd></button>
            <div className="sales-notification-wrap">
              <button aria-expanded={noticeOpen} aria-label="Notifications" className="sales-sidebar-utility" onClick={() => setNoticeOpen((open) => !open)} title="Notifications" type="button"><Bell aria-hidden="true" size={16} /><span>Notifications</span><img aria-hidden="true" className="sales-utility-indicator" src="/ui-an-003-prototype/unread-indicator.svg" alt="" /></button>
              {noticeOpen && <div className="sales-popover sales-popover--notice"><strong>Notifications</strong><span>No new data alerts</span></div>}
            </div>
          </div>
          <nav className="sales-sidebar__nav" aria-label="Primary navigation">
            {sidebarGroups.map((group) => (
              <div className="sales-nav-group" key={group.label}>
                <span className="sales-nav-group__label">{group.label}</span>
                {group.items.map(({ label, icon: Icon, active }) => (
                  <button aria-current={active ? "page" : undefined} aria-label={label} className={active ? "sales-nav-item sales-nav-item--active" : "sales-nav-item"} key={label} title={label} type="button"><Icon aria-hidden="true" size={16} /><span>{label}</span></button>
                ))}
              </div>
            ))}
          </nav>
          <div className="sales-sidebar__footer">
            <div className="sales-footer-action-wrap">
              <button aria-expanded={helpOpen} aria-label="Help" className="sales-sidebar-utility" onClick={() => setHelpOpen((open) => !open)} title="Help" type="button"><CircleHelp aria-hidden="true" size={16} /><span>Help</span></button>
              {helpOpen && <div className="sales-popover sales-popover--footer"><strong>Help</strong><button onClick={() => announce("Keyboard shortcuts reference")} type="button">Keyboard shortcuts</button><button onClick={() => announce("Documentation is not linked in this prototype")} type="button">Documentation</button></div>}
            </div>
            <div className="sales-footer-action-wrap">
              <button aria-expanded={userOpen} aria-label="User menu" className="sales-sidebar-utility sales-user-button" onClick={() => setUserOpen((open) => !open)} title="User menu" type="button"><span className="sales-user-avatar" aria-hidden="true">DD</span><span>Daniil Degtyarev</span><ChevronDown aria-hidden="true" size={14} /></button>
              {userOpen && <div className="sales-popover sales-popover--footer"><strong>Daniil Degtyarev</strong><button onClick={() => announce("Profile is disabled in this prototype")} type="button"><UserRound aria-hidden="true" size={15} />Profile</button><button onClick={() => announce("Sign out is disabled in this prototype")} type="button"><LogOut aria-hidden="true" size={15} />Sign out</button></div>}
            </div>
            <button className="sales-hide-sidebar" onClick={() => setAndPersistSidebarMode("hidden")} title="Hide sidebar" type="button"><ChevronLeft aria-hidden="true" size={15} /><span>Hide sidebar</span></button>
          </div>
          {sidebarMode === "expanded" && (
            <div
              aria-label="Resize sidebar"
              aria-orientation="vertical"
              aria-valuemax={320}
              aria-valuemin={208}
              aria-valuenow={Math.round(sidebarWidth)}
              className="sales-sidebar-resizer"
              onDoubleClick={() => setSidebarWidth(224)}
              onKeyDown={(event) => {
                if (event.key === "ArrowLeft") setSidebarWidth((width) => Math.max(208, width - 8));
                if (event.key === "ArrowRight") setSidebarWidth((width) => Math.min(320, width + 8));
                if (event.key === "Home") setSidebarWidth(224);
              }}
              onPointerDown={(event: ReactPointerEvent<HTMLDivElement>) => {
                resizeStart.current = { x: event.clientX, width: sidebarWidth };
                setResizing(true);
              }}
              role="separator"
              tabIndex={0}
            />
          )}
        </aside>
      )}

      <main className="sales-application" aria-label="Sales overview prototype">
        <header className="sales-header">
          <div className="sales-header__title">
            {sidebarMode === "hidden" && <IconButton label="Show navigation" onClick={() => setAndPersistSidebarMode(viewportWidth < 1200 ? "collapsed" : "expanded")}><PanelLeftOpen aria-hidden="true" size={17} /></IconButton>}
            <div><h1>Sales overview</h1><p>Analytics&nbsp; / &nbsp;Sales</p></div>
          </div>
          <div className="sales-header__actions">
            <IconButton expanded={inspectorOpen} label={inspectorOpen ? "Hide context panel" : "Show context panel"} onClick={() => setInspectorOpen((open) => !open)}><ExactIcon name="context-actions" /></IconButton>
            <IconButton label="More page actions" quiet><Ellipsis aria-hidden="true" size={18} /></IconButton>
          </div>
        </header>

        <section className="sales-kpis" aria-label="Sales metrics">
          {metrics.map((metric) => <div className="sales-kpi" key={metric.label}><span>{metric.label}</span><div><strong>{metric.value}</strong><em className={`sales-tone--${metric.tone}`}>{metric.delta}</em></div></div>)}
        </section>

        <section className="sales-chart-card" aria-labelledby="revenue-trend-title">
          <h2 id="revenue-trend-title">Revenue trend</h2>
          <div className="sales-chart-toolbar" aria-label="Chart controls">
            <button aria-label="Show chart view" className={chartMode === "chart" ? "sales-text-tab sales-text-tab--active" : "sales-text-tab"} onClick={() => setChartMode("chart")} type="button">Chart</button>
            <button aria-label="Show data view" className={chartMode === "data" ? "sales-text-tab sales-text-tab--active" : "sales-text-tab"} onClick={() => setChartMode("data")} type="button">Data</button>
            <button className="sales-control sales-period" type="button"><ChevronDown aria-hidden="true" size={16} /><span>Monthly</span></button>
            <div className="sales-chart-type" role="group" aria-label="Chart type">
              <button aria-label="Line chart" aria-pressed={chartType === "line"} onClick={() => setChartType("line")} type="button"><LineChart aria-hidden="true" size={16} /></button>
              <button aria-label="Bar chart" aria-pressed={chartType === "bar"} onClick={() => setChartType("bar")} type="button"><BarChart3 aria-hidden="true" size={16} /></button>
            </div>
            <div className="sales-filter-wrap">
              <IconButton label="Filter view" onClick={() => setFilterOpen((open) => !open)} pressed={filterOpen}><ExactIcon name="filter" /></IconButton>
              {filterOpen && <div className="sales-popover sales-popover--filter"><strong>Filter view</strong><button type="button" onClick={() => announce("Channel filter selected")}>Channel · All</button><button type="button" onClick={() => announce("Store filter selected")}>Store · All</button></div>}
            </div>
            <button className={saved ? "sales-control sales-save sales-save--active" : "sales-control sales-save"} onClick={() => setSaved((value) => !value)} type="button"><ExactIcon name="bookmark" /><span>{saved ? "Saved" : "Save view"}</span></button>
            <IconButton buttonRef={chartFocusTrigger} label="Expand chart" onClick={() => openFocus("revenue-trend")}><ExactIcon name="expand" /></IconButton>
          </div>
          <ChartPlot mode={chartMode} />
          <ResultTrustTrigger onClick={() => setTrustOpen(true)} />
        </section>

        <section className="sales-table-card" aria-labelledby="sales-breakdown-title">
          <div className="sales-table-card__header">
            <div className="sales-breakdown-selector">
              <h2 id="sales-breakdown-title"><button aria-expanded={breakdownOpen} onClick={() => setBreakdownOpen((open) => !open)} type="button">{breakdownLabels[breakdownMode].title}<ChevronDown aria-hidden="true" size={15} /></button></h2>
              {breakdownOpen && <div className="sales-popover sales-popover--breakdown">{(["channel", "store", "product"] as const).map((mode) => <button aria-pressed={breakdownMode === mode} key={mode} onClick={() => { setBreakdownMode(mode); setBreakdownOpen(false); }} type="button">{breakdownLabels[mode].title}</button>)}</div>}
            </div>
            <div>
              <ComparisonToggle display={comparisonDisplay} onChange={setComparisonDisplay} />
              <IconButton label="Download table" onClick={() => announce("Download is disabled in this prototype")}><ExactIcon name="download" /></IconButton>
              <IconButton buttonRef={tableFocusTrigger} label="Expand table" onClick={() => openFocus("breakdown")}><ExactIcon name="expand" /></IconButton>
            </div>
          </div>
          <BreakdownTable display={comparisonDisplay} mode={breakdownMode} />
        </section>

        {inspectorOpen && (
          <aside className="sales-inspector" aria-label="Context panel">
            <div className="sales-inspector__header"><h2>Context</h2></div>
            <span className="sales-section-label">ON THIS PAGE</span>
            <nav className="sales-page-sections" aria-label="On this page"><button type="button">Overview</button><button className="sales-page-section--active" type="button">Revenue trend</button><button type="button">{breakdownLabels[breakdownMode].title}</button></nav>
            <div className="sales-share-section"><span className="sales-section-label">SHARE</span><button type="button" onClick={() => announce("Prototype link ready to copy")}><ExactIcon name="link" />Copy link</button><button type="button" onClick={() => announce("Email sending is disabled in this prototype")}><ExactIcon name="mail" />Send by email</button></div>
            <span className="sales-section-label sales-section-label--view">VIEW</span>
            <div className="sales-context-filters">{contextFilters.map(({ label, value, icon: Icon }) => <button className="sales-context-filter" key={label} onClick={() => announce(`${label}: ${value}`)} type="button"><Icon aria-hidden="true" size={16} /><span><small>{label}</small><strong>{value}</strong></span><ChevronDown aria-hidden="true" size={14} /></button>)}</div>
          </aside>
        )}
      </main>
      {trustOpen && <TrustDrawer onClose={() => setTrustOpen(false)} />}
      {toast && <div className="sales-toast" role="status">{toast}</div>}
    </div>
  );
}
