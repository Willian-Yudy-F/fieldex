import fs from "node:fs";
import vm from "node:vm";

const dataScript = fs.readFileSync("fieldex-data.js", "utf8");
const context = { window: {} };
vm.createContext(context);
vm.runInContext(dataScript, context);

if (context.window.FIELD_DEX_INLINE.entries.length !== 42) {
  throw new Error("Inline data must contain 42 entries.");
}

const html = fs.readFileSync("index.html", "utf8");
const inlineScripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
if (inlineScripts.length !== 1) {
  throw new Error(`Expected one inline application script, found ${inlineScripts.length}.`);
}
new Function(inlineScripts[0][1]);
console.log("FielDex data and JavaScript syntax are valid.");
