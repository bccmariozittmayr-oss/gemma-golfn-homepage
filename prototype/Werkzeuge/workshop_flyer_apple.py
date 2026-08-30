# -*- coding: utf-8 -*-
"""Workshop-Flyer-Generator v2 — "Apple-Design"-Variante (HTML/CSS + Playwright).

Unterschiede zu workshop_flyer_html.py (v1, Juli-Stil):
  - Original-Gebaeudefoto (GG Gebaeude.png, Profifoto) statt KI-Golden-Hour
  - Original-Logo (Logo_Liegend.JPG aus den offiziellen Gemma-Golfn-Logos)
  - Reduziertes Layout: Weissraum, Hairline-Trenner, eine Akzentfarbe (CI-Gruen),
    keine bunten Icons — Vorgabe Mario 24.08.2026 ("TOP Apple Design Qualitaet")
  - Rendert in 2x-Aufloesung und rechnet mit Lanczos herunter -> scharfe Kanten

Erzeugt: 1080x1080, 1920x1080, A4 (PNG 300dpi + PDF).
Nutzung:  python workshop_flyer_apple.py [termine.json]
Output:   Werkzeuge/output/
"""
import json, sys
from pathlib import Path
from datetime import datetime
from PIL import Image

SCRIPT_DIR = Path(__file__).parent
GG = Path(__file__).resolve().parents[4]  # .../01_Kunden/gemma-golfn
ORIG = GG / "marketing" / "grafiken" / "Workshops" / "_originale"
HERO = ORIG / "GG Gebäude.png"
LOGO = ORIG / "Logo_Liegend.JPG"
QR = SCRIPT_DIR / "assets" / "qr-workshop.png"

OUT = SCRIPT_DIR / "output"
OUT.mkdir(exist_ok=True)

DATA = {
    "monat": "September", "jahr": "2026",
    "termine": [
        {"datum": "03.09.2026", "thema": "Langes Spiel", "zeit": "16:00 – 18:00 Uhr"},
        {"datum": "04.09.2026", "thema": "Pitchen / Bunker", "zeit": "13:00 – 15:00 Uhr"},
        {"datum": "10.09.2026", "thema": "Driver", "zeit": "16:00 – 18:00 Uhr"},
        {"datum": "23.09.2026", "thema": "Langes Spiel", "zeit": "16:00 – 18:00 Uhr"},
        {"datum": "29.09.2026", "thema": "Chippen / Putten", "zeit": "16:00 – 18:00 Uhr"},
    ],
}

WT = {0: "Montag", 1: "Dienstag", 2: "Mittwoch", 3: "Donnerstag", 4: "Freitag", 5: "Samstag", 6: "Sonntag"}

def rows_html(termine):
    rows = []
    for t in termine:
        dt = datetime.strptime(t["datum"], "%d.%m.%Y")
        dd = dt.strftime("%d.%m.")
        rows.append(f'''
        <div class="row">
          <div class="dat"><span class="wt">{WT[dt.weekday()]}</span><span class="dd">{dd}</span></div>
          <div class="topic">{t["thema"]}</div>
          <div class="time">{t["zeit"]}</div>
        </div>''')
    return "\n".join(rows)

