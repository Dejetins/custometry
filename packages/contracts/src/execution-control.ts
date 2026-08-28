// Generated from execution-control OpenAPI. Do not edit.
export const executionControlContractDigest = "59bd5afa5c6653a33ddfc44f53a331888deacb8769b1f5c25326f5d1e8cfeebc" as const;
export const executionControlOperations = {
  "cancel_operator_run": { method: "POST", path: "/runs/{run_id}/cancel" },
  "get_operator_queue_summary": { method: "GET", path: "/queue-summary" },
  "get_operator_run": { method: "GET", path: "/runs/{run_id}" },
  "list_operator_runs": { method: "GET", path: "/runs" },
  "retry_operator_run": { method: "POST", path: "/runs/{run_id}/retry" },
} as const;
export const executionControlSchemaNames = ["AttemptResponse","CancelRequest","HTTPValidationError","QueueSummaryResponse","RetryRequest","RunDetailResponse","RunListResponse","RunResponse","ValidationError"] as const;
