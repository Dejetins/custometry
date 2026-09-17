import { describe, expect, it } from "vitest";
import fixture from "./canonical-line.fixture.json";
import { ChartCompileError, compileLineChart, type LineData, type LineRenderProfile } from "../src/index";

const profile: LineRenderProfile = { locale: "ru", primary: "#62B6CE", comparison: "#98A2AA", text: "#E5E5E7", grid: "#292B2E" };
const compile = (spec: unknown = fixture.spec, data: LineData = fixture.data) => compileLineChart(spec, data, profile);

describe("S03 canonical daily line consumer", () => {
  it("compiles the provider-produced fixture and keeps exact table strings and identities", () => {
    const before = JSON.stringify(fixture);
    const compiled = compile();
    expect(compiled.option.series[0].data).toEqual([1.25, null]);
    expect(compiled.table.map((row) => row.net_revenue)).toEqual(["1.25", null]);
    expect(compiled.artifactHash).toBe(fixture.data.artifactHash);
    expect(compiled.metricHash).toBe(fixture.data.metricHash);
    expect(compiled.unit).toBe("EUR");
    expect(JSON.stringify(fixture)).toBe(before);
  });

  it("aligns the previous year by calendar date across a leap day and preserves the full table", () => {
    const compiled = compile();
    expect(compiled.option.series[1].data).toEqual([2.5, 3.75]);
    expect(compiled.comparisonTable?.map((row) => row.net_revenue)).toEqual(["2.50", "999.00", "3.75"]);
    expect(compiled.option.series[1].lineStyle.type).toBe("dashed");
  });

  it("preserves high precision and zero without aggregating or filling nulls", () => {
    const data = structuredClone(fixture.data);
    data.daily[0].net_revenue = "0.12345678901234567890123456789";
    data.daily[1].net_revenue = "0";
    const compiled = compile(fixture.spec, data);
    expect(compiled.table[0].net_revenue).toBe(data.daily[0].net_revenue);
    expect(compiled.option.series[0].data[1]).toBe(0);
    expect(compiled.option.series[0].connectNulls).toBe(false);
  });

  it("localizes display without changing data and uses no HTML tooltip", () => {
    const ru = compile();
    const en = compileLineChart(fixture.spec, fixture.data, { ...profile, locale: "en" });
    expect(ru.option.series[0].name).toBe("Текущий период");
    expect(en.option.series[0].name).toBe("Current period");
    expect(en.table).toEqual(ru.table);
    expect(en.option.tooltip.renderMode).toBe("richText");
  });

  it("supports a disabled comparison and a fully empty current result without invented values", () => {
    const spec = structuredClone(fixture.spec);
    spec.series = spec.series.slice(0, 1);
    const noComparison = { ...spec, source_binding: { ...spec.source_binding, comparison_artifact_id: null } };
    const compiled = compile(noComparison, { ...fixture.data, comparison: null });
    expect(compiled.option.series).toHaveLength(1);
    expect(compiled.comparisonTable).toBeNull();
    const empty = compile({ ...noComparison, chart_data: { ...spec.chart_data, row_count: 0 } }, { ...fixture.data, comparison: null, daily: [] });
    expect(empty.table).toEqual([]);
    expect(empty.option.series[0].data).toEqual([]);
  });

  it.each([
    ["option", { tooltip: { formatter: "<b>unsafe</b>" } }],
    ["chart_type", "bar"], ["schema_version", "2.0.0"],
    ["title_override", "<script>unsafe</script>"],
    ["annotations", [{ url: "https://example.invalid" }]],
    ["formatter", () => "unsafe"],
  ])("rejects unsupported root field/value %s", (key, value) => {
    expect(() => compile({ ...fixture.spec, [key]: value })).toThrow(ChartCompileError);
  });

  it.each(["source_binding", "chart_data", "accessibility", "interaction", "visual_semantics", "access_policy"])("rejects unknown nested fields in %s", (key) => {
    const spec = structuredClone(fixture.spec) as Record<string, unknown>;
    spec[key] = { ...(spec[key] as object), custom: "extra" };
    expect(() => compile(spec)).toThrow(ChartCompileError);
  });

  it.each(["workspaceId", "ownerPrincipalId", "artifactId", "artifactHash", "metricVersionId", "metricHash", "policyHash"] as const)("rejects a mismatched %s", (key) => {
    const data = { ...fixture.data, [key]: key.endsWith("Hash") ? "c".repeat(64) : "22222222-2222-4222-8222-222222222222" };
    expect(() => compile(fixture.spec, data)).toThrow(ChartCompileError);
  });

  it("rejects wrong metric unit and extra measure fields", () => {
    const spec = structuredClone(fixture.spec);
    spec.measures[0].unit = "SEK";
    expect(() => compile(spec)).toThrow(ChartCompileError);
    expect(() => compile({ ...fixture.spec, measures: [{ ...fixture.spec.measures[0], formatter: "unsafe" }] })).toThrow(ChartCompileError);
  });

  it("rejects invalid dates, duplicate dates, nonfinite numbers and mismatched row counts", () => {
    for (const update of [{ date: "2025-02-29" }, { net_revenue: "NaN" }, { net_revenue: "1e309" }, { date: "2025-03-01" }]) {
      const data = structuredClone(fixture.data);
      Object.assign(data.daily[0], update);
      expect(() => compile(fixture.spec, data)).toThrow(ChartCompileError);
    }
    expect(() => compile(fixture.spec, { ...fixture.data, daily: [] })).toThrow(ChartCompileError);
  });

  it("does not carry references back into caller-owned data", () => {
    const compiled = compile();
    compiled.table[0].net_revenue = "999";
    expect(fixture.data.daily[0].net_revenue).toBe("1.25");
  });
});