def build_html(data, variant):
    monat, jahr = data["monat"], data["jahr"]
    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; -webkit-font-smoothing:antialiased; }}
  :root {{ --ink:#1d1d1f; --gray:#6e6e73; --gray2:#86868b; --line:#e5e5ea; --tile:#f5f5f7;
           --green:#1a5632; --green-bright:#217a3c; }}
  body {{ font-family:'Inter',-apple-system,'Segoe UI',sans-serif; width:var(--W); height:var(--H);
          overflow:hidden; background:#fff; color:var(--ink); }}
  .canvas {{ width:var(--W); height:var(--H); display:flex; flex-direction:column; }}

  .hero {{ position:relative; flex:0 0 var(--heroH);
           background:url("{HERO.as_uri()}") center 42%/cover no-repeat; }}
  .hero::after {{ content:""; position:absolute; inset:0;
           background:linear-gradient(180deg, rgba(0,0,0,.10) 0%, rgba(0,0,0,0) 30%); }}
  .logo {{ position:absolute; top:var(--logoPad); left:var(--logoPad); z-index:2; }}
  .logo img {{ width:var(--logoW); display:block; border-radius:var(--logoR);
           box-shadow:0 4px 18px rgba(0,0,0,.22); }}

  .head {{ padding:var(--headPadT) var(--pad) 0; }}
  h1 {{ font-size:var(--h1); font-weight:800; letter-spacing:-0.025em; line-height:1; }}
  .sub {{ margin-top:var(--subMT); font-size:var(--sub); font-weight:600; color:var(--green-bright); letter-spacing:-0.01em; }}
  .sub span {{ color:var(--gray2); font-weight:500; }}

  .list {{ flex:1 1 auto; margin:var(--listMT) var(--pad) 0; display:flex; flex-direction:column; justify-content:space-evenly; }}
  .row {{ display:flex; align-items:baseline; gap:var(--rowGap); border-top:1px solid var(--line); padding:var(--rowPad) 0; }}
  .row:first-child {{ border-top:none; }}
  .dat {{ width:var(--datW); flex:0 0 var(--datW); display:flex; flex-direction:column; }}
  .wt {{ font-size:var(--wtF); font-weight:500; color:var(--gray2); }}
  .dd {{ font-size:var(--ddF); font-weight:700; letter-spacing:-0.02em; margin-top:2px; }}
  .topic {{ flex:1; font-size:var(--topF); font-weight:700; letter-spacing:-0.02em; }}
  .time {{ font-size:var(--timF); font-weight:500; color:var(--gray); white-space:nowrap; }}

  .tiles {{ display:flex; gap:var(--tileGap); margin:var(--tilesMT) var(--pad) 0; }}
  .tile {{ flex:1; background:var(--tile); border-radius:var(--tileR); text-align:center; padding:var(--tilePad); }}
  .tile .t {{ font-size:var(--tileT); font-weight:700; letter-spacing:-0.02em; }}
  .tile .s {{ font-size:var(--tileS); font-weight:500; color:var(--gray2); margin-top:3px; }}

  .cta {{ margin:var(--ctaMT) var(--pad) var(--ctaMB); display:flex; align-items:center; justify-content:space-between; gap:20px; }}
  .cta .hint {{ font-size:var(--hintF); font-weight:500; color:var(--gray); line-height:1.45; }}
  .cta .hint b {{ color:var(--ink); font-weight:700; }}
  .pill {{ background:var(--green); color:#fff; border-radius:999px; padding:var(--pillPad);
           font-size:var(--pillF); font-weight:700; letter-spacing:-0.01em; white-space:nowrap; }}
  .qr {{ flex:0 0 auto; background:#fff; border:1px solid var(--line); border-radius:14px; padding:8px; }}
  .qr img {{ width:var(--qrS); display:block; }}
'''
    if variant == "sq":
        html += '''
  :root,body { --W:1080px; --H:1080px; --heroH:352px; --pad:60px; --logoPad:26px; --logoW:180px; --logoR:12px;
    --headPadT:30px; --h1:64px; --subMT:8px; --sub:24px;
    --listMT:8px; --rowGap:22px; --rowPad:8px; --datW:175px; --wtF:14px; --ddF:26px; --topF:28px; --timF:20px;
    --tilesMT:4px; --tileGap:13px; --tileR:16px; --tilePad:13px 8px; --tileT:19px; --tileS:12px;
    --ctaMT:18px; --ctaMB:30px; --hintF:14px; --pillPad:16px 28px; --pillF:22px; --qrS:0px; }
  .qr { display:none; }
'''
    elif variant == "wide":
        html += '''
  :root,body { --W:1920px; --H:1080px; --heroH:0px; --pad:80px; --logoPad:32px; --logoW:200px; --logoR:12px;
    --headPadT:64px; --h1:82px; --subMT:12px; --sub:28px;
    --listMT:20px; --rowGap:26px; --rowPad:14px; --datW:200px; --wtF:16px; --ddF:31px; --topF:32px; --timF:23px;
    --tilesMT:14px; --tileGap:14px; --tileR:18px; --tilePad:18px 8px; --tileT:22px; --tileS:14px;
    --ctaMT:30px; --ctaMB:56px; --hintF:17px; --pillPad:22px 38px; --pillF:26px; --qrS:0px; }
  .qr { display:none; }
  .canvas { flex-direction:row; }
  .left { flex:0 0 55%; display:flex; flex-direction:column; }
  .hero { flex:0 0 45%; height:100%; background-position:38% center; }
  .hero::after { background:linear-gradient(90deg, rgba(0,0,0,.06) 0%, rgba(0,0,0,0) 22%); }
  .logo { top:auto; left:auto; right:36px; bottom:36px; }
'''
    else:  # a4
        html += '''
  :root,body { --W:1240px; --H:1754px; --heroH:560px; --pad:88px; --logoPad:36px; --logoW:230px; --logoR:14px;
    --headPadT:56px; --h1:104px; --subMT:14px; --sub:33px;
    --listMT:30px; --rowGap:28px; --rowPad:20px; --datW:230px; --wtF:19px; --ddF:37px; --topF:39px; --timF:27px;
    --tilesMT:20px; --tileGap:16px; --tileR:20px; --tilePad:22px 10px; --tileT:26px; --tileS:16px;
    --ctaMT:40px; --ctaMB:60px; --hintF:19px; --pillPad:24px 42px; --pillF:30px; --qrS:130px; }
'''
    body_inner = f'''
    <div class="head">
      <h1>Workshops.</h1>
      <div class="sub">{monat} {jahr} <span>· Golfpark Metzenhof, Kronstorf</span></div>
    </div>
    <div class="list">
      {rows_html(data["termine"])}
    </div>
    <div class="tiles">
      <div class="tile"><div class="t">3–4</div><div class="s">Personen pro Gruppe</div></div>
      <div class="tile"><div class="t">2 Stunden</div><div class="s">Intensivtraining</div></div>
      <div class="tile"><div class="t">€ 50</div><div class="s">pro Workshop</div></div>
    </div>
    <div class="cta">
      <div class="hint">Online buchen. Einfach. Schnell. Transparent.<br><b>Dörfling 2, 4484 Kronstorf</b></div>
      <div class="pill">workshop.metzenhof.at</div>
      <div class="qr"><img src="{QR.as_uri()}"></div>
    </div>'''
    if variant == "wide":
        html += f'''
</style></head><body>
<div class="canvas">
  <div class="left">{body_inner}</div>
  <div class="hero"><div class="logo"><img src="{LOGO.as_uri()}"></div></div>
</div>
</body></html>'''
    else:
        html += f'''
</style></head><body>
<div class="canvas">
  <div class="hero"><div class="logo"><img src="{LOGO.as_uri()}"></div></div>
  {body_inner}
</div>
</body></html>'''
    return html

def render_all():
    from playwright.sync_api import sync_playwright
    stem = f"Workshops_{DATA['monat']}_{DATA['jahr']}"
    jobs = [  # (variant, w, h, scale, ziel-endgroesse, dateiname)
        ("sq",   1080, 1080, 2, (1080, 1080), f"{stem}_1080x1080.png"),
        ("wide", 1920, 1080, 2, (1920, 1080), f"{stem}_1920x1080.png"),
        ("a4",   1240, 1754, 2, None,         f"{stem}_A4_Druck.png"),
    ]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for variant, w, h, scale, final, fname in jobs:
            html_file = OUT / f"flyer_{variant}.html"
            html_file.write_text(build_html(DATA, variant), encoding="utf-8")
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
            page.goto(html_file.as_uri())
            page.wait_for_timeout(1500)
            page.screenshot(path=str(OUT / fname), full_page=False)
            if final:  # 2x gerendert -> scharf herunterrechnen
                img = Image.open(OUT / fname)
                img.resize(final, Image.LANCZOS).save(OUT / fname, optimize=True)
            print("OK", fname)
            if variant == "a4":
                page.pdf(path=str(OUT / f"{stem}_A4_Druck.pdf"),
                         width="210mm", height="297mm", print_background=True, scale=0.68)
                print("OK PDF")
            page.close()
        browser.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            DATA = json.load(f)
    render_all()
