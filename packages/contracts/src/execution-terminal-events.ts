// Generated from execution-terminal-event.schema.json. Do not edit.
export const executionTerminalEventContractDigest = "e32454590a06399c5ff20fd011d283cf72ed8cd43a5128745c2e76637f094018" as const;
export const executionTerminalEventVersion = "1.0.0" as const;
export type ExecutionTerminalEventType =
  | "execution.run.failed"
  | "execution.run.stuck"
  | "execution.run.recovered";
export interface ExecutionTerminalEventV1 {
  event_id: string;
  event_type: ExecutionTerminalEventType;
  event_version: "1.0.0";
  source_owner: "execution";
  workspace_id: string;
  resource_type: "run";
  resource_id: string;
  run_id: string;
  attempt_id: string;
  retry_of_run_id: string | null;
  retry_of_attempt_id: string | null;
  status_code: "FAILED" | "STUCK" | "RECOVERED";
  reason_code: string;
  severity: "info" | "warning" | "critical";
  category: "execution";
  occurred_at: string;
  message_code: "RUN_FAILED" | "RUN_STUCK" | "RUN_RECOVERED";
  message_parameters: Readonly<Record<string, string>>;
  group_key: string;
  route_id: "UI-OPS-002";
  route_parameters: Readonly<Record<string, string>>;
  trace_id: string | null;
}
