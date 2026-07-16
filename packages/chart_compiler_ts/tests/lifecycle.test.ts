import { describe, expect, it } from "vitest";

import { chartCompilerLifecycle } from "../src/index";

describe("Chart compiler Foundation boundary", () => {
  it("does not claim an implementation before the ChartSpec stage", () => {
    expect(chartCompilerLifecycle).toBe("planned");
  });
});
