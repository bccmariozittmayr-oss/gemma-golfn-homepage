# -*- coding: utf-8 -*-
"""Workshop-Flyer-Generator (HTML/CSS + Playwright) im Gemma-Golfn-CI (Juli-Stil).

Erzeugt aus einer Termin-JSON drei Formate: 1080x1080, 1920x1080 (16:9), A4 (PNG + PDF).
Nutzung:  python workshop_flyer_html.py workshop_september_2026.json
Output:   Werkzeuge/output/
Vorteil gegenueber gemini_flyer.py: kostenlos, 100% texttreu (keine KI-Tippfehler).
"""
import json, sys
from pathlib import Path
from datetime import datetime
from PIL import Image

SCRIPT_DIR = Path(__file__).parent
GG = Path(__file__).resolve().parents[4]  # .../01_Kunden/gemma-golfn
PROTO = GG / "projekte" / "Gemma Golfn Homepage" / "prototype"
SUJET = GG / "marketing" / "grafiken" / "Workshops" / "WORKSHOP LANGES SPIEL OHNE DATUM 1080 1080 .png"
HERO = PROTO / "hero-building-golden.jpg"

ASSETS = SCRIPT_DIR / "assets"
ASSETS.mkdir(exist_ok=True)
OUT = SCRIPT_DIR / "output"
OUT.mkdir(exist_ok=True)

# ---- Assets vorbereiten ----
logo_png = ASSETS / "gemma-golfn-logo.png"
if not logo_png.exists():
    Image.open(SUJET).crop((50, 36, 424, 154)).save(logo_png)

qr_png = ASSETS / "qr-workshop.png"
if not qr_png.exists():
    import qrcode
    qr = qrcode.QRCode(border=1, box_size=10)
    qr.add_data("https://workshop.metzenhof.at/")
    qr.make(fit=True)
    qr.make_image(fill_color="#14301d", back_color="white").save(qr_png)

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

WT = {0: "MO", 1: "DI", 2: "MI", 3: "DO", 4: "FR", 5: "SA", 6: "SO"}

# Icon je Thema: (Kreisfarbe, SVG-Inhalt weiss)
ICONS = {
    "langes spiel": ("#2e7d32", '<path d="M13 30V6l14 5-14 5" fill="#fff"/><rect x="12" y="6" width="2.6" height="26" rx="1.3" fill="#fff"/>'),
    "driver": ("#1565c0", '<circle cx="20" cy="12" r="6" fill="#fff"/><rect x="18.7" y="19" width="2.6" height="7" fill="#fff"/><path d="M13 26h14l-4 6h-6z" fill="#fff"/>'),
    "pitchen / bunker": ("#d9a514", '<circle cx="27" cy="10" r="4" fill="#fff"/><path d="M5 32q8-9 15-5t15 0v5H5z" fill="#fff"/>'),
    "chippen / putten": ("#1c1c1c", '<rect x="19" y="4" width="2.6" height="22" rx="1.3" fill="#fff"/><rect x="12" y="25" width="12" height="4.5" rx="2" fill="#fff"/><circle cx="30" cy="28.5" r="3" fill="#fff"/>'),
}

def icon_for(thema):
    return ICONS.get(thema.lower(), ICONS["langes spiel"])

def rows_html(termine):
    rows = []
    for t in termine:
        dt = datetime.strptime(t["datum"], "%d.%m.%Y")
        col, svg = icon_for(t["thema"])
        rows.append(f'''
        <div class="row">
          <div class="dat"><span class="wt">{WT[dt.weekday()]}</span><span class="dd">{t["datum"]}</span></div>
          <div class="ico" style="background:{col}"><svg viewBox="0 0 40 36">{svg}</svg></div>
          <div class="topic">{t["thema"].upper()}</div>
          <div class="time">{t["zeit"]}</div>
        </div>''')
    return "\n".join(rows)

