#!/usr/bin/env python3
"""Builds the static site.

- index.html, procflare/, swingcast/, stattrim/, transmogsweep/, trinketdock/, spikespotter/, profcd/ are generated completely.
- leveltrail/ and vendorfloor/ are hand-written tool pages; only the parts between
  <!--@header-->...<!--/@header-->, <!--@footer-->...<!--/@footer--> and
  <!--@changelog-->...<!--/@changelog--> are replaced.

Changelogs come from tools/changelogs/<addon>.md (copy each addon's CHANGELOG.md there).
Run: python3 tools/build.py
"""
import html, re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CL = ROOT / "tools" / "changelogs"

ADDONS = [
    dict(key="leveltrail", name="LevelTrail", cf=1798692, glow="rgba(95,176,122,.30)", tool=True,
         tag="Your leveling run, analysed",
         blurb="Records every level, death, XP source, gold day and dungeon visit. Paste the export into the page and see your run split by split, with records and a share image.",
         wago="https://addons.wago.io/addons/leveltrail"),
    dict(key="vendorfloor", name="VendorFloor", cf=1797826, glow="rgba(224,112,60,.32)", tool=True,
         tag="Auction house sniper",
         blurb="Finds auctions below vendor price, below disenchant value and profitable crafts. One click to buy, collect and sell. The page shows your real profit per day and item.",
         wago="https://addons.wago.io/addons/vendorfloor"),
    dict(key="procflare", name="ProcFlare", cf=1800929, glow="rgba(240,190,90,.32)", tool=False,
         tag="Never miss a proc",
         blurb="A big pulsing Clearcasting alert with sound and screen flash, and small icons with a countdown for weapon, trinket and talent procs. Nothing to set up.",
         wago="https://addons.wago.io/addons/procflare"),
    dict(key="swingcast", name="SwingCast", cf=1800255, glow="rgba(90,120,230,.32)", tool=False,
         tag="Cast bar plus swing timer",
         blurb="Adds spell icon, cast time, latency zone and a swing timer to the standard cast bar. The strip lights up while Maul, Heroic Strike or Cleave is queued.",
         wago="https://addons.wago.io/addons/swingcast"),
    dict(key="stattrim", name="StatTrim", cf=1801407, glow="rgba(110,160,240,.28)", tool=False,
         tag="A tidy character window",
         blurb="Hide, merge and reorder categories and stats right inside the character window. Edit with checkboxes and arrows, works in combat.",
         wago="https://addons.wago.io/addons/stattrim"),
    dict(key="transmogsweep", name="TransmogSweep", cf=1816987, glow="rgba(163,53,238,.32)", tool=False,
         tag="Collect transmogs from the auction house",
         blurb="Every transmog appearance on the auction house you have not collected yet, cheapest first, as a tab in the auction house window. Also finds the recipes your character has not learned yet. Buy them top to bottom with one button.",
         wago="https://addons.wago.io/addons/transmogsweep"),
    dict(key="trinketdock", name="TrinketDock", cf=1818466, glow="rgba(79,195,247,.30)", tool=False,
         tag="A light trinket menu",
         blurb="Two buttons for your trinkets and a flyout to swap them. In combat the swap is queued and done the moment combat ends. Nothing runs in the background.",
         wago="https://addons.wago.io/addons/trinketdock"),
    dict(key="spikespotter", name="SpikeSpotter", cf=1818471, glow="rgba(255,138,61,.30)", tool=False,
         tag="Find the addon behind the stutter",
         blurb="Short FPS drops when you kill, loot or pull? SpikeSpotter asks the game's own addon profiler which addons used those frames and ranks them, with a copyable report.",
         wago="https://addons.wago.io/addons/spikespotter"),
    dict(key="profcd", name="ProfCD", cf=1818860, glow="rgba(140,204,242,.30)", tool=False,
         tag="Profession cooldowns at a glance",
         blurb="Hover the minimap button for the transmute, Mooncloth and Salt Shaker timers of all your characters. Click it to see which crafts you have the mats for.",
         wago="https://addons.wago.io/addons/profcd"),
]
A = {a["key"]: a for a in ADDONS}

# cache busting: changes whenever site.css or site.js change
import hashlib
ASSET_V = hashlib.md5((ROOT / "assets" / "site.css").read_bytes() + (ROOT / "assets" / "site.js").read_bytes()).hexdigest()[:8]


def cf_url(a): return f"https://www.curseforge.com/wow/addons/{a['key']}"
def badge(a): return f"https://img.shields.io/curseforge/dt/{a['cf']}?label=downloads&color=9c7a32&labelColor=1f1a14&style=flat-square"


def esc(s): return html.escape(str(s), quote=True)


def md_inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


def changelog(key, show=5):
    p = CL / f"{key}.md"
    if not p.exists():
        return '<div class="empty">No changelog yet.</div>'
    vers, cur = [], None
    for line in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            cur = [m.group(1).strip(), []]; vers.append(cur); continue
        m = re.match(r"^\s*-\s+(.*)$", line)
        if m and cur:
            cur[1].append(m.group(1))
    def block(v):
        return f'<div class="cl"><b>{esc(v[0])}</b><ul>' + "".join(f"<li>{md_inline(x)}</li>" for x in v[1]) + "</ul></div>"
    out = '<div class="changelog">' + "".join(block(v) for v in vers[:show]) + "</div>"
    if len(vers) > show:
        out += f'<details><summary>{len(vers) - show} older versions</summary><div class="changelog" style="margin-top:12px">' + "".join(block(v) for v in vers[show:]) + "</div></details>"
    return out


def latest(key):
    p = CL / f"{key}.md"
    if p.exists():
        m = re.search(r"^##\s+(\S+)", p.read_text(encoding="utf-8"), re.M)
        if m: return m.group(1)
    return ""


def header(active, base):
    links = "".join(
        f'<a href="{base}{a["key"]}/"{" class=on" if a["key"] == active else ""}><img src="{base}assets/icons/{a["key"]}-64.png" alt=""><span>{a["name"]}</span></a>'
        for a in ADDONS)
    return f'''<header class="top"><div class="wrap">
  <a class="brand" href="{base}"><img src="{base}assets/icons/bencepo-64.png" alt=""><span class="bt">Bencepo<b>·</b>Addons</span></a>
  <nav class="nav">{links}</nav>
  <div class="spacer"></div>
  <a class="btn sm" href="{base}#import">Import export</a>
</div></header>'''


PAYPAL = "https://ko-fi.com/bencepo"


def support_panel():
    return f'''<div class="panel support reveal" style="margin-top:18px;display:flex;gap:22px;align-items:center;flex-wrap:wrap">
    <div style="flex:1;min-width:260px"><h2 style="margin-bottom:6px">Support the addons</h2><p class="small" style="margin:0">All addons and pages are free and stay free, without ads or cookies. A privacy-friendly counter only tallies page views. If they save you time in game, a tip keeps new features and fixes coming.</p></div>
    <a class="btn primary" href="{PAYPAL}" target="_blank" rel="noopener">Support on Ko-fi</a>
  </div>'''


def footer(base):
    addons = "".join(f'<a href="{base}{a["key"]}/">{a["name"]}</a>' for a in ADDONS)
    cf = "".join(f'<a href="{cf_url(a)}" target="_blank" rel="noopener">{a["name"]} on CurseForge</a>' for a in ADDONS)
    return f'''<footer class="site"><div class="wrap">
  <div class="cols">
    <div><h4>Bencepo · Addons</h4><p style="margin:0 0 10px">Small, fast addons for World of Warcraft: Forever. Built by a player who tests every change in game. The pages run in your browser: your exports never leave it.</p>
      <a href="{base}#community">Feedback, bugs and ideas</a><a href="{PAYPAL}" target="_blank" rel="noopener">Support on Ko-fi</a></div>
    <div><h4>Addons</h4>{addons}</div>
    <div><h4>Download</h4>{cf}</div>
  </div>
  <div class="legal">By Bencepo. Not affiliated with Blizzard Entertainment. World of Warcraft is a trademark of Blizzard Entertainment, Inc. Headings use Cinzel (SIL Open Font License).</div>
</div></footer>'''


def page(title, desc, active, base, body, extra_head="", scripts="", icon="bencepo"):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="https://bencepo.github.io/assets/icons/{icon}-256.png">
<meta name="theme-color" content="#0b0a09">
<link rel="icon" type="image/png" href="{base}assets/icons/{icon}-64.png">
<link rel="stylesheet" href="{base}assets/site.css?v={ASSET_V}">
{extra_head}
</head>
<body>
<!--@header-->{header(active, base)}<!--/@header-->
{body}
<!--@footer-->{footer(base)}<!--/@footer-->
<script src="{base}assets/site.js?v={ASSET_V}"></script>
{scripts}
</body>
</html>
'''


def dl_buttons(a):
    return (f'<a class="btn primary" href="{cf_url(a)}" target="_blank" rel="noopener">Download on CurseForge</a>'
            f'<a class="btn" href="{a["wago"]}" target="_blank" rel="noopener">Wago</a>')


def feats(items):
    return '<div class="features">' + "".join(
        f'<div class="feat reveal"><div class="fi">{g}</div><b>{esc(t)}</b><span>{md_inline(d)}</span></div>' for g, t, d in items) + "</div>"


def goes_with(keys, base):
    return '<div class="addons">' + "".join(card(A[k], base, compact=True) for k in keys) + "</div>"


VIDEOS = {
    "vendorfloor": "https://youtu.be/_CKO9z5iTYE",
    "procflare": "https://youtube.com/shorts/WF2kPiWWzdE",
    "swingcast": "https://youtube.com/shorts/zE11MGQ7QIY",
}


def card(a, base, compact=False):
    video = "" if compact or a["key"] not in VIDEOS else f'<a class="btn sm ghost" href="{VIDEOS[a["key"]]}" target="_blank" rel="noopener">▶ Video</a>'
    open_btn = f'<a class="btn gold sm" href="{base}{a["key"]}/">{"Open the page" if a["tool"] else "Details & demo"}</a>'
    return f'''<div class="acard reveal" style="--glow:{a["glow"]}">
  <div class="head"><img src="{base}assets/icons/{a["key"]}-128.png" alt=""><div><h3>{a["name"]}</h3><div class="small">{esc(a["tag"])}</div></div></div>
  {"" if compact else f'<p>{esc(a["blurb"])}</p>'}
  <div class="meta"><span class="tag">v{esc(latest(a["key"]))}</span></div>
  <div class="links">{open_btn}<a class="btn sm" href="{cf_url(a)}" target="_blank" rel="noopener">CurseForge</a><a class="btn sm ghost" href="{a["wago"]}" target="_blank" rel="noopener">Wago</a>{video}</div>
