#!/usr/bin/env node
// Renders 95 Sigma post images and thumbnails from a JSON spec.
//
//   node render/render.js topics/<slug>/visual.json
//
// The JSON holds one spec or an array of specs; each spec becomes
// <name>.png in an "out" folder next to the JSON file.
"use strict";
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

function loadPlaywright() {
  try {
    return require("playwright");
  } catch (e) {
    // Cloud sessions ship Playwright globally rather than in the project.
    const root = execSync("npm root -g").toString().trim();
    return require(path.join(root, "playwright"));
  }
}

const SIZES = { post: [1080, 1350], reel: [1080, 1920], yt: [1280, 720] };
const TEMPLATE = path.resolve(__dirname, "..", "templates", "card.html");

async function main() {
  const input = process.argv[2];
  if (!input) {
    console.error("usage: node render/render.js <spec.json>");
    process.exit(1);
  }
  const raw = JSON.parse(fs.readFileSync(input, "utf8"));
  const specs = Array.isArray(raw) ? raw : [raw];
  const outDir = path.join(path.dirname(path.resolve(input)), "out");
  fs.mkdirSync(outDir, { recursive: true });

  const { chromium } = loadPlaywright();
  const browser = await chromium.launch({ args: ["--allow-file-access-from-files"] });
  try {
    for (const [i, spec] of specs.entries()) {
      const [w, h] = SIZES[spec.format] || SIZES.post;
      const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
      await page.addInitScript((s) => { window.SPEC = s; }, spec);
      await page.goto("file://" + TEMPLATE);
      await page.waitForFunction(() => window.__ready === true, null, { timeout: 15000 });
      await page.waitForFunction(() => Array.from(document.images).every((im) => im.complete && im.naturalWidth > 0), null, { timeout: 15000 });
      const name = spec.name || `${spec.format || "post"}-${spec.variant || "light"}-${i + 1}`;
      const file = path.join(outDir, name + ".png");
      await page.locator("#c").screenshot({ path: file });
      console.log(file);
      await page.close();
    }
  } finally {
    await browser.close();
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
