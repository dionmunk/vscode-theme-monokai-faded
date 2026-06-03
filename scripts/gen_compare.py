import json, re, html, os

FADED = "/Users/munk/Library/CloudStorage/Dropbox/Projects/vscode-theme-monokai-faded/themes/monokai-faded.json"
PRO   = os.path.expanduser("~/.vscode/extensions/monokai.theme-monokai-pro-vscode-2.0.13/themes/Monokai Pro.json")
OUT   = "/Users/munk/Library/CloudStorage/Dropbox/Projects/vscode-theme-monokai-faded/theme-compare-full.html"

def load_jsonc(path):
    lines = []
    for line in open(path, encoding="utf-8"):
        s = line.lstrip()
        if s.startswith("//"):
            continue
        i = line.find("//")            # values are hex; no '//' inside strings here
        if i != -1:
            line = line[:i]
        lines.append(line)
    text = "".join(lines)
    text = re.sub(r",(\s*[}\]])", r"\1", text)   # trailing commas
    return json.loads(text)

faded = load_jsonc(FADED)["colors"]
pro   = load_jsonc(PRO)["colors"]

def norm(v):
    return v.strip().lower() if isinstance(v, str) else v

keys = sorted(set(faded) | set(pro), key=lambda k: (k.split(".")[0], k))

groups = {}
for k in keys:
    groups.setdefault(k.split(".")[0], []).append(k)

n_shared = n_diff = n_fonly = n_ponly = 0
for k in keys:
    a, b = faded.get(k), pro.get(k)
    if a is not None and b is not None:
        n_shared += 1
        if norm(a) != norm(b):
            n_diff += 1
    elif a is not None:
        n_fonly += 1
    else:
        n_ponly += 1

data = {"faded": faded, "pro": pro, "groups": groups}

DATA_JSON = json.dumps(data)

