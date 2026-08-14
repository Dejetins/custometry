async page => {
  const root = "/Users/daniildegtyarev/.codex/worktrees/e0a0/Custometry/.codex/delivery/ui-design-programs/custometry-v2/evidence/g3-r2";
  const url = "http://127.0.0.1:4173/.codex/delivery/ui-design-programs/custometry-v2/artifacts/g3-r2/candidate-shell.html";
  const errors = [];
  const failed = [];
  const external = [];
  page.on("console", message => {
    if (message.type() === "error") errors.push(message.text());
  });
  page.on("pageerror", error => errors.push(error.message));
  page.on("requestfailed", request => failed.push(request.url()));
  page.on("request", request => {
    const target = request.url();
    if (!target.startsWith("http://127.0.0.1:4173/") && !target.startsWith("data:")) external.push(target);
  });

  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.goto(url);
  await page.locator("#inspector-toggle").click();
  await page.waitForTimeout(160);
  const inspectorWide = await page.evaluate(() => {
    const workspace = document.querySelector(".workspace").getBoundingClientRect();
    const body = document.querySelector(".workspace-body").getBoundingClientRect();
    const inspector = document.querySelector("#inspector-panel-context").getBoundingClientRect();
    return {
      workspace: { x: workspace.x, y: workspace.y, width: workspace.width, height: workspace.height },
      body: { x: body.x, y: body.y, width: body.width, height: body.height },
      inspector: { x: inspector.x, y: inspector.y, width: inspector.width, height: inspector.height },
      fillsWorkspaceBody: Math.abs(body.y - inspector.y) <= 1 && Math.abs(body.height - inspector.height) <= 1,
      position: getComputedStyle(document.querySelector("#inspector-panel-context")).position,
      focus: document.activeElement.id
    };
  });
  await page.screenshot({ path: `${root}/candidate-web-1920-inspector.png`, scale: "css" });
  await page.keyboard.press("Escape");
  const inspectorWideReturn = await page.evaluate(() => document.activeElement.id);

  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(url);
  const table = await page.evaluate(() => ({
    visible: !!document.querySelector("#table-specimen")?.offsetParent,
    rows: [...document.querySelectorAll("#table-specimen tbody tr:not(.table-group-row)")].map(row => row.getBoundingClientRect().height),
    groupRows: document.querySelectorAll("#table-specimen .table-group-row").length,
    stickyHeadings: [...document.querySelectorAll("#table-specimen thead th")].every(cell => getComputedStyle(cell).position === "sticky"),
    headingTabIndexes: [...document.querySelectorAll("#table-specimen thead th")].map(cell => cell.tabIndex),
    namedSort: document.querySelector('[aria-label="Сортировать демонстрационные значения"]')?.getAttribute("aria-label"),
    groupedControlSurfaces: document.querySelectorAll(".control-cluster").length,
    groupedIconButtons: document.querySelectorAll(".control-cluster button svg.icon").length,
    documentOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
  }));
  await page.screenshot({ path: `${root}/candidate-web-1440-table.png`, scale: "css" });

  await page.setViewportSize({ width: 768, height: 1024 });
  await page.goto(url);
  const workspaceBefore = await page.locator(".workspace").boundingBox();
  await page.locator("#nav-toggle").click();
  await page.waitForTimeout(160);
  const drawer = await page.evaluate(() => {
    const rect = document.querySelector("#context-nav").getBoundingClientRect();
    return {
      bounds: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
      viewportContained: rect.x >= 0 && rect.y >= 0 && rect.right <= innerWidth && rect.bottom <= innerHeight,
      ariaModal: document.querySelector("#context-nav").getAttribute("aria-modal"),
      workspaceInert: document.querySelector(".workspace").inert,
      scrollLock: getComputedStyle(document.querySelector(".workspace-scroll")).overflow,
      focus: document.activeElement.textContent.trim()
    };
  });
  await page.screenshot({ path: `${root}/candidate-web-768-drawer.png`, scale: "css" });
  await page.keyboard.press("Shift+Tab");
  drawer.shiftTabWrap = await page.evaluate(() => document.activeElement.textContent.trim());
  await page.keyboard.press("Tab");
  drawer.tabWrap = await page.evaluate(() => document.activeElement.textContent.trim());
  await page.locator("#drawer-scrim").click({ position: { x: 700, y: 500 } });
  drawer.outsideReturn = await page.evaluate(() => document.activeElement.id);
  await page.locator("#nav-toggle").click();
  await page.keyboard.press("Escape");
  drawer.escapeReturn = await page.evaluate(() => document.activeElement.id);
  const workspaceAfter = await page.locator(".workspace").boundingBox();
  drawer.workspaceStable = workspaceBefore && workspaceAfter && workspaceBefore.x === workspaceAfter.x && workspaceBefore.width === workspaceAfter.width;

  await page.locator("#inspector-toggle").click();
  await page.waitForTimeout(160);
  const inspectorNarrow = await page.evaluate(() => {
    const rect = document.querySelector("#inspector-panel-context").getBoundingClientRect();
    return {
      bounds: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
      viewportContained: rect.x >= 0 && rect.y >= 0 && rect.right <= innerWidth && rect.bottom <= innerHeight,
      focus: document.activeElement.id,
      ariaHidden: document.querySelector("#inspector-panel-context").getAttribute("aria-hidden")
    };
  });
  await page.screenshot({ path: `${root}/candidate-web-768-inspector.png`, scale: "css" });
  await page.keyboard.press("Escape");
  inspectorNarrow.escapeReturn = await page.evaluate(() => document.activeElement.id);

  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(url);
  await page.locator("#lang-toggle").click();
  const language = await page.evaluate(() => ({
    lang: document.documentElement.lang,
    heading: document.querySelector(".hero h1").textContent,
    overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
    heroClipped: document.querySelector(".hero").scrollWidth > document.querySelector(".hero").clientWidth
  }));
  await page.screenshot({ path: `${root}/candidate-web-1440-en.png`, scale: "css" });

  await page.setViewportSize({ width: 768, height: 1024 });
  await page.goto(url);
  const cdp = await page.context().newCDPSession(page);
  await cdp.send("Emulation.setPageScaleFactor", { pageScaleFactor: 2 });
  const zoom = await page.evaluate(() => ({
    scale: visualViewport.scale,
    viewport: { width: visualViewport.width, height: visualViewport.height },
    taskVisible: !!document.querySelector(".hero")?.offsetParent,
    trustVisible: !!document.querySelector("#trust")?.offsetParent,
    recoveryVisible: [...document.querySelectorAll(".state-card b")].some(node => node.textContent.includes("Восстановление")),
    horizontalDocumentOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
  }));
  await page.screenshot({ path: `${root}/candidate-web-768-zoom-200.png`, scale: "css" });
  await cdp.send("Emulation.setPageScaleFactor", { pageScaleFactor: 1 });

  await page.emulateMedia({ reducedMotion: "reduce" });
  const reducedMotion = await page.evaluate(() => ({
    matches: matchMedia("(prefers-reduced-motion: reduce)").matches,
    transitionDuration: getComputedStyle(document.querySelector("#inspector-panel-context")).transitionDuration
  }));

  return {
    inspectorWide,
    inspectorWideReturn,
    table,
    drawer,
    inspectorNarrow,
    language,
    zoom,
    reducedMotion,
    consoleErrors: errors,
    requestFailures: failed,
    externalRequests: [...new Set(external)]
  };
}
