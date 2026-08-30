"""
Gemini Flyer-Generator fuer Gemma Golfn
========================================
Generiert Flyer ueber Google Gemini AI im Gemma Golfn CI.
Output: 1080x1080 (Social) + optional A4 (Druck)
Speichert automatisch in den Aktuelle Aktionen Ordner + aktionen.json

Nutzung:
  python gemini_flyer.py                          (interaktiv)
  python gemini_flyer.py workshop_august_2026.json (aus JSON)

Benoetigt: .env Datei mit GEMINI_API_KEY
"""

import json
import sys
import os
import calendar
import base64
from pathlib import Path
from datetime import datetime

# dotenv laden
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# --------------- KONFIGURATION ---------------

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR.parent / "Aktuelle Aktionen"
CI_FILE = SCRIPT_DIR.parent.parent.parent / "Gemma Golfn Premium Clean CI.md"

WOCHENTAG_KURZ = {0: "MO", 1: "DI", 2: "MI", 3: "DO", 4: "FR", 5: "SA", 6: "SO"}

MONAT_NR = {
    "Januar": 1, "Februar": 2, "Maerz": 3, "Maerz": 3, "April": 4,
    "Mai": 5, "Juni": 6, "Juli": 7, "August": 8, "September": 9,
    "Oktober": 10, "November": 11, "Dezember": 12
}


def load_ci_guidelines():
    """Laedt die CI-Richtlinien falls vorhanden."""
    if CI_FILE.exists():
        return CI_FILE.read_text(encoding="utf-8")
    return ""


def build_workshop_prompt(data):
    """Baut einen optimierten Prompt fuer Gemini Bildgenerierung."""
    monat = data["monat"]
    jahr = data["jahr"]
    termine = data["termine"]

    # Termine als exakte Liste formatieren
    termine_text = ""
    for i, t in enumerate(termine):
        try:
            dt = datetime.strptime(t["datum"], "%d.%m.%Y")
            wt = WOCHENTAG_KURZ[dt.weekday()]
        except (ValueError, KeyError):
            wt = "??"
        termine_text += f"Row {i+1}: Left side \"{wt}\" above \"{t['datum']}\", green circle icon in middle, \"{t['thema'].upper()}\" in bold white, right side \"{t['zeit']}\"\n"

    prompt = f"""I am attaching a reference flyer image. Recreate this EXACT same design but with updated content for {monat} {jahr}.

The attached image shows the EXACT layout, typography, colors, spacing and style I need. Copy this design pixel-perfectly but change ONLY the month, dates and workshop topics.

KEEP IDENTICAL from the reference:
- The exact same Gemma Golfn logo at top (white rounded box with golfer silhouette icon and "GEMMA GOLFN" text)
- The word "WORKSHOPS" in the exact same huge bold condensed white font
- "TRAIN SMARTER. PLAY BETTER." tagline in italics
- The exact same dark green gradient overlay on the bottom half
- The building/golf course photo visible in the upper portion
- Green circular icons next to each workshop topic (golf flag icon for Langes Spiel, golf club icon for Driver, sand/bunker icon for Pitchen/Bunker, target/putting icon for Putten, flag icon for Kurzes Spiel)
- Thin horizontal separator lines between each workshop row
- The bottom info bar with 4 rounded dark boxes: "KLEINE GRUPPEN 2-4 PERSONEN" | "2 STUNDEN INTENSIVTRAINING" | "EUR50 PRO WORKSHOP" | "GEMMA GOLFN KRONSTORF"
- Footer text: "ONLINE BUCHEN. EINFACH. SCHNELL. TRANSPARENT."
- Website: "workshop.metzenhof.at" in bold at very bottom
- Color scheme: dark forest green (#1a3c2b), white text, green (#1a693b) circle icons

CHANGE to new content:
- Month: "{monat.upper()} {jahr}" (instead of the month shown in reference)
- Workshop schedule (exactly {len(termine)} rows):
{termine_text}
CRITICAL RULES:
- Output must be EXACTLY 1080x1080 pixels square format
- ALL text must be PERFECTLY SPELLED with zero errors
- ALL {len(termine)} workshop rows must appear - do NOT skip any
- Every date, weekday, topic and time must match EXACTLY as listed above
- The design must look like a professional print-ready marketing flyer
- Premium quality, Apple-clean aesthetic"""

    return prompt


