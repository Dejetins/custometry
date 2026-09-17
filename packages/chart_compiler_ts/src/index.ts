/** Only the MS-003 canonical daily revenue line subset is implemented. */
export const chartCompilerLifecycle = "line-v1" as const;
export { compileLineChart, ChartCompileError } from "./line";
export type { DailyRow, LineData, LineRenderProfile } from "./line";

export interface ChartSpecEnvelope {
  readonly schemaVersion: string;
  readonly chartType: string;
  readonly payload: Readonly<Record<string, unknown>>;
}