</div>'''


def community(base):
    return f'''<section class="section" id="community">
  <div class="eyebrow">Community</div>
  <h2 class="goldtext">Feedback, bugs and ideas</h2>
  <p class="lead">Every addon is tested in game before it ships, but Forever changes often. Tell me what breaks and what you miss.</p>
  <div class="grid3">
    <div class="panel reveal"><h2>Report a bug</h2><p class="small">Open an issue on GitHub (the form asks for everything needed) or leave a comment on CurseForge: what you did, what happened, and the error text from BugSack if there is one.</p>
      <div class="row" style="margin-bottom:8px">{"".join(f'<a class="btn sm gold" href="https://github.com/Bencepo/{a["name"]}/issues/new/choose" target="_blank" rel="noopener">{a["name"]}</a>' for a in ADDONS)}</div>
      <div class="row">{"".join(f'<a class="btn sm" href="{cf_url(a)}#comments" target="_blank" rel="noopener">{a["name"]}</a>' for a in ADDONS)}</div></div>
    <div class="panel reveal"><h2>Share your run</h2><p class="small">LevelTrail turns your export into a share image for Discord or Reddit, VendorFloor does the same for your flips. Names can be hidden.</p>
      <div class="row"><a class="btn sm gold" href="{base}leveltrail/#demo">LevelTrail demo</a><a class="btn sm gold" href="{base}vendorfloor/#demo">VendorFloor demo</a></div></div>
    <div class="panel reveal"><h2>Suggest a feature</h2><p class="small">Ideas that make leveling faster or the UI calmer have the best chance. Comments on CurseForge reach me directly.</p>
      <div class="row"><a class="btn sm" href="https://www.curseforge.com/members/bencepo/projects" target="_blank" rel="noopener">All projects on CurseForge</a></div></div>
  </div>
  {support_panel()}
</section>'''


# ---------------------------------------------------------------- home
def home():
    base = ""
    icons = "".join(f'<a href="{a["key"]}/" title="{a["name"]}" style="--glow:{a["glow"]}"><img src="assets/icons/{a["key"]}-128.png" alt="{a["name"]}"></a>' for a in ADDONS)
    body = f'''<main>
<div class="wrap">
  <section class="hero homehero">
    <div class="wordmark"><span class="orn"></span><h1 class="goldtext">Bencepo</h1><span class="orn r"></span></div>
    <div class="tagline">Lightweight addons for WoW Forever</div>
    <p class="lead">Small addons for proc alerts, the cast bar, the character window, the auction house, transmog collecting and your leveling run. Light on memory, set up with buttons, never with walls of chat commands.</p>
    <div class="ctas"><a class="btn primary" href="#addons">Browse the addons</a><a class="btn" href="#import">Paste an export</a></div>
    <div class="iconrow">{icons}</div>
  </section>

  <section class="section" id="addons">
    <div class="eyebrow">The collection</div>
    <h2 class="goldtext">Every addon, one style</h2>
    <p class="lead">All of them are free, all of them work together, and none of them needs a configuration marathon.</p>
    <div class="addons">{"".join(card(a, base) for a in ADDONS)}</div>
  </section>

  <section class="section" id="videos">
    <div class="eyebrow">Watch them in action</div>
    <h2 class="goldtext">25-second demos</h2>
    <p class="lead">Short clips straight from the game. They open on YouTube; nothing from YouTube loads on this page.</p>
    <div class="vids">
      <a class="vid reveal" href="https://youtube.com/shorts/PKxT8-Vhkis" target="_blank" rel="noopener"><img src="assets/video/vendorfloor-short.jpg" alt="VendorFloor demo" loading="lazy"><span class="play">▶</span><b>VendorFloor</b><span class="small">Auctions below vendor price</span></a>
      <a class="vid reveal" href="https://youtube.com/shorts/WF2kPiWWzdE" target="_blank" rel="noopener"><img src="assets/video/procflare-short.jpg" alt="ProcFlare demo" loading="lazy"><span class="play">▶</span><b>ProcFlare</b><span class="small">Sound on: proc alerts with sound packs</span></a>
      <a class="vid reveal" href="https://youtube.com/shorts/zE11MGQ7QIY" target="_blank" rel="noopener"><img src="assets/video/swingcast-short.jpg" alt="SwingCast demo" loading="lazy"><span class="play">▶</span><b>SwingCast</b><span class="small">Bear tanks: stop wasting your Maul</span></a>
    </div>
    <div style="text-align:center;margin-top:18px"><a class="btn" href="https://www.youtube.com/@Bencepo" target="_blank" rel="noopener">More videos on YouTube</a></div>
  </section>

  <section class="section" id="import">
    <div class="split">
      <div>
        <div class="eyebrow">Import hub</div>
        <h2 class="goldtext" style="font-size:30px;margin:6px 0 8px">Paste any export</h2>
        <p class="lead">LevelTrail (<code>/trail</code>) or VendorFloor (Menu &gt; Export): paste it here and the right page opens with your data. Nothing is uploaded, the page reads it in your browser.</p>
        <ul class="ticks">
          <li><b>LevelTrail</b>: time per level, XP sources, deaths, gear, records and a share image.</li>
          <li><b>VendorFloor</b>: profit per day, best items, time to sale, cumulative profit and a share image.</li>
        </ul>
      </div>
      <div class="panel dropzone" id="hub">
        <h2>Your export <span class="small">paste or drop a text file</span></h2>
        <textarea id="hubText" spellcheck="false" placeholder='{{"levelTrail":2,...}}  or  {{"vendorFloor":1,...}}'></textarea>
        <div class="row" style="margin-top:12px">
          <button class="primary" id="hubGo">Open my data</button>
          <span class="small" id="hubKind">Detects the addon on its own.</span>
        </div>
        <div class="msg" id="hubMsg"></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="eyebrow">How they are built</div>
    <h2 class="goldtext">Small on purpose</h2>
    <div class="features" style="margin-top:20px">
      <div class="feat reveal"><div class="fi">✦</div><b>Buttons, not commands</b><span>Every setting lives in the options window or behind the minimap button. Chat commands exist, but you never need them.</span></div>
      <div class="feat reveal"><div class="fi">◈</div><b>Light and quiet</b><span>No work while nothing happens. Each release gets a performance review and a code check with the WoW API annotations.</span></div>
      <div class="feat reveal"><div class="fi">⛉</div><b>Private by design</b><span>The web pages read your export in the browser. No accounts, no uploads, no cookies. Your exports never leave your browser.</span></div>
      <div class="feat reveal"><div class="fi">⚒</div><b>Made for Forever</b><span>Built around Forever's limits, such as the hidden combat log and secret values, instead of pretending they are not there.</span></div>
    </div>
  </section>

  {community(base)}
</div>
</main>'''
    head = '''<style>
.homehero{text-align:center;padding-top:84px}
.homehero h1{margin-left:auto;margin-right:auto;font-size:46px;max-width:900px}
.homehero h1 small{display:block;font-size:26px;color:var(--text);margin-top:10px;letter-spacing:1px}
.homehero .lead{margin-left:auto;margin-right:auto}
.homehero .ctas{justify-content:center}
.iconrow{display:flex;justify-content:center;gap:22px;margin-top:46px;flex-wrap:wrap}
.iconrow a{position:relative;display:block;border-radius:20px;transition:transform .25s}
.iconrow a::after{content:"";position:absolute;inset:-18px;border-radius:50%;background:radial-gradient(circle,var(--glow),transparent 70%);z-index:-1;opacity:.8}
.iconrow img{width:92px;height:92px;border-radius:20px;display:block;box-shadow:0 0 0 1px var(--line2),0 14px 30px rgba(0,0,0,.6);animation:float 6s ease-in-out infinite}
.iconrow a:nth-child(2) img{animation-delay:-1.2s}.iconrow a:nth-child(3) img{animation-delay:-2.4s}.iconrow a:nth-child(4) img{animation-delay:-3.6s}.iconrow a:nth-child(5) img{animation-delay:-4.8s}
.iconrow a:hover{transform:scale(1.08)}
.ticks{list-style:none;padding:0;margin:0;color:var(--muted)}
.ticks li{padding-left:24px;position:relative;margin:8px 0}
.ticks li::before{content:"◆";position:absolute;left:2px;color:var(--gold);font-size:12px;top:3px}
.vids{display:flex;justify-content:center;gap:22px;flex-wrap:wrap;margin-top:20px}
.vid{position:relative;display:flex;flex-direction:column;gap:4px;width:220px;text-decoration:none;color:var(--text);text-align:center}
.vid img{width:220px;height:391px;object-fit:cover;border-radius:16px;box-shadow:0 0 0 1px var(--line2),0 14px 30px rgba(0,0,0,.6);transition:transform .25s}
.vid:hover img{transform:scale(1.03)}
.vid .play{position:absolute;left:50%;top:195px;transform:translate(-50%,-50%);width:58px;height:58px;border-radius:50%;background:rgba(0,0,0,.65);color:var(--gold);font-size:24px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 2px var(--gold)}
.vid b{margin-top:6px;color:var(--gold)}
@media(max-width:860px){.homehero h1{font-size:36px}.iconrow img{width:64px;height:64px}}
</style>'''
    js = '''<script>