def build_custom_prompt(data):
    """Baut einen Prompt fuer individuelle/kreative Flyer."""
    ci = load_ci_guidelines()
    ci_section = f"\n\nCI GUIDELINES:\n{ci}" if ci else ""

    prompt = f"""Create a professional marketing flyer for GEMMA GOLFN (premium golf driving range in Austria).

FORMAT: Square 1080x1080 pixels

CONTENT:
Title: {data.get('titel', 'GEMMA GOLFN')}
Description: {data.get('beschreibung', '')}
Price: {data.get('preis', '')}
Valid until: {data.get('gueltig_bis', '')}
Call to action: {data.get('cta', 'Jetzt buchen')}
Contact: office@gemma-golfn.at | +43 7225 7389 10

STYLE: Premium, modern, Apple-clean aesthetic. Dark green and white color scheme.
Brand colors: Dark green (#1a693b), White, Black
The GEMMA GOLFN logo (white text on green rounded rectangle) should be at the top.
{ci_section}

CRITICAL: All text must be exactly as specified, perfectly readable and correctly spelled. No placeholder text. This is real marketing material for print and social media."""

    return prompt


def generate_image(prompt, api_key):
    """Sendet Prompt an Gemini/Imagen und gibt das generierte Bild zurueck."""
    client = genai.Client(api_key=api_key)

    # Referenzbild laden falls vorhanden
    reference_images = []
    ref_dir = Path(__file__).parent.parent / "Aktuelle Aktionen"

    # Juli-Flyer als Referenz
    for ref_name in [
        "Workshop Juli 2026 1080_1080PNG Gueltig bis Ende Juli.png",
        "Workshop Juli 2026 1080_1080PNG Gültig bis Ende Juli.png",
    ]:
        ref_path = ref_dir / ref_name
        if ref_path.exists():
            ref_img = Image.open(ref_path)
            buf = BytesIO()
            ref_img.save(buf, format="PNG")
            reference_images.append(types.Part.from_bytes(data=buf.getvalue(), mime_type="image/png"))
            print(f"  Referenzbild geladen: {ref_name}")
            break

    # Gebaeude-Foto als Referenz
    for bg_name in ["20211217_124809487_iOS.jpg", "hero-building.png"]:
        bg_path = ref_dir / bg_name
        if not bg_path.exists():
            bg_path = Path(__file__).parent.parent / bg_name
        if bg_path.exists():
            bg_img = Image.open(bg_path)
            buf = BytesIO()
            bg_img.save(buf, format="JPEG", quality=85)
            reference_images.append(types.Part.from_bytes(data=buf.getvalue(), mime_type="image/jpeg"))
            print(f"  Gebaeude-Foto geladen: {bg_name}")
            break

    # Content zusammenbauen: Referenzbilder + Prompt
    contents = reference_images + [prompt]

    # Versuch 1: Gemini 2.5 Flash Image (bestes Layout-Verstaendnis)
    try:
        print("  Versuche Gemini 2.5 Flash Image...")
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            )
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                img_data = part.inline_data.data
                return Image.open(BytesIO(img_data))
    except Exception as e:
        print(f"  Gemini 2.5 Flash Image fehlgeschlagen: {e}")

    # Versuch 3: Gemini 3 Pro Image
    try:
        print("  Versuche Gemini 3 Pro Image...")
        response = client.models.generate_content(
            model="gemini-3-pro-image",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            )
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                img_data = part.inline_data.data
                return Image.open(BytesIO(img_data))
    except Exception as e:
        print(f"  Gemini 3 Pro Image fehlgeschlagen: {e}")

    raise Exception("Keines der Modelle konnte ein Bild generieren.")


def update_aktionen_json(filename, titel, text, link, expires):
    """Fuegt den neuen Flyer zur aktionen.json hinzu."""
    json_path = OUTPUT_DIR / "aktionen.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            aktionen = json.load(f)
    else:
        aktionen = []

    if not any(a["bild"] == filename for a in aktionen):
        aktionen.append({
            "bild": filename,
            "titel": titel,
            "text": text,
            "link": link,
            "expires": expires
        })
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(aktionen, f, ensure_ascii=False, indent=2)
        print(f"OK aktionen.json aktualisiert (expires: {expires})")


def interaktiv_workshop():
    """Interaktive Eingabe fuer Workshop-Flyer."""
    print("\n" + "=" * 50)
    print("  GEMMA GOLFN - Workshop-Flyer via Gemini AI")
    print("=" * 50 + "\n")

    monat = input("Monat (z.B. August): ").strip()
    jahr = input("Jahr (z.B. 2026): ").strip()

    print(f"\nTermine fuer {monat} {jahr} eingeben.")
    print("Format: DATUM;THEMA;UHRZEIT")
    print("Beispiel: 05.08.2026;Langes Spiel;16:00 - 18:00 Uhr")
    print("Leere Zeile = fertig.\n")

    termine = []
    while True:
        zeile = input(f"Termin {len(termine) + 1}: ").strip()
        if not zeile:
            break
        teile = zeile.split(";")
        if len(teile) != 3:
            print("  ! Format: DATUM;THEMA;UHRZEIT - nochmal bitte.")
            continue
        termine.append({
            "datum": teile[0].strip(),
            "thema": teile[1].strip(),
            "zeit": teile[2].strip()
        })

    return {"typ": "workshop", "monat": monat, "jahr": jahr, "termine": termine}


