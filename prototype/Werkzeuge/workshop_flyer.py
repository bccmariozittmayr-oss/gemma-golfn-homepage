"""
Workshop-Flyer-Generator fuer Gemma Golfn
==========================================
Erstellt Workshop-Flyer im CI-Design (Juli-2026-Stil).
Output: 1080x1080 (Social) + A4 (Druck)

Nutzung:
  python workshop_flyer.py

Das Script fragt interaktiv nach Monat/Jahr und den Workshop-Terminen.
Alternativ: JSON-Datei als Argument uebergeben (siehe workshops_beispiel.json).
"""

import json
import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# --------------- KONFIGURATION ---------------

# Farben (Gemma Golfn CI)
GREEN_DARK = (26, 105, 59)
GREEN_BG = (34, 60, 46)
WHITE = (255, 255, 255)
WHITE_70 = (255, 255, 255, 179)
WHITE_50 = (255, 255, 255, 128)
WHITE_30 = (255, 255, 255, 77)
OVERLAY = (20, 40, 30, 180)

# Wochentage
WOCHENTAGE = {
    "MO": "Montag", "DI": "Dienstag", "MI": "Mittwoch",
    "DO": "Donnerstag", "FR": "Freitag", "SA": "Samstag", "SO": "Sonntag"
}
WOCHENTAG_KURZ = {
    0: "MO", 1: "DI", 2: "MI", 3: "DO", 4: "FR", 5: "SA", 6: "SO"
}

# Pfade
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
ASSETS_DIR = SCRIPT_DIR / "assets"
OUTPUT_DIR = PROJECT_DIR / "Aktuelle Aktionen"

# Workshop-Icons (Emoji-Symbole als Text)
TOPIC_ICONS = {
    "LANGES SPIEL": "🏌",
    "DRIVER": "🏌",
    "PITCHEN": "⛳",
    "PITCHEN / BUNKER": "⛳",
    "CHIPPEN": "⛳",
    "CHIPPEN / PITCHEN": "⛳",
    "PUTTEN": "🎯",
    "BUNKER": "⛳",
    "KURZES SPIEL": "⛳",
}


def get_system_font(bold=False, size=32):
    """Versucht eine passende Systemschrift zu finden."""
    font_names = []
    if bold:
        font_names = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
            "C:/Windows/Fonts/segoeui b.ttf",
        ]
    else:
        font_names = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]

    for font_path in font_names:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)

    return ImageFont.load_default()