(function(){
  const t = document.getElementById("hubText"), msg = document.getElementById("hubMsg"), kind = document.getElementById("hubKind"), hub = document.getElementById("hub");
  const NAMES = { leveltrail: "LevelTrail", vendorfloor: "VendorFloor" };
  function check() {
    const k = BENCEPO.detect(t.value);
    kind.textContent = k ? `Recognised: ${NAMES[k]} export.` : t.value.trim() ? "Not recognised yet." : "Detects the addon on its own.";
    kind.className = "small" + (k ? " good" : "");
    return k;
  }
  function go() {
    const k = check();
    if (!t.value.trim()) { msg.textContent = "Paste an export first."; msg.className = "msg err"; return; }
    if (!k) { msg.textContent = "This is not a LevelTrail or VendorFloor export. Copy it again with Ctrl+C in the addon's export window."; msg.className = "msg err"; return; }
    BENCEPO.handoff(k, t.value, "");
  }
  t.addEventListener("input", check);
  t.addEventListener("paste", () => setTimeout(() => { if (check()) go(); }, 0));
  document.getElementById("hubGo").onclick = go;
  ["dragenter","dragover"].forEach(e => hub.addEventListener(e, ev => { ev.preventDefault(); hub.classList.add("over"); }));
  ["dragleave","drop"].forEach(e => hub.addEventListener(e, () => hub.classList.remove("over")));
  hub.addEventListener("drop", ev => { ev.preventDefault(); const f = ev.dataTransfer.files && ev.dataTransfer.files[0];
    if (f) f.text().then(x => { t.value = x; go(); }); else { t.value = ev.dataTransfer.getData("text"); go(); } });
})();
</script>'''
    return page("Bencepo · Addons for WoW Forever", "LevelTrail, VendorFloor, ProcFlare, SwingCast, StatTrim and TransmogSweep: small, fast addons for World of Warcraft: Forever, with private web pages for your leveling run and auction flips.",
                "", base, body, head, js)


# ---------------------------------------------------------------- showcase pages

INGAME_W = {"trinketdock": 570, "profcd": 620, "procflare": 920, "swingcast": 895, "leveltrail": 470, "spikespotter": 560}


def ingame(key, caption):
    """Section with a real in-game screenshot (media/<key>/ingame.jpg)."""
    a = A[key]
    return f'''<section class="section" id="ingame">
    <div class="eyebrow">In game</div>
    <h2 class="goldtext">How it looks in WoW Forever</h2>
    <p class="lead">{esc(caption)}</p>
    <div class="panel reveal" style="padding:10px;max-width:{INGAME_W.get(key, 800) + 22}px"><img src="../media/{key}/ingame.jpg" alt="{a["name"]} in WoW Forever" loading="lazy" style="width:100%;display:block;border-radius:8px"></div>
  </section>'''

def showcase(key, demo_html, demo_css, demo_js, features, settings, extra_sections, goes):
    a, base = A[key], "../"
    body = f'''<main>
<div class="wrap">
  <section class="hero addonhero">
    <img class="heroicon" src="{base}assets/icons/{key}-256.png" alt="{a["name"]}">
    <div>
      <div class="eyebrow">{esc(a["tag"])} · v{esc(latest(key))}</div>
      <h1 class="goldtext">{a["name"]}</h1>
      <p class="lead">{esc(a["blurb"])}</p>
      <div class="ctas">{dl_buttons(a)}<a class="btn ghost" href="#demo">Try the live demo</a></div>
    </div>
  </section>

  <section class="section" id="demo">
    <div class="eyebrow">Live demo</div>
    <h2 class="goldtext">See it in action</h2>
    <p class="lead">A recreation in your browser, close to what you see in game.</p>
    {demo_html}
  </section>

  <section class="section" id="features">
    <div class="eyebrow">Features</div>
    <h2 class="goldtext">What it does</h2>
    {feats(features)}
  </section>

  {extra_sections}

  <section class="section">
    <div class="split">
      <div class="panel reveal"><h2>Settings</h2>{settings}</div>
      <div class="panel reveal" id="changelog"><h2>Changelog</h2><!--@changelog-->{changelog(key)}<!--/@changelog--></div>
    </div>
  </section>

  <section class="section">
    <div class="eyebrow">Goes well with</div>
    <h2 class="goldtext">More from Bencepo</h2>
    {goes_with(goes, base)}
  </section>

  {community(base)}
</div>
</main>'''
    return page(f"{a['name']} · {a['tag']} · WoW Forever addon", a["blurb"], key, base, body,
                f"<style>{demo_css}</style>", f"<script>{demo_js}</script>", icon=key)


PROC_DEMO = '''
<div class="pfgrid">
<div class="panel" style="padding:0;overflow:hidden">
  <div class="pfstage" id="pfStage">
    <div class="pfflash" id="pfFlash"></div>
    <div class="pfcc" id="pfCC"><div class="pfccicon"></div><div class="pfcctime" id="pfCCt">15</div><div class="pfcclabel">Clearcasting</div></div>
    <div class="pfrow" id="pfRow"></div>
    <div class="pfchar"></div>
    <div class="pfhint" id="pfHint">Press a button below to trigger a proc.</div>
  </div>
  <div class="row" style="padding:16px 18px;border-top:1px solid var(--line)">
    <button class="primary" id="pfCCBtn">Clearcasting</button>
    <button id="pfW">Weapon proc</button>
    <button id="pfT">Trinket proc</button>
    <button id="pfD">Target debuff</button>
  </div>
</div>
<div class="wowopt">
  <div class="wowopt-h">ProcFlare <span>Options</span></div>
  <div class="wo"><label>Sound pack</label><div class="wsel" data-key="pack"></div></div>
  <div class="wo"><label>Clearcasting sound</label><div class="wsel" data-key="cc"></div></div>
  <div class="wo"><label>Screen flash</label><span class="wchk on" id="pfFlashOn"></span></div>
  <div class="wo"><label>Proc sound</label><div class="wsel" data-key="proc"></div></div>
  <div class="wo"><label>Volume</label><div class="wslide"><input type="range" id="pfVol" min="25" max="100" step="25" value="100"><b id="pfVolV">100</b></div></div>
  <div class="wo"><label>Sound</label><span class="wchk on" id="pfSound"></span></div>
  <p class="small" style="margin:12px 2px 0">The same options as in game, in ProcFlare's own window (/pfl). ProcFlare picks the pack from your class on first login.</p>
