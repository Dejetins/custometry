/**
 * Foundation boundary for the future versioned ChartSpec compiler.
 *
 * No compile function is exported yet: returning placeholder ECharts options would
 * create a false core contract before the ChartSpec stage is accepted.
 */
export const chartCompilerLifecycle = "planned" as const;

export interface ChartSpecEnvelope {
  readonly schemaVersion: string;
  readonly chartType: string;
  readonly payload: Readonly<Record<string, unknown>>;
}
