import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const css = readFileSync(resolve(process.cwd(), "app/responsive-hardening.css"), "utf8");
const layout = readFileSync(resolve(process.cwd(), "app/layout.tsx"), "utf8");

describe("responsive hardening", () => {
  it("loads the global responsive guardrail stylesheet", () => {
    expect(layout).toContain('import "./responsive-hardening.css"');
  });

  it("prevents horizontal viewport overflow and allows grid children to shrink", () => {
    expect(css).toContain("overflow-x: clip");
    expect(css).toContain("min-width: 0");
    expect(css).toContain("grid-template-columns: minmax(0, 1fr)");
  });

  it("keeps long headings and controls inside their containers", () => {
    expect(css).toContain("overflow-wrap: anywhere");
    expect(css).toContain("white-space: normal");
    expect(css).toContain("max-width: 100%");
  });

  it("stacks primary actions on narrow mobile screens", () => {
    expect(css).toContain("flex: 1 1 100%");
    expect(css).toContain("width: 100%");
  });
});
