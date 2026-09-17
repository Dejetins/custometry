import { describe, expect, it } from "vitest";

import { chartCompilerLifecycle } from "../src/index";

describe("Chart compiler supported subset", () => {
  it("declares only the canonical line subset", () => {
    expect(chartCompilerLifecycle).toBe("line-v1");
  });
});