def interaktiv_custom():
    """Interaktive Eingabe fuer individuelle Flyer."""
    print("\n" + "=" * 50)
    print("  GEMMA GOLFN - Kreativ-Flyer via Gemini AI")
    print("=" * 50 + "\n")

    return {
        "typ": "custom",
        "titel": input("Titel (z.B. Callaway Ballaktion): ").strip(),
        "beschreibung": input("Beschreibung (kurz, was soll drauf): ").strip(),
        "preis": input("Preis (z.B. ab EUR 140,-): ").strip(),
        "gueltig_bis": input("Gueltig bis (z.B. 31.07.2026): ").strip(),
        "cta": input("Call-to-Action (z.B. Jetzt sichern) [Enter=Jetzt buchen]: ").strip() or "Jetzt buchen",
        "link": input("Link fuer Homepage (z.B. mailto:office@...): ").strip() or "mailto:office@gemma-golfn.at",
    }


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # API Key pruefen
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "HIER_DEINEN_KEY_EINFUEGEN":
        print("FEHLER: Kein GEMINI_API_KEY in .env gefunden!")
        print("Bitte .env Datei im Werkzeuge-Ordner anlegen mit:")
        print("GEMINI_API_KEY=dein_key_hier")
        sys.exit(1)

    # Daten laden
    if len(sys.argv) > 1:
        json_path = Path(sys.argv[1])
        if not json_path.exists():
            print(f"Datei nicht gefunden: {json_path}")
            sys.exit(1)
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "termine" in data:
            data["typ"] = "workshop"
        else:
            data["typ"] = "custom"
        print(f"Daten geladen aus: {json_path}")
    else:
        print("\nWas moechtest du erstellen?")
        print("  1 = Workshop-Flyer (monatlich)")
        print("  2 = Kreativer Flyer (Aktion, Produkt, Event)")
        wahl = input("\nAuswahl (1/2): ").strip()
        if wahl == "2":
            data = interaktiv_custom()
        else:
            data = interaktiv_workshop()

    # Prompt bauen
    if data.get("typ") == "workshop":
        prompt = build_workshop_prompt(data)
        monat = data["monat"]
        jahr = data["jahr"]
        filename = f"Workshop {monat} {jahr} 1080_1080PNG Gueltig bis Ende {monat}.png"
        titel = f"Workshops {monat} {jahr}"
        text = "ab EUR 50,- - Kleine Gruppen, 2h intensives Training"
        link = "https://workshop.metzenhof.at/"
        monat_nr = MONAT_NR.get(monat, 1)
        letzter_tag = calendar.monthrange(int(jahr), monat_nr)[1]
        expires = f"{jahr}-{monat_nr:02d}-{letzter_tag}"
    else:
        prompt = build_custom_prompt(data)
        titel = data.get("titel", "Aktion")
        safe_titel = titel.replace(" ", "_").replace("/", "-")
        gueltig = data.get("gueltig_bis", "").replace(".", "")
        filename = f"{safe_titel}_1080_1080_Gueltig_bis_{gueltig}.png"
        text = data.get("beschreibung", "")[:80]
        link = data.get("link", "mailto:office@gemma-golfn.at")
        try:
            dt = datetime.strptime(data.get("gueltig_bis", ""), "%d.%m.%Y")
            expires = dt.strftime("%Y-%m-%d")
        except ValueError:
            expires = "2026-12-31"

    print(f"\n> Sende Prompt an Gemini AI...")
    print(f"  Typ: {data.get('typ', 'custom')}")
    print(f"  Titel: {titel}")
    print(f"  Dateiname: {filename}")

    # Bild generieren
    try:
        img = generate_image(prompt, api_key)

        # Auf 1080x1080 skalieren falls noetig
        if img.size != (1080, 1080):
            img = img.resize((1080, 1080), Image.LANCZOS)

        # Speichern
        output_path = OUTPUT_DIR / filename
        img.save(output_path, "PNG", quality=95)
        print(f"  OK Gespeichert: {output_path}")

        # aktionen.json aktualisieren
        update_aktionen_json(filename, titel, text, link, expires)

        print("\n" + "=" * 50)
        print("  FERTIG! Flyer wurde erstellt.")
        print(f"  Datei: {output_path}")
        print("  Homepage zeigt ihn automatisch an.")
        print("=" * 50)

    except Exception as e:
        print(f"\nFEHLER bei Bildgenerierung: {e}")
        print("\nDer generierte Prompt war:")
        print("-" * 40)
        print(prompt)
        print("-" * 40)
        print("\nDu kannst diesen Prompt manuell in Google AI Studio einfuegen")
        print("(aistudio.google.com) und das Bild dort generieren lassen.")
        sys.exit(1)


if __name__ == "__main__":
    main()