</div>
</div>'''
PROC_CSS = '''
.pfgrid{display:grid;grid-template-columns:1fr 360px;gap:18px;align-items:start}
@media(max-width:900px){.pfgrid{grid-template-columns:1fr}}
.pfstage{position:relative;height:380px;background:radial-gradient(ellipse at 50% 120%,#24361f 0%,#121a10 40%,#07090a 75%),#07090a;overflow:hidden}
.pfstage::before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 50% 30%,rgba(120,150,200,.10),transparent 60%)}
.pfflash{position:absolute;inset:0;pointer-events:none;box-shadow:inset 0 0 0 0 rgba(80,150,255,0);transition:box-shadow .5s}
.pfflash.on{box-shadow:inset 0 0 120px 30px rgba(80,150,255,.55);transition:box-shadow .08s}
.pfchar{position:absolute;left:50%;bottom:34px;width:46px;height:96px;margin-left:-23px;border-radius:23px 23px 8px 8px;background:linear-gradient(#2a2620,#14110d);box-shadow:0 0 0 1px rgba(255,255,255,.04),0 20px 30px rgba(0,0,0,.6)}
.pfchar::before{content:"";position:absolute;left:9px;top:-26px;width:28px;height:28px;border-radius:50%;background:#2a2620}
.pfcc{position:absolute;left:50%;top:22px;transform:translateX(-50%) scale(.6);opacity:0;transition:.25s;text-align:center}
.pfcc.on{opacity:1;transform:translateX(-50%) scale(1)}
.pfccicon{width:96px;height:96px;border-radius:12px;margin:0 auto;border:2px solid #6aa8ff;background:conic-gradient(from 0deg,#14204a,#3b6fe0,#a6c8ff,#3b6fe0,#14204a,#3b6fe0,#a6c8ff,#14204a);animation:pfpulse 1s ease-in-out infinite;box-shadow:0 0 30px rgba(90,150,255,.8)}
.pfccicon::after{content:"";display:block;width:100%;height:100%;border-radius:10px;background:radial-gradient(circle,rgba(255,255,255,.85) 0%,rgba(140,190,255,.4) 30%,transparent 60%)}
@keyframes pfpulse{0%,100%{box-shadow:0 0 18px rgba(90,150,255,.6);transform:scale(1)}50%{box-shadow:0 0 46px rgba(120,180,255,1);transform:scale(1.07)}}
.pfcctime{font:800 30px var(--sans);color:#fff;text-shadow:0 2px 6px #000;margin-top:-62px;position:relative}
.pfcclabel{margin-top:40px;font-family:var(--display);color:#a6c8ff;font-size:14px;letter-spacing:1px;text-shadow:0 1px 4px #000}
.pfrow{position:absolute;left:50%;top:172px;transform:translateX(-50%);display:flex;gap:8px}
.pfp{width:42px;height:42px;border-radius:7px;border:1px solid #e0b45a;position:relative;animation:pfin .25s ease-out;box-shadow:0 0 14px var(--c)}
.pfp b{position:absolute;inset:0;display:grid;place-items:center;font:800 15px var(--sans);color:#fff;text-shadow:0 1px 3px #000}
.pfp i{position:absolute;left:0;right:0;bottom:-16px;text-align:center;font-style:normal;font-size:10px;color:var(--muted);white-space:nowrap}
@keyframes pfin{from{transform:scale(1.6);opacity:0}}
.pfhint{position:absolute;left:0;right:0;bottom:12px;text-align:center;color:var(--dim);font-size:13px}
/* in-game options look */
.wowopt{background:linear-gradient(rgba(20,16,10,.92),rgba(12,10,7,.95)),repeating-linear-gradient(45deg,rgba(255,255,255,.015) 0 2px,transparent 2px 6px);border:2px solid #5a4a2c;border-radius:6px;padding:14px 14px 16px;box-shadow:inset 0 0 0 1px #000,0 10px 30px rgba(0,0,0,.5)}
.wowopt-h{font-family:var(--display);font-size:20px;color:#fff;padding-bottom:10px;margin-bottom:6px;border-bottom:1px solid rgba(255,209,0,.25)}
.wowopt-h span{font-size:13px;color:#a89a80;font-family:var(--sans);margin-left:6px}
.wo{display:grid;grid-template-columns:130px 1fr;align-items:center;gap:10px;padding:7px 2px}
.wo label{color:#ffd100;font-size:13px;text-shadow:0 1px 1px #000}
.wsel{display:flex;align-items:center;gap:4px}
.wsel button{flex:none;width:22px;height:24px;padding:0;border-radius:3px;border:1px solid #6b5a3a;background:linear-gradient(#3a3226,#1c170f);color:#ffd100;font-size:10px;display:grid;place-items:center}
.wsel button:hover{border-color:#ffd100;box-shadow:none}
.wsel select{flex:1;min-width:0;appearance:none;-webkit-appearance:none;text-align:center;text-align-last:center;height:24px;border-radius:3px;border:1px solid #6b5a3a;background:linear-gradient(#3a3226,#1c170f);color:#fff;font:13px var(--sans);padding:0 6px;cursor:pointer}
.wsel select:focus{outline:none;border-color:#ffd100}
.wsel select option{background:#1c170f;color:#fff}
.wchk{width:22px;height:22px;border-radius:3px;border:1px solid #6b5a3a;background:#0e0b07;cursor:pointer;position:relative}
.wchk.on::after{content:"";position:absolute;left:6px;top:1px;width:7px;height:13px;border:solid #ffd100;border-width:0 3px 3px 0;transform:rotate(40deg)}
.wslide{display:flex;align-items:center;gap:10px}
.wslide input{flex:1;accent-color:#ffd100}
.wslide b{color:#fff;font-weight:400;font-size:13px;width:28px;text-align:right}
'''
PROC_JS = '''
(function(){
  const $ = id => document.getElementById(id);
  const SOUNDS = [["none","None"],["war_drums","Melee: War drums"],["war_horn","Melee: War horn"],["axe_clash","Melee: Axe clash"],["beast_roar","Melee: Beast roar"],["rage_spike","Melee: Rage spike"],["thud","Melee: Thud"],
    ["arcane_surge","Caster: Arcane surge"],["mana_burst","Caster: Mana burst"],["frost_shatter","Caster: Frost shatter"],["fire_burst","Caster: Fire burst"],["power_chord","Caster: Power chord"],["spark","Caster: Spark"],
    ["chime","ProcFlare chime"],["ping","ProcFlare ping"]];
  const PACKS = [["melee","Melee"],["caster","Caster"]];
  const PACKSET = { melee: ["war_drums","axe_clash"], caster: ["arcane_surge","spark"] };
  const st = { pack: "melee", cc: "war_drums", proc: "axe_clash" };
  const cache = {};
  function play(name){ if (!name || name === "none" || !$("pfSound").classList.contains("on")) return;
    const a = cache[name] = cache[name] || new Audio("../assets/sounds/procflare/" + name + ".mp3");
    a.volume = +$("pfVol").value / 100; a.currentTime = 0; a.play().catch(() => {}); }
  function sel(key, items){
    const box = document.querySelector(`.wsel[data-key=${key}]`);
    box.innerHTML = `<button aria-label="Previous">◀</button><select>${items.map(([v,l]) => `<option value="${v}">${l}</option>`).join("")}</select><button aria-label="Next">▶</button>`;
    const s = box.querySelector("select"); s.value = st[key];
    const set = v => { st[key] = v; s.value = v; changed(key); };
    s.onchange = () => set(s.value);
    const [prev, , next] = box.children;
    prev.onclick = () => { const i = items.findIndex(x => x[0] === st[key]); set(items[(i - 1 + items.length) % items.length][0]); };
    next.onclick = () => { const i = items.findIndex(x => x[0] === st[key]); set(items[(i + 1) % items.length][0]); };
    box._set = v => { st[key] = v; s.value = v; };
  }
  function changed(key){
    if (key === "pack") { const [c, p] = PACKSET[st.pack]; document.querySelector(".wsel[data-key=cc]")._set(c); document.querySelector(".wsel[data-key=proc]")._set(p); play(c); }
    else play(st[key]);
  }
  sel("pack", PACKS); sel("cc", SOUNDS); sel("proc", SOUNDS);
  document.querySelectorAll(".wchk").forEach(c => c.onclick = () => c.classList.toggle("on"));
  $("pfVol").oninput = () => { $("pfVolV").textContent = $("pfVol").value; };
  $("pfVol").onchange = () => play(st.cc);
  let ccT = null, ccLeft = 0;
  $("pfCCBtn").onclick = () => {
    $("pfHint").textContent = "Clearcasting: your next spell is free.";
    ccLeft = 15; $("pfCCt").textContent = ccLeft; $("pfCC").classList.add("on");
    play(st.cc);
    if ($("pfFlashOn").classList.contains("on")) { $("pfFlash").classList.add("on"); setTimeout(() => $("pfFlash").classList.remove("on"), 180); }
    clearInterval(ccT); ccT = setInterval(() => { ccLeft--; $("pfCCt").textContent = ccLeft; if (ccLeft <= 0) { clearInterval(ccT); $("pfCC").classList.remove("on"); } }, 1000);
  };
  const KINDS = { pfW: ["Crusader", "#e8c46a", "radial-gradient(circle at 40% 35%,#fff3c4,#e0a83a 45%,#6b3d0c)", 15],
                  pfT: ["Trinket", "#b27ae0", "radial-gradient(circle at 40% 35%,#f0d8ff,#9a5bd6 45%,#3a1660)", 20],
                  pfD: ["On target", "#5fb0ff", "radial-gradient(circle at 40% 35%,#d8f0ff,#3d8ad9 45%,#0c2a52)", 12] };
  Object.keys(KINDS).forEach(id => $(id).onclick = () => {
    const [name, c, bg, sec] = KINDS[id];
    $("pfHint").textContent = name + " proc: small icon with a countdown.";
    play(st.proc);
    const el = document.createElement("div"); el.className = "pfp"; el.style.setProperty("--c", c); el.style.background = bg;
    el.innerHTML = `<b>${sec}</b><i>${name}</i>`; $("pfRow").prepend(el);
    let left = sec; const t = setInterval(() => { left--; el.querySelector("b").textContent = left; if (left <= 0) { clearInterval(t); el.remove(); } }, 1000);
  });
})();
'''

SWING_DEMO = '''
<div class="panel" style="padding:0;overflow:hidden">
  <div class="scstage">
    <div class="scwrap">
      <div class="scbar">
        <div class="scicon" id="scIcon"></div>
        <div class="sccast"><div class="scfill" id="scFill"></div><div class="sclat" id="scLat"></div><span class="scname" id="scName">Healing Touch</span><span class="sctime" id="scTime"></span></div>
      </div>
      <div class="scswing"><div class="scsfill" id="scSwing"></div><span id="scSwingT">2.4</span></div>
      <div class="small" style="text-align:center;margin-top:14px" id="scHint">The swing strip runs on its own. Cast a spell or queue Maul.</div>
    </div>
  </div>
  <div class="row" style="padding:16px 18px;border-top:1px solid var(--line)">
    <button class="primary" id="scCast">Cast Healing Touch</button>
    <button id="scMaul">Queue Maul</button>
    <button id="scCleave">Queue Cleave</button>
    <div class="spacer"></div>
    <label class="small">Latency <input type="range" id="scPing" min="20" max="400" value="120" style="vertical-align:middle"> <span id="scPingV">120 ms</span></label>
  </div>
</div>'''
SWING_CSS = '''
.scstage{height:300px;display:grid;place-items:center;background:radial-gradient(ellipse at 50% 120%,#1d2433 0%,#0d1018 55%,#07080b 80%)}
.scwrap{width:min(560px,88%)}
.scbar{display:flex;gap:8px;align-items:center}
.scicon{flex:none;width:40px;height:40px;border-radius:5px;border:1px solid #b89a5a;background:radial-gradient(circle at 40% 35%,#e5ffd4,#5fb07a 45%,#163a20);opacity:.35;transition:opacity .2s}
.scicon.on{opacity:1;box-shadow:0 0 12px rgba(95,176,122,.6)}
.sccast{position:relative;flex:1;height:28px;border-radius:4px;background:rgba(0,0,0,.65);border:1px solid #6b5a3a;box-shadow:0 0 0 2px #1a1510,0 6px 16px rgba(0,0,0,.6);overflow:hidden}
.scfill{position:absolute;left:0;top:0;bottom:0;width:0;background:linear-gradient(#ffe08a,#e0a83a 55%,#a7731e)}
.sclat{position:absolute;right:0;top:0;bottom:0;width:10%;background:rgba(220,60,40,.55);opacity:0}
.scname{position:absolute;left:10px;top:4px;font-size:14px;color:#fff;text-shadow:0 1px 2px #000}
.sctime{position:absolute;right:10px;top:4px;font-size:14px;color:#fff;text-shadow:0 1px 2px #000;font-variant-numeric:tabular-nums}
.scswing{position:relative;margin:8px 0 0 48px;height:9px;border-radius:3px;background:rgba(0,0,0,.6);border:1px solid #3a3226;overflow:visible}
.scsfill{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:3px;background:#c9ced6}
.scswing span{position:absolute;right:0;top:12px;font-size:11px;color:var(--muted);font-variant-numeric:tabular-nums}
'''
SWING_JS = '''
(function(){
  const $ = id => document.getElementById(id);
  const SPEED = 2.4; let swingStart = performance.now(), queued = null;
  let cast = null; const CAST = 2.5;
  function ping(){ return +$("scPing").value / 1000; }
  $("scPing").oninput = () => { $("scPingV").textContent = $("scPing").value + " ms"; };
  $("scCast").onclick = () => { cast = performance.now(); $("scIcon").classList.add("on"); $("scHint").textContent = "Red zone at the end: press your next spell as soon as the bar reaches it."; };
  $("scMaul").onclick = () => { queued = "#e8873a"; $("scHint").textContent = "Maul queued: the strip turns orange until the swing lands."; };
  $("scCleave").onclick = () => { queued = "#4f8fd9"; $("scHint").textContent = "Cleave queued: blue until the swing lands."; };
  function frame(now){
    let s = (now - swingStart) / 1000;
    if (s >= SPEED) { swingStart = now; s = 0; if (queued) { queued = null; } }
    $("scSwing").style.width = (s / SPEED * 100) + "%";
    $("scSwing").style.background = queued || "#c9ced6";
    $("scSwing").style.boxShadow = queued ? `0 0 10px ${queued}` : "none";
    $("scSwingT").textContent = (SPEED - s).toFixed(1);
    if (cast) {
      const c = (now - cast) / 1000;
      const lat = Math.min(.5, ping() / CAST);
      $("scLat").style.width = (lat * 100) + "%"; $("scLat").style.opacity = 1;
      if (c >= CAST) { cast = null; $("scFill").style.width = "0"; $("scTime").textContent = ""; $("scIcon").classList.remove("on"); $("scLat").style.opacity = 0; }
      else { $("scFill").style.width = (c / CAST * 100) + "%"; $("scTime").textContent = (CAST - c).toFixed(1); }
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
'''

STAT_DEMO = '''
<div class="grid2">
  <div class="panel" style="padding:18px">
    <div class="row" style="justify-content:space-between;margin-bottom:10px"><b class="display" style="color:var(--gold2)">Character Stats</b>
      <button class="sm" id="stEdit" title="Edit mode">⚙ Edit</button></div>
    <div class="stpanel" id="stPanel"></div>
    <div class="small" style="margin-top:10px" id="stHint">Click the gear to enter edit mode, like in game.</div>
  </div>
  <div class="panel" style="padding:18px">
    <h2>Recorded in game</h2>
    <img src="../media/stattrim/demo.gif" alt="StatTrim demo in WoW Forever" loading="lazy" style="width:100%;border-radius:10px;border:1px solid var(--line)">
  </div>
</div>'''
STAT_CSS = '''
.stpanel{background:rgba(0,0,0,.55);border:1px solid #4a3d26;border-radius:6px;padding:6px 8px;font-size:13px}
.stcat{margin:6px 0 2px}
.stcat .h{display:flex;align-items:center;gap:6px;color:#ffd100;font-weight:700;padding:2px 0;border-bottom:1px solid rgba(255,209,0,.15)}
.strow{display:flex;align-items:center;gap:6px;padding:2px 0}
.strow .n{flex:1;color:#e8e2d0}.strow .v{color:#fff;font-variant-numeric:tabular-nums}
.stctl{display:none;gap:2px}.edit .stctl{display:inline-flex}
.stctl button{padding:0 5px;font-size:11px;border-radius:4px;line-height:16px}
.off{opacity:.35}.gone{display:none}
.edit .gone{display:flex;opacity:.35}
.stcat.gone{display:none}.edit .stcat.gone{display:block;opacity:.35}
.hidenm>.h .t{display:none}.edit .hidenm>.h .t{display:inline;opacity:.4}
'''
STAT_JS = '''
(function(){
  const $ = id => document.getElementById(id);
  let edit = false;
  const cats = [
    { n: "Primary Attributes", s: [["Strength","48"],["Agility","112"],["Stamina","97"],["Intellect","61"],["Spirit","66"],["Movement Speed","100%"]] },
    { n: "Melee", s: [["Damage","81-104"],["Speed","2.40"],["Power","388"],["Hit","3.0%"],["Crit","14.2%"]] },
    { n: "Spell", s: [["Bonus Damage","12"],["Bonus Healing","24"],["Hit","0.0%"],["Crit","5.1%"],["Mana Regen","22"]] },
    { n: "Defenses", s: [["Armor","2780"],["Defense","170"],["Dodge","11.4%"],["Parry","0.0%"],["Block","0.0%"]] }
  ].map(c => ({ ...c, on: true, name: true, s: c.s.map(([n, v]) => ({ n, v, on: true })) }));
  function render(){
    const p = $("stPanel"); p.className = "stpanel" + (edit ? " edit" : "");
    p.innerHTML = cats.map((c, ci) => `<div class="stcat ${c.on ? "" : "gone"} ${c.name ? "" : "hidenm"}">
      <div class="h"><span class="stctl"><input type="checkbox" data-c="${ci}" ${c.on ? "checked" : ""} title="Show category"><input type="checkbox" data-cn="${ci}" ${c.name ? "checked" : ""} title="Show the name"></span><span class="t">${c.n}</span><span class="spacer"></span><span class="stctl"><button data-cu="${ci}">▲</button><button data-cd="${ci}">▼</button></span></div>
      ${c.s.map((s, si) => `<div class="strow ${s.on ? "" : "gone"}"><span class="stctl"><input type="checkbox" data-s="${ci}.${si}" ${s.on ? "checked" : ""}></span><span class="n">${s.n}</span><span class="v">${s.v}</span><span class="stctl"><button data-su="${ci}.${si}">▲</button><button data-sd="${ci}.${si}">▼</button></span></div>`).join("")}
    </div>`).join("");
  }
  const mv = (a, i, d) => { const j = i + d; if (j < 0 || j >= a.length) return; [a[i], a[j]] = [a[j], a[i]]; };
  $("stPanel").addEventListener("click", ev => {
    const t = ev.target, d = t.dataset; if (!Object.keys(d).length) return;
    if (d.c) cats[d.c].on = t.checked;
    if (d.cn) cats[d.cn].name = t.checked;
    if (d.s) { const [c, s] = d.s.split(".").map(Number); cats[c].s[s].on = t.checked; }
    if (d.cu) mv(cats, +d.cu, -1); if (d.cd) mv(cats, +d.cd, 1);
    if (d.su) { const [c, s] = d.su.split(".").map(Number); mv(cats[c].s, s, -1); }
    if (d.sd) { const [c, s] = d.sd.split(".").map(Number); mv(cats[c].s, s, 1); }
    render();
  });
  $("stEdit").onclick = () => { edit = !edit; $("stEdit").classList.toggle("gold", edit);
    $("stHint").textContent = edit ? "Untick what you do not need, move rows with the arrows. Click the gear again to finish." : "Hidden rows are gone. Your panel, your order."; render(); };
  render();
})();
'''

TS_DEMO = '''
<div class="grid2">
  <div class="panel tsdemo" style="padding:14px">
    <div class="row" style="gap:8px;margin-bottom:10px">
      <button class="sm tsbtn" id="tsScan">Scan</button>
      <button class="sm tson" id="tsUnique">&#10003; Unique appearances</button>
      <span class="small" id="tsStatus" style="margin-left:auto">5 uncollected looks</span>
    </div>
    <div class="tslist" id="tsList"></div>
    <div class="row" style="margin-top:10px"><span class="small" id="tsInfo">Click "Start buying": each click checks or buys the next item.</span>
      <button class="sm tsbtn" id="tsBuy" style="margin-left:auto">Start buying</button></div>
  </div>
  <div class="panel" style="padding:18px">
    <h2>Recorded in game</h2>
    <img src="../media/transmogsweep/demo.gif" alt="TransmogSweep in the auction house of WoW Forever" loading="lazy" style="width:100%;border-radius:10px;border:1px solid var(--line)">
  </div>
</div>'''
TS_CSS = '''
.tsdemo{background:linear-gradient(180deg,#210d33,#07040b);border-color:#5c3380}
.tsdemo .tsbtn{background:#a335ee;border-color:#d58cff;color:#fff}
.tsdemo .tson{background:#28143a;border-color:#a335ee;color:#c98cff}
.tslist{background:rgba(0,0,0,.5);border:1px solid #5c3380;border-radius:6px;font-size:13px;min-height:150px}
.tsrow{display:flex;gap:8px;padding:5px 10px;border-bottom:1px solid rgba(163,53,238,.12);transition:background .2s,opacity .3s}
.tsrow .n{flex:1}.tsrow .s{width:90px;color:#a38fb8}.tsrow .p{width:70px;text-align:right;color:#fff;font-variant-numeric:tabular-nums}
.tsrow.sel{background:rgba(163,53,238,.25)}.tsrow.gone{opacity:0}
.q1{color:#fff}.q2{color:#1eff00}
'''
TS_JS = '''
(function(){
  const $ = id => document.getElementById(id);
  const all = [["White Woolen Dress","Chest",550,1],["War Paint Shoulder Pads","Shoulder",577,1],["Dirty Blunderbuss","Ranged",590,1],["Fine Leather Tunic","Chest",600,2],["Woolen Boots","Feet",615,2]];
  let rows = all.slice(), sel = -1, ready = false;
  const money = c => Math.floor(c / 100) + "s " + (c % 100) + "c";
  function render(){
    $("tsList").innerHTML = rows.map((r, i) => `<div class="tsrow ${i === sel ? "sel" : ""}"><span class="n q${r[3]}">${r[0]}</span><span class="s">${r[1]}</span><span class="p">${money(r[2])}</span></div>`).join("") || '<div class="small" style="padding:20px;text-align:center">Nothing left to collect.</div>';
    $("tsStatus").textContent = rows.length + " uncollected looks";
    $("tsBuy").textContent = !rows.length ? "Buy" : ready ? "Buy for " + money(rows[sel][2]) : (sel < 0 ? "Start buying" : "Check price");
  }
  $("tsBuy").onclick = () => {
    if (!rows.length) return;
    if (sel < 0) sel = 0;
    if (!ready) { ready = true; $("tsInfo").textContent = rows[sel][0] + " found. Click Buy."; render(); return; }
    $("tsInfo").textContent = "Bought " + rows[sel][0] + ". The next row is checked by itself.";
    rows.splice(sel, 1); if (sel >= rows.length) sel = rows.length - 1; ready = rows.length > 0; render();
  };
  $("tsScan").onclick = () => { rows = all.slice(); sel = -1; ready = false; $("tsInfo").textContent = "Scanned weapons and armor: a few seconds, any time."; render(); };
  $("tsUnique").onclick = () => { $("tsInfo").textContent = "Unique: one row per look, the cheapest item that has it."; };
  render();
})();
'''

PC_DEMO = '''
<div class="grid2">
  <div class="panel pcdemo" style="padding:18px">
    <div class="row" style="justify-content:space-between;margin-bottom:12px">
      <b class="display" style="color:#8cccf2">ProfCD</b>
      <span class="small">Hover the button, then click it</span>
    </div>
    <div class="pcstage">
      <div class="pcmap"><div class="pcbtn" id="pcBtn" title="ProfCD">&#9719;</div></div>
      <div class="pctip" id="pcTip"></div>
    </div>
    <div class="pcwin" id="pcWin"></div>
    <div class="small" id="pcInfo" style="margin-top:12px">Click a craft that is ready and has its mats to use it.</div>
  </div>
  <div class="panel" style="padding:18px">
    <h2>How it plays</h2>
    <ul class="ticks" style="list-style:none;padding:0;margin:0;color:var(--muted)">
      <li style="margin:7px 0">Hover the minimap button: every cooldown of every character, with the time left.</li>
      <li style="margin:7px 0">Click it: the window lists each craft with its mats, in bags, in the bank or missing.</li>
      <li style="margin:7px 0">Every transmute has its own cooldown in Forever, so each gets its own row.</li>
      <li style="margin:7px 0">Alts show as of their last login.</li>
      <li style="margin:7px 0">No minimap button? ProfCD makes a macro: one click opens the window, the next closes it.</li>
    </ul>
  </div>
</div>'''
PC_CSS = '''
.pcdemo{background:linear-gradient(180deg,#0d1a24,#05090d);border-color:#24506a}
.pcstage{position:relative;height:72px}
.pcmap{position:absolute;right:6px;top:0;width:64px;height:64px;border-radius:50%;background:radial-gradient(#2c3e2a,#14200f);border:3px solid #6b5a3a}
.pcbtn{position:absolute;left:-14px;bottom:-6px;width:32px;height:32px;border-radius:50%;background:#0f1318;border:2px solid #8cccf2;color:#8cccf2;display:flex;align-items:center;justify-content:center;font-size:18px;cursor:pointer;user-select:none}
.pcbtn:hover{box-shadow:0 0 12px rgba(140,204,242,.6)}
.pctip{display:none;position:absolute;right:84px;top:0;z-index:3;background:rgba(8,10,14,.96);border:1px solid #4a5a6a;border-radius:4px;padding:8px 10px;font-size:12px;min-width:220px}
.pctip.on{display:block}
.pctip .l{display:flex;justify-content:space-between;gap:14px;color:#e6e9ee}
.pcwin{display:none;margin-top:10px;background:rgba(15,19,24,.97);border:1px solid #28313c;border-top:2px solid #8cccf2;border-radius:4px;padding:10px 12px;font-size:13px}
.pcwin.on{display:block}
.pcwin .r{display:grid;grid-template-columns:1fr 70px 1.2fr;gap:8px;padding:3px 0;cursor:default}
.pcwin .r.go{cursor:pointer}.pcwin .r.go:hover{background:rgba(140,204,242,.08)}
.pcwin .c{color:#ffd100;margin-top:6px}.pcwin .t{text-align:right;font-variant-numeric:tabular-nums}
.pcg{color:#60ff60}.pcy{color:#ffd24d}.pcr{color:#ff6060}.pcm{color:#8d97a5}
'''
PC_JS = '''
(function(){
  const $ = id => document.getElementById(id);
  const now = () => Math.floor(Date.now() / 1000);
  const chars = [
    { n: "Mortrak", c: "#ff7d0a", me: true, cds: [
      { l: "Transmute: Arcanite", at: 0, cd: 172800, mats: [["Thorium Bar", 1, 4, 6], ["Arcane Crystal", 1, 0, 2]] },
      { l: "Transmute: Truesilver", at: now() + 1460, cd: 3600, mats: [["Mithril Bar", 1, 0, 0]] },
      { l: "Transmute: Gold", at: 0, cd: 3600, mats: [["Iron Bar", 1, 7, 7]] } ] },
    { n: "Stitchwork", c: "#9482c9", seen: "18.11. 21:40", cds: [
      { l: "Mooncloth", at: now() + 201600, cd: 345600, mats: [["Felcloth", 2, 2, 2]] } ] },
  ];
  const fmt = at => { const r = at - now(); if (r <= 0) return '<span class="pcg">Ready</span>';
    const d = Math.floor(r / 86400), h = Math.floor(r % 86400 / 3600), m = Math.floor(r % 3600 / 60);
    return d ? d + "d " + h + "h" : h ? h + "h " + String(m).padStart(2, "0") + "m" : Math.max(m, 1) + "m"; };
  function mats(x){ const miss = [], n = []; let bank = false;
    for (const [name, need, bags, total] of x.mats) { n.push(Math.floor(total / need));
      if (bags < need) { if (total >= need) bank = true; else miss.push((need - total) + "x " + name); } }
    if (miss.length) return ['<span class="pcr">Missing: ' + miss.join(", ") + "</span>", false];
    const k = Math.min(...n);
    return ['<span class="' + (bank ? 'pcy">Mats in bank' : 'pcg">Mats in bags') + "</span>" + (k > 1 ? ' <span class="pcm">(' + k + "x)</span>" : ""), !bank]; }
  function tip(){ $("pcTip").innerHTML = '<div style="color:#8cccf2;margin-bottom:4px">ProfCD</div>' + chars.map(c =>
      '<div style="color:' + c.c + ';margin-top:6px">' + c.n + "</div>" + c.cds.map(x => '<div class="l"><span>' + x.l + "</span><span>" + fmt(x.at) + "</span></div>").join("")).join("") +
      '<div class="pcm" style="margin-top:6px">Click: mats and details</div>'; }
  function win(){ $("pcWin").innerHTML = chars.map((c, ci) =>
      '<div class="c"><span style="color:' + c.c + '">' + c.n + '</span> <span class="pcm">' + (c.me ? "this character" : "as of " + c.seen) + "</span></div>" +
      c.cds.map((x, xi) => { const [st, ok] = mats(x); const go = c.me && ok && x.at <= now();
        return '<div class="r' + (go ? " go" : "") + '" data-c="' + ci + '" data-x="' + xi + '"><span>' + x.l + '</span><span class="t">' + fmt(x.at) + "</span><span>" + st + "</span></div>"; }).join("")).join(""); }
  $("pcBtn").onmouseenter = () => { tip(); $("pcTip").classList.add("on"); };
  $("pcBtn").onmouseleave = () => $("pcTip").classList.remove("on");
  $("pcBtn").onclick = () => { $("pcWin").classList.toggle("on"); win(); };
  $("pcWin").onclick = e => { const r = e.target.closest(".r.go"); if (!r) return;
    const x = chars[+r.dataset.c].cds[+r.dataset.x];
    for (const m of x.mats) { m[2] -= m[1]; m[3] -= m[1]; }
    x.at = now() + x.cd; $("pcInfo").textContent = x.l.replace("Transmute: ", "Transmuted ") + ". The cooldown starts."; win(); };
  setInterval(() => { if ($("pcWin").classList.contains("on")) win(); if ($("pcTip").classList.contains("on")) tip(); }, 1000);
})();
'''

TD_DEMO = '''
<div class="grid2">
  <div class="panel tddemo" style="padding:18px">
    <div class="row" style="justify-content:space-between;margin-bottom:12px">
      <b class="display" style="color:#7fd3fa">TrinketDock</b>
      <button class="sm" id="tdCombat">Enter combat</button>
    </div>
    <div class="tdstage" id="tdStage">
      <div class="tdfly" id="tdFly"></div>
      <div class="tddock" id="tdDock"></div>
    </div>
    <div class="small" id="tdInfo" style="margin-top:12px">Hover a button. Left-click a trinket for the top slot, right-click for the bottom slot.</div>
  </div>
  <div class="panel" style="padding:18px">
    <h2>How it plays</h2>
    <ul class="ticks" style="list-style:none;padding:0;margin:0;color:var(--muted)">
      <li style="margin:7px 0">Click a dock button to use the trinket, or bind a key.</li>
      <li style="margin:7px 0">Hover it: the trinkets in your bags fly out.</li>
      <li style="margin:7px 0">Out of combat a click swaps right away.</li>
      <li style="margin:7px 0">In combat the click queues the swap, shown by a small icon on the button. It happens the moment combat ends.</li>
      <li style="margin:7px 0">Nothing else runs: no bag scans when you loot, no work when combat starts or ends.</li>
    </ul>
  </div>
</div>'''
TD_CSS = '''
.tddemo{background:linear-gradient(180deg,#0d1a24,#05090d);border-color:#24506a}
.tdstage{position:relative;height:260px;display:flex;align-items:flex-end;justify-content:center}
.tddock{display:flex;gap:6px}
.tdfly{position:absolute;bottom:62px;display:flex;flex-direction:column-reverse;gap:6px}
.tdb{width:52px;height:52px;border-radius:8px;border:2px solid #3c4a5a;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:20px;color:#fff;position:relative;cursor:pointer;user-select:none;text-shadow:0 1px 2px #000}
.tdb:hover{border-color:#4fc3f7;box-shadow:0 0 12px rgba(79,195,247,.5)}
.tdb .q{position:absolute;right:-6px;bottom:-6px;width:22px;height:22px;border:2px solid #ffd100;border-radius:4px;font-size:11px;display:flex;align-items:center;justify-content:center}
.tdb .cd{position:absolute;inset:0;background:rgba(0,0,0,.6);border-radius:6px;font-size:13px;display:flex;align-items:center;justify-content:center}
.tdfly .tdb{width:44px;height:44px;font-size:16px}
.tdfly .tdb.mark{box-shadow:0 0 0 2px #ffd100 inset}
'''
TD_JS = '''
(function(){
  const $ = id => document.getElementById(id);
  const T = {
    sw: { n: "Nifty Stopwatch", c: "#3b6ea5", l: "S" },
    hoj: { n: "Hand of Justice", c: "#7a4a2a", l: "H" },
    bb: { n: "Blackhand's Breadth", c: "#8a2a2a", l: "B" },
    carrot: { n: "Carrot on a Stick", c: "#c06a1a", l: "C" },
    gd: { n: "Glyph of Deflection", c: "#4a7a9a", l: "G" },
  };
  let eq = { 13: "sw", 14: "hoj" }, bag = ["bb", "carrot", "gd"], queue = {}, combat = false, open = null, used = {};
  const box = (k, extra, cls) => `<div class="tdb${cls || ""}" style="background:${T[k].c}" ${extra || ""}>${T[k].l}`;
  function renderDock(){
    $("tdDock").innerHTML = [13, 14].map(s => box(eq[s], `data-slot="${s}" title="${T[eq[s]].n}"`) +
      (used[s] ? `<span class="cd">${used[s]}s</span>` : "") +
      (queue[s] ? `<span class="q" style="background:${T[queue[s]].c}">${T[queue[s]].l}</span>` : "") + "</div>").join("");
  }
  function renderFly(){
    if (!open) { $("tdFly").innerHTML = ""; return; }
    $("tdFly").style.left = open === 13 ? "calc(50% - 52px)" : "calc(50% + 6px)";
    $("tdFly").innerHTML = bag.map(k => box(k, `data-bag="${k}" title="${T[k].n}"`, (queue[13] === k || queue[14] === k) ? " mark" : "") + "</div>").join("");
  }
  function swap(k, s){ const i = bag.indexOf(k); if (i < 0) return; bag[i] = eq[s]; eq[s] = k; }
  $("tdDock").addEventListener("mouseover", e => { const b = e.target.closest("[data-slot]"); if (b) { open = +b.dataset.slot; renderFly(); } });
  $("tdDock").addEventListener("click", e => { const b = e.target.closest("[data-slot]"); if (!b) return; const s = +b.dataset.slot;
    if (used[s]) { $("tdInfo").textContent = "Still on cooldown."; return; }
    $("tdInfo").textContent = "Used " + T[eq[s]].n + "."; used[s] = 10; renderDock(); });
  $("tdStage").addEventListener("mouseleave", () => { open = null; renderFly(); });
  function pick(e, s){ const b = e.target.closest("[data-bag]"); if (!b) return; e.preventDefault(); const k = b.dataset.bag;
    if (combat) {
      if (queue[s] === k) { delete queue[s]; $("tdInfo").textContent = "Queue cleared."; }
      else { queue[s] = k; const o = s === 13 ? 14 : 13; if (queue[o] === k) delete queue[o];
        $("tdInfo").textContent = T[k].n + " queued for the " + (s === 13 ? "top" : "bottom") + " slot: swapped when combat ends."; }
    } else { swap(k, s); $("tdInfo").textContent = T[k].n + " equipped in the " + (s === 13 ? "top" : "bottom") + " slot."; open = null; }
    renderDock(); renderFly(); }
  $("tdFly").addEventListener("click", e => pick(e, 13));
  $("tdFly").addEventListener("contextmenu", e => pick(e, 14));
  $("tdCombat").onclick = () => {
    combat = !combat; $("tdCombat").textContent = combat ? "Leave combat" : "Enter combat"; $("tdCombat").classList.toggle("gold", combat);
    if (!combat) { const done = []; for (const s of [13, 14]) if (queue[s]) { done.push(T[queue[s]].n); swap(queue[s], s); } queue = {};
      $("tdInfo").textContent = done.length ? "Combat ended: swapped in " + done.join(" and ") + "." : "Out of combat."; }
    else $("tdInfo").textContent = "In combat: the flyout still opens, clicks queue the swap.";
    renderDock(); renderFly(); };
  setInterval(() => { let ch = false; for (const s of [13, 14]) if (used[s]) { used[s]--; ch = true; } if (ch) renderDock(); }, 1000);
  renderDock();
})();
'''

SS_DEMO = '''
<div class="grid2">
  <div class="panel ssdemo" style="padding:16px">
    <div class="row" style="gap:8px;margin-bottom:10px">
      <button class="sm ssbtn" data-a="kill">Kill a mob</button><button class="sm ssbtn" data-a="loot">Loot</button><button class="sm ssbtn" data-a="pull">Pull</button>
      <button class="sm" id="ssReset" style="margin-left:auto">Reset</button>
    </div>
    <canvas id="ssGraph" width="560" height="90" style="width:100%;height:90px;background:rgba(0,0,0,.45);border:1px solid #4a2c18;border-radius:6px"></canvas>
    <div class="small" id="ssStatus" style="margin:10px 0 6px">0 spikes recorded.</div>
    <div class="sstable" id="ssTable"></div>
  </div>
  <div class="panel" style="padding:18px">
    <h2>Recorded in game</h2>
    <img src="../media/spikespotter/window.jpg" alt="SpikeSpotter window in WoW Forever" loading="lazy" style="width:100%;border-radius:10px;border:1px solid var(--line)">
  </div>
</div>'''
SS_CSS = '''
.ssdemo{background:linear-gradient(180deg,#1f1209,#090503);border-color:#5a3418}
.ssdemo .ssbtn{background:#ff8a3d;border-color:#ffb27d;color:#1a0d05}
.sstable{font-size:13px}
.ssrow{display:grid;grid-template-columns:1fr 70px 60px 70px;gap:6px;padding:3px 6px;border-bottom:1px solid rgba(255,138,61,.12)}
.ssrow.h{color:#8d97a5}.ssrow span:not(:first-child){text-align:right;font-variant-numeric:tabular-nums}
'''
SS_JS = '''
(function(){
  const $ = id => document.getElementById(id);
  const cv = $("ssGraph"), g = cv.getContext("2d");
  const frames = Array(140).fill(16);
  const A = {
    kill: [["QuestTracker", 18, 26], ["GuideAddon", 8, 14], ["CombatText", 1, 3]],
    loot: [["FishingHelper", 30, 38], ["AuctionHelper", 20, 25], ["BagAddon", 3, 6]],
    pull: [["GearSwapper", 24, 30], ["UIFrames", 2, 4]],
  };
  let stats = {}, spikes = 0, engine = 0;
  const r = (a, b) => a + Math.random() * (b - a);
  function draw(){
    g.clearRect(0, 0, cv.width, cv.height);
    const y = ms => cv.height - Math.min(ms, 120) / 120 * (cv.height - 6);
    g.strokeStyle = "rgba(141,151,165,.5)"; g.lineWidth = 1; g.setLineDash([6, 6]); g.beginPath(); g.moveTo(0, y(40)); g.lineTo(cv.width, y(40)); g.stroke(); g.setLineDash([]);
    g.lineWidth = 2; g.beginPath();
    frames.forEach((ms, i) => { const x = i / (frames.length - 1) * cv.width; i ? g.lineTo(x, y(ms)) : g.moveTo(x, y(ms)); });
    g.strokeStyle = "#5d6d80"; g.stroke();
    frames.forEach((ms, i) => { if (ms > 40) { const x = i / (frames.length - 1) * cv.width; g.fillStyle = "#ff8a3d"; g.beginPath(); g.arc(x, y(ms), 4, 0, 7); g.fill(); } });
  }
  function table(){
    const list = Object.entries(stats).sort((a, b) => b[1].ms - a[1].ms);
    $("ssStatus").textContent = spikes + " spikes recorded, " + engine + " of them without a notable addon share (the game itself).";
    $("ssTable").innerHTML = '<div class="ssrow h"><span>Addon</span><span>total ms</span><span>spikes</span><span>worst ms</span></div>' +
      (list.length ? list.map(([n, s], i) => `<div class="ssrow"><span>${i + 1}. ${n}</span><span>${s.ms.toFixed(0)}</span><span>${s.n}</span><span>${s.max.toFixed(0)}</span></div>`).join("")
        : '<div class="ssrow"><span style="color:#8d97a5">Nothing yet. Kill, loot, pull.</span></div>');
  }
  function spike(kind){
    let sum = 0;
    if (Math.random() < 0.12) engine++;
    else for (const [n, a, b] of A[kind]) { const t = r(a, b); sum += t; const s = stats[n] || (stats[n] = { ms: 0, n: 0, max: 0 }); s.ms += t; s.n++; s.max = Math.max(s.max, t); }
    spikes++; frames.push(16 + sum + r(25, 35)); frames.shift(); table();
  }
  document.querySelectorAll(".ssbtn").forEach(b => b.onclick = () => spike(b.dataset.a));
  $("ssReset").onclick = () => { stats = {}; spikes = 0; engine = 0; table(); };
  setInterval(() => { frames.push(r(13, 19)); frames.shift(); draw(); }, 60);
  table(); draw();
})();
'''
SS_NOTE = '''<section class="section"><div class="note"><b style="color:var(--gold2)">Where it found real culprits.</b> On the author's own setup: a fishing helper and an auction helper at about 60 ms on every loot, an equipment manager at 27 ms on every combat start and end, a quest data collector at 20 ms on every quest kill. After disabling them the loot stutter was gone.</div></section>'''


def lst(items):
    return '<ul class="ticks" style="list-style:none;padding:0;margin:0;color:var(--muted)">' + "".join(f'<li style="padding-left:22px;position:relative;margin:7px 0"><span style="position:absolute;left:2px;color:var(--gold);font-size:11px;top:4px">◆</span>{md_inline(x)}</li>' for x in items) + "</ul>"


def build():
    (ROOT / "index.html").write_text(home(), encoding="utf-8")

    pf = showcase("procflare", PROC_DEMO, PROC_CSS, PROC_JS, [
        ("✦", "Clearcasting you cannot miss", "Big pulsing icon above your character while the buff is up, with the seconds left, a sound and a short flash at the screen edges. Omen of Clarity, Arcane Concentration and Elemental Focus, and Shadow Trance from Nightfall for warlocks."),
        ("⚡", "Reactive abilities", "Overpower and Revenge (warrior), Riposte (rogue), Mongoose Bite and Counterattack (hunter) show for the few seconds after a dodge, parry or block opens them. Only your class's ones."),
        ("♫", "Sound packs of its own", "**Melee**: war drums, war horn, axe clash, beast roar. **Caster**: arcane surge, mana burst, frost shatter, fire burst. Picked from your class, with volume and sound channel."),
        ("⚔", "Weapon, trinket and talent procs", "Small icons with a countdown and a softer sound. Crusader, trinkets and talent procs are picked up on their own, nothing to set up."),
        ("◎", "Procs on your target", "Debuffs your weapon or talents put on your target, such as Icy Chill or Spell Vulnerability."),
        ("✕", "Mute what you do not need", "In move mode your recent procs are shown: right-click one to mute or unmute it."),
        ("⚙", "Works in combat", "Forever hides buff details in combat. ProcFlare still finds Clearcasting by spell, by the game's own proc glow or by your abilities becoming free or instant, and asks for your class's known procs (Flurry, Enrage, Vengeance, Nature's Grace and more) by spell."),
        ("◈", "Light", "Classes without Clearcasting do not rescan their buffs on every resource change; with Clearcasting at most five times a second."),
    ], lst([
        "Its own **settings window**: drag it anywhere, it stays open while you play and every change applies at once. `/pfl`, or the **minimap button**: left-click the window, shift-click move mode, right-click preview.",
        "**Sound pack** (Melee or Caster), Clearcasting sound and proc sound, each from 12 own sounds or the game's.",
        "**Volume** 25 to 100 % and the **sound channel**: on Sound Effects by default, so the game's effects slider applies.",
        "Clearcasting (or Shadow Trance) alert and screen flash, other procs, reactive abilities, only your own procs.",
        "Longest buff that still counts as a proc (30 s by default), size and position.",
    ]), ingame("procflare", "A real screenshot: the Clearcasting alert above the character, proc icons with their countdowns, and the settings window.") + '''<section class="section"><div class="note"><b style="color:var(--gold2)">Limits.</b> Procs that only deal damage (Fiery Weapon, Lifestealing) or grant an extra attack (Hand of Justice, Windfury) cannot be shown: Forever keeps the combat log from addons. In restricted content (some boss encounters, battlegrounds) only Clearcasting is shown.</div></section>''',
        ["swingcast", "stattrim", "leveltrail"])
    (ROOT / "procflare").mkdir(exist_ok=True); (ROOT / "procflare" / "index.html").write_text(pf, encoding="utf-8")

    sc = showcase("swingcast", SWING_DEMO, SWING_CSS, SWING_JS, [
        ("◧", "Spell icon", "Inside the cast bar at its left end, or left of it, so you see what you are casting at a glance."),
        ("⧗", "Remaining cast time", "Counted down right on the bar."),
        ("▮", "Latency zone", "Red end of the bar: once the bar reaches it, the next spell can be pressed."),
        ("⚔", "Swing timer", "A thin strip right under the cast bar, with the seconds to the next swing."),
        ("◆", "Queued swing", "Orange while Maul, Heroic Strike or Raptor Strike is queued, blue for Cleave."),
        ("⚙", "Your look", "Height, font, font size and every colour, with the game's colour picker."),
    ], lst([
        "Switch on Forever's swing timer first: **Options > Advanced Options > Swing Timer**.",
        "Its own **settings window**: drag it anywhere, it stays open while you play and every change shows live. `/swc`, or the **minimap button**: left-click the window, right-click an 8 s preview.",
        "**Move the swing strip** in the game's Edit Mode or with \"Move strip\" in the window, or keep it under the cast bar.",
        "Show or hide icon, cast time, latency zone, swing strip and its seconds; hide the built-in swing bars.",
        "Advanced: `/swc help` lists every setting as a command.",
    ]), ingame("swingcast", "A real screenshot: the settings window and the swing strip under the cast bar, shown as a preview while the window is open.") + '''<section class="section"><div class="note"><b style="color:var(--gold2)">How it works.</b> The strip mirrors Forever's built-in swing timer, the only accurate source: Forever keeps the combat log from addons and hands attack speed to addons as secret values. If the strip ever fails, it switches itself off and the built-in bar comes back.</div></section>''',
        ["procflare", "stattrim", "leveltrail"])
    (ROOT / "swingcast").mkdir(exist_ok=True); (ROOT / "swingcast" / "index.html").write_text(sc, encoding="utf-8")

    st = showcase("stattrim", STAT_DEMO, STAT_CSS, STAT_JS, [
        ("☑", "Hide categories or stats", "A checkbox on every row, right in the character window."),
        ("≡", "Merge categories", "Hide only a category's name: its stats join the category above, for one compact list."),
        ("⇅", "Reorder", "Move categories and stats up and down with arrows."),
        ("⚙", "Edit in place", "Gear icon above the stats panel. Rows you turned off stay faded until you leave edit mode."),
        ("⛨", "Safe in combat", "StatTrim never touches Blizzard's stat list, it only moves and fades the finished rows."),
        ("◈", "Does nothing when idle", "Without hidden or moved stats StatTrim does no work at all."),
    ], lst([
        "Gear icon above the stats panel, or `/stt`.",
        "`/stt list`: all categories and stats in one window.",
        "`/stt reset` shows everything again, `/stt order` restores the original order.",
    ]), "", ["swingcast", "procflare", "leveltrail"])
    (ROOT / "stattrim").mkdir(exist_ok=True); (ROOT / "stattrim" / "index.html").write_text(st, encoding="utf-8")

    ts = showcase("transmogsweep", TS_DEMO, TS_CSS, TS_JS, [
        ("◩", "A tab of its own", "Right in the auction house window. The tabs of Auctionator, VendorFloor and other addons stay where they are."),
        ("⚡", "Fast scan", "Asks the auction house for weapons and armor only, grouped by item: a few seconds, no 15-minute wait, repeat it any time."),
        ("✓", "What the game says", "Collected counts account-wide, exactly as the item tooltip shows it: \"You haven't collected this appearance\"."),
        ("◈", "Unique appearances", "One row per look, the cheapest item that has it. Off: completionist mode, every source you lack."),
        ("▶", "Buy top to bottom", "\"Start buying\" checks the first item, the next click buys it, then the next row is checked by itself. One click per item."),
        ("⚙", "Filters", "Usable by my class, slot, search, maximum price, hide items above your level. Right-click hides a look you never want."),
        ("✎", "Recipes too", "A second list with the recipes your character has not learned yet, for its own professions, cheapest first. \"Learnable now\" keeps it to what your skill allows today."),
    ], lst([
        "Its own **settings window**: the gear in the tab or the addon menu at the minimap. Drag it anywhere, changes apply live.",
        "**Unique appearances**, **Usable by my class**, **Hide items above my level**, **Hide what I bought** (until you learn it).",
        "**Learnable now** for the recipe list: only recipes your skill, level and other requirements allow today.",
        "**Small tab**: follows VendorFloor or Auctionator when unset.",
        "**Show hidden appearances** and **Forget purchases** to reset.",
        "**Alt+click** a row shows a diagnosis to copy into a bug report.",
    ]), '''<section class="section"><div class="note"><b style="color:var(--gold2)">Learning a look.</b> Bought items arrive in the mail. Wear one or sell it to a vendor and the appearance is yours on every character. Until then it stays hidden in the list.</div></section>''',
        ["vendorfloor", "stattrim", "leveltrail"])
    (ROOT / "transmogsweep").mkdir(exist_ok=True); (ROOT / "transmogsweep" / "index.html").write_text(ts, encoding="utf-8")

    td = showcase("trinketdock", TD_DEMO, TD_CSS, TD_JS, [
        ("◧", "Two use buttons", "Your top and bottom trinket with their cooldowns. Click to use, or bind a key (Options > Keybindings > TrinketDock)."),
        ("⇡", "Flyout to swap", "Hover a button and every trinket in your bags shows up. Left-click equips it to the top slot, right-click to the bottom slot."),
        ("⧗", "Queue in combat", "Trinkets cannot be swapped in combat, so the flyout queues the swap. It happens the moment combat ends; a small icon on the button shows what is queued."),
        ("◈", "Light", "Bags are read only when the flyout opens. No work when you loot, none when combat starts or ends. Made as a slim replacement for ItemRack's trinket menu."),
        ("⚙", "Your layout", "Side by side or stacked, flyout up or down, any scale. Shift-drag to move, or lock it."),
    ], lst([
        "Its own **settings window**: `/tdock` or the addon menu at the minimap. Drag it anywhere, changes apply live.",
        "**Show the buttons**, **Lock position**, **Vertical**, **Tooltips**, **Scale**, flyout **upwards or downwards**, **Reset position**.",
        "**Keybindings** for both trinkets under Options > Keybindings > TrinketDock.",
    ]), ingame("trinketdock", "A real screenshot: the settings window with frame, background and opacity, and the dock with its flyout on the right."), ["spikespotter", "procflare", "swingcast"])
    (ROOT / "trinketdock").mkdir(exist_ok=True); (ROOT / "trinketdock" / "index.html").write_text(td, encoding="utf-8")

    ss = showcase("spikespotter", SS_DEMO, SS_CSS, SS_JS, [
        ("⚡", "Catches the stutter", "Watches the frame time. A frame that takes much longer than usual counts as a spike; loading screens are left out."),
        ("☰", "Ranking of the culprits", "Every addon that took part in a spike, with total time, how often and its worst frame, read from the game's own addon profiler."),
        ("◎", "Game or addon?", "Spikes where no addon took a notable share are counted apart: then the game itself is the cause, and disabling addons will not help."),
        ("✎", "Context", "Each spike is logged with the game events that fired just before (loot window, quest log update, combat start), so you see when an addon gets expensive."),
        ("⧉", "Copy report", "Ranking and the last 100 spikes as text, ready for a bug report to the addon at fault or a forum post."),
        ("⏻", "Off when you are done", "One switch stops all measuring; then SpikeSpotter costs nothing."),
    ], lst([
        "Its own **window**: `/spike` or the addon menu at the minimap. The ranking refreshes live while you play.",
        "**Watch for spikes**, **Chat message per spike**, **Spike threshold** (20 to 150 ms).",
        "**Reset** before a test, **Copy report** after it.",
        "How to use it: Reset, play a few minutes the way the stutter happens, look at the ranking, disable the top addon and test again.",
    ]), SS_NOTE, ["trinketdock", "vendorfloor", "procflare"])
    (ROOT / "spikespotter").mkdir(exist_ok=True); (ROOT / "spikespotter" / "index.html").write_text(ss, encoding="utf-8")

    pc = showcase("profcd", PC_DEMO, PC_CSS, PC_JS, [
        ("◷", "Timers on hover", "Hover the minimap button: every tracked cooldown of every character, with the time left or \"Ready\"."),
        ("⚗", "Mats check", "Click it: each craft shows \"Mats in bags\", \"Mats in bank\" or what is missing, and how many crafts the mats are enough for."),
        ("⧗", "Forever cooldowns", "Every transmute on its own cooldown (Arcanite, Truesilver, Gold, the elemental ones), plus Mooncloth and the Salt Shaker. Durations come from the game."),
        ("☰", "Recipes from the game", "Reagents are read from the profession window, so recipe changes in Forever show up on their own."),
        ("◎", "Alts included", "Other characters show as of their last login. /pcd forget removes one."),
        ("⌘", "Macro instead of a button", "Turn the minimap button off and ProfCD creates a macro: one click opens the window, the next closes it."),
    ], lst([
        "Its own **window**: the minimap button, `/pcd` or the addon menu at the minimap. Drag it anywhere, it stays open while you play.",
        "**Minimap button**, **Show other characters**, **Chat notice when ready**.",
        "`/pcd minimap` toggles the button, `/pcd forget <name>` removes a character.",
    ]), ingame("profcd", "A real screenshot: each transmute with its cooldown and whether the mats are in your bags."), ["trinketdock", "spikespotter", "vendorfloor"])
    (ROOT / "profcd").mkdir(exist_ok=True); (ROOT / "profcd" / "index.html").write_text(pc, encoding="utf-8")

    # tool pages: replace marked blocks
    for key in ("leveltrail", "vendorfloor"):
        p = ROOT / key / "index.html"
        s = p.read_text(encoding="utf-8")
        s = re.sub(r'assets/site\.(css|js)(\?v=\w+)?"', lambda m: f'assets/site.{m.group(1)}?v={ASSET_V}"', s)
        s = re.sub(r"<!--@header-->.*?<!--/@header-->", lambda m: f"<!--@header-->{header(key, '../')}<!--/@header-->", s, flags=re.S)
        s = re.sub(r"<!--@footer-->.*?<!--/@footer-->", lambda m: f"<!--@footer-->{footer('../')}<!--/@footer-->", s, flags=re.S)
        s = re.sub(r"<!--@changelog-->.*?<!--/@changelog-->", lambda m: f"<!--@changelog-->{changelog(key)}<!--/@changelog-->", s, flags=re.S)
        s = re.sub(r"<!--@version-->.*?<!--/@version-->", lambda m: f"<!--@version-->v{latest(key)}<!--/@version-->", s, flags=re.S)
        s = re.sub(r"<!--@goes-->.*?<!--/@goes-->", lambda m: f"<!--@goes-->{goes_with([k for k in ('procflare','swingcast','stattrim','transmogsweep','leveltrail','vendorfloor') if k != key][:3], '../')}<!--/@goes-->", s, flags=re.S)
        s = re.sub(r"<!--@community-->.*?<!--/@community-->", lambda m: f"<!--@community-->{community('../')}<!--/@community-->", s, flags=re.S)
        p.write_text(s, encoding="utf-8")
    print("built")


if __name__ == "__main__":
    build()
