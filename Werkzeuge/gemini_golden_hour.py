"""
Golden Hour via Gemini AI
=========================
Sendet das Original-Gebaeudefoto an Gemini mit Anweisung,
nur die Lichtstimmung zu aendern - Logos muessen erhalten bleiben.
"""

import os
import sys
from pathlib import Path
from io import BytesIO

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

from google import genai
from google.genai import types
from PIL import Image

SCRIPT_DIR = Path(__file__).parent
PROTOTYPE_DIR = SCRIPT_DIR.parent
INPUT_FILE = PROTOTYPE_DIR / "20211217_124809487_iOS.jpg"
OUTPUT_FILE = PROTOTYPE_DIR / "hero-building-golden-gemini.jpg"

PROMPT = """Edit this photo to look like it was taken during a dramatic golden hour sunset.

ONLY CHANGE the lighting and atmosphere:
- Replace the sky with dramatic orange/amber sunset clouds with a sun setting on the left side
- Apply warm golden light across the entire scene as if the sun is setting to the left
- The grass should have warm golden tones
- Add subtle lens flare or sun glow from the left
- The overall mood should be warm, cinematic, and premium

DO NOT CHANGE anything else:
- All logos and signs on the building MUST remain EXACTLY as they are, perfectly readable: "GEMMA GOLFN", "TOPTRACER RANGE", "METZENHOF", "PARC ARCHITEKTUR" - do NOT alter, blur, remove or modify any text/logos
- The building structure, windows, umbrellas, furniture - everything stays identical
- Do not add or remove any objects
- Do not change the perspective or crop

The result should look like a professional real estate/architecture photo shot during actual golden hour - natural and cinematic, not like an Instagram filter. Output the edited photo only."""


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("FEHLER: Kein GEMINI_API_KEY in .env gefunden!")
        sys.exit(1)

    if not INPUT_FILE.exists():
        print(f"FEHLER: {INPUT_FILE} nicht gefunden!")
        sys.exit(1)

    print(f"Lade Original: {INPUT_FILE.name}")
    img = Image.open(INPUT_FILE)
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=95)
    image_bytes = buf.getvalue()
    print(f"  Groesse: {img.size[0]}x{img.size[1]}")

    client = genai.Client(api_key=api_key)

    image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")

    models_to_try = [
        ("Gemini 3.1 Flash Image", "gemini-3.1-flash-image"),
        ("Gemini 3 Pro Image", "gemini-3-pro-image"),
        ("Gemini 2.5 Flash Image", "gemini-2.5-flash-image"),
    ]

    for label, model_name in models_to_try:
        try:
            print(f"\nSende an {label}...")
            response = client.models.generate_content(
                model=model_name,
                contents=[image_part, PROMPT],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                )
            )
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                    result = Image.open(BytesIO(part.inline_data.data))
                    result.save(OUTPUT_FILE, "JPEG", quality=95)
                    print(f"OK Gespeichert: {OUTPUT_FILE}")
                    print(f"  Groesse: {OUTPUT_FILE.stat().st_size // 1024} KB")
                    print(f"  Modell: {label}")
                    return
                if part.text:
                    print(f"  Gemini Text: {part.text[:200]}")
            print("  Kein Bild in der Antwort erhalten.")
        except Exception as e:
            print(f"  Fehler: {e}")

    print("\nKein Modell konnte das Bild bearbeiten.")
    print("Verwende den Prompt manuell in Google AI Studio oder ChatGPT.")


if __name__ == "__main__":
    main()