def create_workshop_flyer_1080(data):
    """Erstellt einen 1080x1080 Workshop-Flyer."""
    monat = data["monat"]
    jahr = data["jahr"]
    termine = data["termine"]

    img = Image.new("RGBA", (1080, 1080), GREEN_BG)
    draw = ImageDraw.Draw(img)

    # Hintergrundbild laden falls vorhanden
    bg_path = ASSETS_DIR / "metzenhof_bg.png"
    if bg_path.exists():
        bg = Image.open(bg_path).convert("RGBA")
        bg = bg.resize((1080, 400))
        bg.putalpha(Image.eval(bg.split()[3], lambda x: int(x * 0.4)))
        img.paste(bg, (0, 80), bg)

    # Dunkles Overlay fuer Lesbarkeit
    overlay = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([0, 0, 1080, 1080], fill=(20, 40, 30, 140))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # ---- HEADER ----

    # Logo-Bereich (weisser abgerundeter Kasten oben mitte)
    logo_x, logo_y = 440, 30
    logo_w, logo_h = 200, 90
    draw.rounded_rectangle(
        [logo_x, logo_y, logo_x + logo_w, logo_y + logo_h],
        radius=12, fill=WHITE
    )
    font_logo_big = get_system_font(bold=True, size=28)
    font_logo_small = get_system_font(bold=True, size=20)

    # Gemma Golfn Text im Logo-Kasten
    draw.text((logo_x + 55, logo_y + 15), "GEMMA", fill=GREEN_DARK, font=font_logo_big)
    draw.text((logo_x + 58, logo_y + 48), "GOLFN", fill=GREEN_DARK, font=font_logo_big)

    # Gruener Balken links im Logo
    draw.rectangle([logo_x + 10, logo_y + 10, logo_x + 45, logo_y + logo_h - 10], fill=GREEN_DARK)
    font_icon = get_system_font(bold=False, size=22)
    draw.text((logo_x + 17, logo_y + 22), "⛳", fill=WHITE, font=font_icon)

    # ---- TITEL ----
    font_title = get_system_font(bold=True, size=72)
    font_subtitle = get_system_font(bold=True, size=36)
    font_tagline = get_system_font(bold=False, size=22)

    draw.text((540, 150), "WORKSHOPS", fill=WHITE, font=font_title, anchor="mt")
    draw.text((540, 230), f"{monat.upper()} {jahr}", fill=WHITE, font=font_subtitle, anchor="mt")

    draw.text((540, 285), "TRAIN SMARTER.", fill=WHITE_70, font=font_tagline, anchor="mt")
    draw.text((540, 312), "PLAY BETTER.", fill=WHITE_70, font=font_tagline, anchor="mt")

    # ---- TERMINE-LISTE ----
    font_day_label = get_system_font(bold=True, size=18)
    font_date = get_system_font(bold=True, size=20)
    font_topic = get_system_font(bold=True, size=28)
    font_time = get_system_font(bold=False, size=22)

    y_start = 370
    row_height = 72
    left_margin = 80

    for i, termin in enumerate(termine):
        y = y_start + i * row_height

        # Trennlinie
        if i > 0:
            draw.line([(left_margin, y - 8), (1000, y - 8)], fill=WHITE_30, width=1)

        # Wochentag + Datum links
        from datetime import datetime
        try:
            dt = datetime.strptime(termin["datum"], "%d.%m.%Y")
            wt = WOCHENTAG_KURZ[dt.weekday()]
        except (ValueError, KeyError):
            wt = "??"

        draw.text((left_margin, y), wt, fill=WHITE_50, font=font_day_label)
        draw.text((left_margin, y + 22), termin["datum"], fill=WHITE, font=font_date)

        # Icon-Kreis
        icon_x = 300
        draw.ellipse([icon_x, y + 5, icon_x + 45, y + 50], fill=GREEN_DARK)
        draw.text((icon_x + 12, y + 12), "⛳", fill=WHITE, font=font_icon)

        # Thema
        draw.text((370, y + 8), termin["thema"].upper(), fill=WHITE, font=font_topic)

        # Uhrzeit rechts
        draw.text((880, y + 12), termin["zeit"], fill=WHITE_70, font=font_time)

    # ---- FOOTER ----
    footer_y = 900

    # Info-Boxen
    box_w = 280
    boxes = [
        ("KLEINE GRUPPEN", "3-4 PERSONEN"),
        ("2 STUNDEN", "INTENSIVTRAINING"),
        ("€50", "PRO WORKSHOP"),
    ]
    font_box_title = get_system_font(bold=True, size=18)
    font_box_sub = get_system_font(bold=False, size=14)

    for j, (title, sub) in enumerate(boxes):
        bx = 80 + j * (box_w + 30)
        draw.rounded_rectangle(
            [bx, footer_y, bx + box_w, footer_y + 55],
            radius=8, fill=WHITE_30
        )
        draw.text((bx + box_w // 2, footer_y + 12), title, fill=WHITE, font=font_box_title, anchor="mt")
        draw.text((bx + box_w // 2, footer_y + 33), sub, fill=WHITE_70, font=font_box_sub, anchor="mt")

    # URL-Zeile
    font_url_label = get_system_font(bold=False, size=16)
    font_url = get_system_font(bold=True, size=20)
    draw.text((540, 980), "ONLINE BUCHEN. EINFACH. SCHNELL. TRANSPARENT.", fill=WHITE_50, font=font_url_label, anchor="mt")
    draw.text((540, 1010), "workshop.metzenhof.at", fill=WHITE, font=font_url, anchor="mt")

    # QR-Code einfuegen falls vorhanden
    qr_path = Path(SCRIPT_DIR).parent.parent / "Workshops" / "qr-code Workshop Metzehof Plattform.png"
    if qr_path.exists():
        qr = Image.open(qr_path).convert("RGBA").resize((70, 70))
        img.paste(qr, (20, 990), qr)

    return img.convert("RGB")


def create_workshop_flyer_a4(data):
    """Erstellt einen A4-Flyer (2480x3508 px bei 300 DPI) basierend auf dem 1080-Design."""
    # A4 bei 300 DPI
    a4_w, a4_h = 2480, 3508
    img_1080 = create_workshop_flyer_1080(data).convert("RGBA")

    # A4-Canvas erstellen
    a4 = Image.new("RGB", (a4_w, a4_h), GREEN_BG)

    # 1080er-Flyer zentriert auf A4 skalieren (Breite nutzen, Rest als Rahmen)
    scale = a4_w / 1080
    scaled_size = (a4_w, int(1080 * scale))
    img_scaled = img_1080.resize(scaled_size, Image.LANCZOS)

    # Zentriert platzieren
    y_offset = (a4_h - scaled_size[1]) // 2
    a4.paste(img_scaled.convert("RGB"), (0, y_offset))

    # Oben und unten Gemma Golfn Branding
    draw = ImageDraw.Draw(a4)
    font_brand = get_system_font(bold=True, size=60)
    font_info = get_system_font(bold=False, size=36)

    draw.text((a4_w // 2, 80), "GEMMA GOLFN", fill=WHITE, font=font_brand, anchor="mt")
    draw.text((a4_w // 2, 150), f"Workshops {data['monat']} {data['jahr']}", fill=WHITE_70[:3], font=font_info, anchor="mt")

    draw.text((a4_w // 2, a4_h - 120), "Golfpark Metzenhof · Dörfling 2, 4484 Kronstorf", fill=WHITE_70[:3], font=font_info, anchor="mt")
    draw.text((a4_w // 2, a4_h - 60), "office@gemma-golfn.at · +43 7225 7389 10", fill=WHITE_50[:3], font=font_info, anchor="mt")

    return a4


def interaktiv_eingabe():
    """Fragt Workshop-Daten interaktiv ab."""
    print("\n" + "=" * 50)
    print("  GEMMA GOLFN – Workshop-Flyer-Generator")
    print("=" * 50 + "\n")

    monat = input("Monat (z.B. August): ").strip()
    jahr = input("Jahr (z.B. 2026): ").strip()

    print(f"\nTermine fuer {monat} {jahr} eingeben.")
    print("Format pro Termin: DATUM;THEMA;UHRZEIT")
    print("Beispiel: 02.08.2026;Langes Spiel;16:00 - 18:00 Uhr")
    print("Leere Zeile = fertig.\n")

    termine = []
    while True:
        zeile = input(f"Termin {len(termine) + 1}: ").strip()
        if not zeile:
            break
        teile = zeile.split(";")
        if len(teile) != 3:
            print("  ! Format: DATUM;THEMA;UHRZEIT - bitte nochmal.")
            continue
        termine.append({
            "datum": teile[0].strip(),
            "thema": teile[1].strip(),
            "zeit": teile[2].strip()
        })

    if not termine:
        print("Keine Termine eingegeben. Abbruch.")
        sys.exit(1)

    return {"monat": monat, "jahr": jahr, "termine": termine}


def main():
    # Assets-Ordner erstellen falls noetig
    ASSETS_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Daten laden: aus JSON-Datei oder interaktiv
    if len(sys.argv) > 1:
        json_path = Path(sys.argv[1])
        if not json_path.exists():
            print(f"Datei nicht gefunden: {json_path}")
            sys.exit(1)
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Workshop-Daten geladen aus: {json_path}")
    else:
        data = interaktiv_eingabe()

    monat = data["monat"]
    jahr = data["jahr"]
    print(f"\nErstelle Flyer fuer: Workshops {monat} {jahr}")
    print(f"Termine: {len(data['termine'])}")

    # 1080x1080 Social Media
    print("\n> Erstelle 1080x1080 (Social Media)...")
    img_1080 = create_workshop_flyer_1080(data)
    name_1080 = f"Workshop {monat} {jahr} 1080_1080PNG Gültig bis Ende {monat}.png"
    path_1080 = OUTPUT_DIR / name_1080
    img_1080.save(path_1080, "PNG", quality=95)
    print(f"  OK Gespeichert: {path_1080}")

    # A4 Druck
    print("> Erstelle A4 Druckformat...")
    img_a4 = create_workshop_flyer_a4(data)
    name_a4 = f"Workshop {monat} {jahr} A4 Druck.png"
    path_a4 = OUTPUT_DIR / name_a4
    img_a4.save(path_a4, "PNG", quality=95, dpi=(300, 300))
    print(f"  ✓ Gespeichert: {path_a4}")

    # aktionen.json automatisch aktualisieren
    json_path = OUTPUT_DIR / "aktionen.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            aktionen = json.load(f)
    else:
        aktionen = []

    # Pruefen ob Eintrag schon existiert
    bereits_da = any(a["bild"] == name_1080 for a in aktionen)
    if not bereits_da:
        # Letzten Tag des Monats berechnen
        import calendar
        monat_nr = {
            "Januar": 1, "Februar": 2, "März": 3, "April": 4, "Mai": 5, "Juni": 6,
            "Juli": 7, "August": 8, "September": 9, "Oktober": 10, "November": 11, "Dezember": 12
        }.get(monat, 1)
        letzter_tag = calendar.monthrange(int(jahr), monat_nr)[1]
        expires = f"{jahr}-{monat_nr:02d}-{letzter_tag}"

        aktionen.append({
            "bild": name_1080,
            "titel": f"Workshops {monat} {jahr}",
            "text": "ab € 50,- · Kleine Gruppen, 2h intensives Training",
            "link": "https://workshop.metzenhof.at/",
            "expires": expires
        })
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(aktionen, f, ensure_ascii=False, indent=2)
        print(f"\nOK aktionen.json aktualisiert (expires: {expires})")

    print("\n" + "=" * 50)
    print("  FERTIG! Flyer wurden erstellt und in den")
    print("  Aktionen-Ordner gelegt. Die Homepage zeigt")
    print("  sie automatisch an.")
    print("=" * 50)


if __name__ == "__main__":
    main()