def build_html(data, variant):
    """variant: sq | wide | a4"""
    monat, jahr = data["monat"], data["jahr"]
    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700;800;900&family=Barlow+Condensed:wght@600;700;800;900&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  :root {{
    --green-dark:#14301d; --green:#1a5632; --green-mid:#2e7d32;
    --lime:#a3c53c; --paper:#f5f4ee;
  }}
  body {{ font-family:'Barlow',Arial,sans-serif; width:var(--W); height:var(--H); overflow:hidden; background:var(--paper); }}
  .canvas {{ width:var(--W); height:var(--H); display:flex; flex-direction:column; position:relative; }}

  /* ---- HERO ---- */
  .hero {{ position:relative; flex:0 0 var(--heroH); background:url("{HERO.as_uri()}") center 62%/cover no-repeat; }}
  .hero::after {{ content:""; position:absolute; inset:0;
     background:linear-gradient(180deg, rgba(255,252,240,.18) 0%, rgba(255,252,240,0) 40%, rgba(245,244,238,0) 78%, var(--paper) 100%); }}
  .logo {{ position:absolute; top:var(--logoTop); left:50%; transform:translateX(-50%); z-index:3; }}
  .logo img {{ width:var(--logoW); display:block; border-radius:14px; box-shadow:0 6px 24px rgba(0,0,0,.28); }}
  .titlebox {{ position:absolute; left:var(--pad); bottom:26px; z-index:3; }}
  h1 {{ font-family:'Barlow Condensed','Barlow',sans-serif; font-weight:900; font-size:var(--h1); line-height:.92;
        color:var(--green-dark); letter-spacing:1px; text-shadow:0 2px 14px rgba(255,250,230,.75); }}
  .monat {{ font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:var(--h2); letter-spacing:10px;
        color:var(--green); margin-top:10px; text-shadow:0 1px 10px rgba(255,250,230,.75); }}
  .rule {{ width:200px; height:4px; background:var(--green); margin:14px 0 12px; }}
  .tagline {{ font-weight:700; font-size:var(--tag); letter-spacing:4px; color:#2b2b25;
        text-shadow:0 0 8px rgba(255,252,240,.9), 0 0 18px rgba(255,252,240,.8); }}
  .tagline b {{ color:var(--green-mid); }}

  /* ---- LISTE ---- */
  .list {{ flex:1 1 auto; padding:var(--listPadV) var(--pad) 8px; display:flex; flex-direction:column; justify-content:space-evenly; }}
  .row {{ display:flex; align-items:center; gap:var(--rowGap); border-top:1.5px solid rgba(20,48,29,.14); padding:var(--rowPad) 0; }}
  .row:first-child {{ border-top:none; }}
  .dat {{ width:var(--datW); display:flex; flex-direction:column; }}
  .wt {{ font-weight:700; font-size:var(--wtF); letter-spacing:2.5px; color:#8a8a80; }}
  .dd {{ font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:var(--ddF); color:var(--green-dark); }}
  .ico {{ width:var(--icoS); height:var(--icoS); border-radius:50%; flex:0 0 var(--icoS);
         display:flex; align-items:center; justify-content:center; box-shadow:0 3px 10px rgba(0,0,0,.18); }}
  .ico svg {{ width:58%; height:58%; }}
  .topic {{ flex:1; font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:var(--topF);
         letter-spacing:1px; color:#181818; }}
  .time {{ font-weight:600; font-size:var(--timF); color:#44443c; white-space:nowrap; }}

  /* ---- FOOTER ---- */
  .footer {{ flex:0 0 var(--footH); background:var(--green-dark); color:#fff;
         display:flex; flex-direction:column; justify-content:center; gap:var(--footGap); padding:14px var(--pad); position:relative; }}
  .chips {{ display:flex; justify-content:space-between; gap:12px; }}
  .chip {{ flex:1; text-align:center; border:1.5px solid rgba(255,255,255,.35); border-radius:12px; padding:var(--chipPad); }}
  .chip .t {{ font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:var(--chipT); letter-spacing:1.5px; }}
  .chip .s {{ font-weight:500; font-size:var(--chipS); color:var(--lime); letter-spacing:1px; margin-top:2px; }}
  .book {{ text-align:center; }}
  .book .line {{ font-weight:600; font-size:var(--bookS); letter-spacing:3px; color:rgba(255,255,255,.75); }}
  .book .url {{ font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:var(--bookU); letter-spacing:2px; color:var(--lime); margin-top:4px; }}
  .qr {{ position:absolute; right:26px; bottom:24px; background:#fff; border-radius:10px; padding:7px; }}
  .qr img {{ width:var(--qrS); display:block; }}
  .adresse {{ text-align:center; font-size:var(--adrF); color:rgba(255,255,255,.65); letter-spacing:1px; margin-top:2px; }}
'''
    if variant == "sq":
        html += '''
  :root,body { --W:1080px; --H:1080px; --heroH:430px; --pad:64px; --logoTop:26px; --logoW:250px;
    --h1:120px; --h2:46px; --tag:21px; --listPadV:18px; --rowGap:26px; --rowPad:10px;
    --datW:150px; --wtF:15px; --ddF:31px; --icoS:52px; --topF:36px; --timF:23px;
    --footH:236px; --footGap:14px; --chipPad:10px 6px; --chipT:20px; --chipS:13px;
    --bookS:15px; --bookU:34px; --adrF:0px; --qrS:0px; }
  .qr, .adresse { display:none; }
'''
    elif variant == "wide":
        html += '''
  :root,body { --W:1920px; --H:1080px; --heroH:430px; --pad:84px; --logoTop:24px; --logoW:240px;
    --h1:118px; --h2:46px; --tag:21px; --listPadV:12px; --rowGap:34px; --rowPad:8px;
    --datW:170px; --wtF:15px; --ddF:32px; --icoS:54px; --topF:38px; --timF:24px;
    --footH:210px; --footGap:12px; --chipPad:10px 6px; --chipT:21px; --chipS:14px;
    --bookS:15px; --bookU:34px; --adrF:0px; --qrS:0px; }
  .qr, .adresse { display:none; }
  .canvas { flex-direction:row; flex-wrap:wrap; }
  .hero { flex:0 0 46%; height:calc(var(--H) - var(--footH)); background-position:72% 62%; }
  .hero::after { background:linear-gradient(270deg, var(--paper) 0%, rgba(245,244,238,0) 16%, rgba(255,252,240,0) 55%, rgba(255,252,240,.28) 100%),
                 linear-gradient(0deg, rgba(255,252,240,.55) 0%, rgba(255,252,240,0) 34%); }
  .logo { left:36%; }
  .titlebox { left:var(--pad); bottom:40px; }
  .list { flex:0 0 54%; height:calc(var(--H) - var(--footH)); padding-top:36px; }
  .footer { flex:0 0 100%; }
'''
    else:  # a4 (1240x1754 @2x -> 2480x3508)
        html += '''
  :root,body { --W:1240px; --H:1754px; --heroH:600px; --pad:80px; --logoTop:40px; --logoW:300px;
    --h1:150px; --h2:56px; --tag:24px; --listPadV:36px; --rowGap:30px; --rowPad:16px;
    --datW:180px; --wtF:17px; --ddF:38px; --icoS:64px; --topF:46px; --timF:28px;
    --footH:400px; --footGap:22px; --chipPad:16px 8px; --chipT:24px; --chipS:16px;
    --bookS:18px; --bookU:44px; --adrF:17px; --qrS:130px; }
  .chips { padding-right:170px; }
  .book { padding-right:170px; }
  .adresse { padding-right:170px; }
'''
    hero_extra = ""
    html += f'''
</style></head><body>
<div class="canvas">
  <div class="hero">
    <div class="logo"><img src="{logo_png.as_uri()}"></div>
    <div class="titlebox">
      <h1>WORKSHOPS</h1>
      <div class="monat">{monat.upper()} {jahr}</div>
      <div class="rule"></div>
      <div class="tagline">TRAIN <b>SMARTER.</b> PLAY <b>BETTER.</b></div>
    </div>
  </div>
  <div class="list">
    {rows_html(data["termine"])}
  </div>
  <div class="footer">
    <div class="chips">
      <div class="chip"><div class="t">KLEINE GRUPPEN</div><div class="s">3–4 PERSONEN</div></div>
      <div class="chip"><div class="t">2 STUNDEN</div><div class="s">INTENSIVTRAINING</div></div>
      <div class="chip"><div class="t">€ 50</div><div class="s">PRO WORKSHOP</div></div>
      <div class="chip"><div class="t">GEMMA GOLFN</div><div class="s">KRONSTORF</div></div>
    </div>
    <div class="book">
      <div class="line">ONLINE BUCHEN. EINFACH. SCHNELL. TRANSPARENT.</div>
      <div class="url">workshop.metzenhof.at</div>
    </div>
    <div class="adresse">Golfpark Metzenhof · Dörfling 2, 4484 Kronstorf · office@gemma-golfn.at</div>
    <div class="qr"><img src="{qr_png.as_uri()}"></div>
  </div>
</div>
</body></html>'''
    return html

def render_all():
    from playwright.sync_api import sync_playwright
    stem = f"Workshops_{DATA['monat']}_{DATA['jahr']}"
    jobs = [
        ("sq",   1080, 1080, 1, f"{stem}_1080x1080.png"),
        ("wide", 1920, 1080, 1, f"{stem}_1920x1080.png"),
        ("a4",   1240, 1754, 2, f"{stem}_A4_Druck.png"),
    ]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for variant, w, h, scale, fname in jobs:
            html_file = OUT / f"flyer_{variant}.html"
            html_file.write_text(build_html(DATA, variant), encoding="utf-8")
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
            page.goto(html_file.as_uri())
            page.wait_for_timeout(1200)  # Fonts/Bilder laden
            page.screenshot(path=str(OUT / fname), full_page=False)
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