tpl = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Monokai Faded vs Monokai Pro — full color comparison</title>
<style>
 :root{--bg:#202020;--bg-pro:#2d2a2e;--panel:#2a2a2a;--text:#f8f8f8;--muted:#9a9a9a;--border:#3a3a3a;}
 *{box-sizing:border-box}
 body{margin:0;background:var(--bg);color:var(--text);font:13px/1.45 -apple-system,"Segoe UI",system-ui,sans-serif}
 header{position:sticky;top:0;background:#1a1a1a;border-bottom:1px solid var(--border);padding:16px 28px;z-index:5}
 h1{font-size:19px;margin:0 0 8px}
 .stats{display:flex;gap:18px;flex-wrap:wrap;color:var(--muted);font-size:12px;margin-bottom:10px}
 .stats b{color:var(--text)}
 .controls{display:flex;gap:14px;align-items:center;flex-wrap:wrap}
 input[type=search]{background:#111;border:1px solid var(--border);color:var(--text);border-radius:6px;padding:7px 10px;width:280px;font-size:13px}
 label.chk{color:var(--muted);font-size:12px;display:flex;align-items:center;gap:6px;cursor:pointer}
 main{padding:8px 28px 60px}
 h2{font-size:13px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);margin:26px 0 8px;border-bottom:1px solid var(--border);padding-bottom:5px}
 table{border-collapse:collapse;width:100%;max-width:1000px}
 tr{border-bottom:1px solid var(--border)}
 td{padding:6px 12px;vertical-align:middle}
 td.key{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:#d6d6d6;white-space:nowrap;width:42%}
 .cell{display:flex;align-items:center;gap:9px}
 .sw{width:34px;height:22px;border-radius:5px;flex:none;border:1px solid rgba(255,255,255,.14);
     background-image:linear-gradient(45deg,#555 25%,transparent 25%),linear-gradient(-45deg,#555 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#555 75%),linear-gradient(-45deg,transparent 75%,#555 75%);
     background-size:8px 8px;background-position:0 0,0 4px,4px -4px,-4px 0}
 .sw i{display:block;width:100%;height:100%;border-radius:4px}
 .hex{font-family:ui-monospace,Menlo,monospace;font-size:12px}
 .none{color:var(--muted);font-style:italic}
 tr.diff td.key{color:#ffd866}
 tr.diff td.key::before{content:"● ";color:#ffd866}
 tr.fonly td.key::before{content:"◂ ";color:#a9dc76}
 tr.ponly td.key::before{content:"▸ ";color:#78dce8}
 .legend{font-size:11px;color:var(--muted)}
 .hide{display:none}
</style></head><body>
<header>
 <h1>Monokai Faded &nbsp;vs&nbsp; Monokai Pro &mdash; full workbench color comparison</h1>
 <div class="stats">
   <span><b>__TOTAL__</b> keys total</span>
   <span><b>__SHARED__</b> shared</span>
   <span style="color:#ffd866"><b>__DIFF__</b> differ</span>
   <span style="color:#a9dc76"><b>__FONLY__</b> Faded-only</span>
   <span style="color:#78dce8"><b>__PONLY__</b> Pro-only</span>
 </div>
 <div class="controls">
   <input id="q" type="search" placeholder="Filter keys… (e.g. editor, tab, git)"/>
   <label class="chk"><input type="checkbox" id="onlyDiff"/> only differences</label>
   <label class="chk"><input type="checkbox" id="hideMissing"/> hide one-sided</label>
   <span class="legend">&nbsp;&nbsp;<span style="color:#ffd866">●</span> differ &nbsp; <span style="color:#a9dc76">◂</span> Faded only &nbsp; <span style="color:#78dce8">▸</span> Pro only</span>
 </div>
</header>
<main id="main"></main>
<script>
const D = __DATA__;
const {faded, pro, groups} = D;
const norm = v => (typeof v==="string"? v.trim().toLowerCase(): v);

function swatch(v){
  if(v==null) return '<span class="none">— not defined</span>';
  return `<div class="cell"><span class="sw"><i style="background:${v}"></i></span><span class="hex">${v}</span></div>`;
}

const main = document.getElementById("main");
let html = "";
for(const g of Object.keys(groups)){
  html += `<section data-group="${g}"><h2>${g}</h2><table><tbody>`;
  for(const k of groups[g]){
    const a = faded[k] ?? null, b = pro[k] ?? null;
    let cls = "";
    if(a!=null && b!=null) cls = (norm(a)!==norm(b))? "diff":"same";
    else if(a!=null) cls = "fonly"; else cls = "ponly";
    html += `<tr class="${cls}" data-key="${k.toLowerCase()}"><td class="key">${k}</td><td>${swatch(a)}</td><td>${swatch(b)}</td></tr>`;
  }
  html += `</tbody></table></section>`;
}
main.innerHTML = html;

const q = document.getElementById("q");
const onlyDiff = document.getElementById("onlyDiff");
const hideMissing = document.getElementById("hideMissing");
function apply(){
  const term = q.value.trim().toLowerCase();
  document.querySelectorAll("section").forEach(sec=>{
    let shown = 0;
    sec.querySelectorAll("tr").forEach(tr=>{
      const k = tr.dataset.key;
      let ok = !term || k.includes(term);
      if(onlyDiff.checked && !tr.classList.contains("diff")) ok = false;
      if(hideMissing.checked && (tr.classList.contains("fonly")||tr.classList.contains("ponly"))) ok = false;
      tr.classList.toggle("hide", !ok);
      if(ok) shown++;
    });
    sec.classList.toggle("hide", shown===0);
  });
}
[q,onlyDiff,hideMissing].forEach(el=>el.addEventListener("input",apply));
</script>
</body></html>"""

out = (tpl
  .replace("__DATA__", DATA_JSON)
  .replace("__TOTAL__", str(len(keys)))
  .replace("__SHARED__", str(n_shared))
  .replace("__DIFF__", str(n_diff))
  .replace("__FONLY__", str(n_fonly))
  .replace("__PONLY__", str(n_ponly)))

open(OUT, "w", encoding="utf-8").write(out)
print(f"keys={len(keys)} shared={n_shared} diff={n_diff} fadedOnly={n_fonly} proOnly={n_ponly}")
print("wrote", OUT)
