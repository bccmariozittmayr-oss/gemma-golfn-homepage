"""
Golden Hour Color Grading fuer Gemma Golfn Hero-Bild v4
========================================================
Warme Amber/Orange-Toene + Sonne links im Himmel.
Logos und Details bleiben 1:1 erhalten.
"""

from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
from pathlib import Path
import numpy as np
import sys

SCRIPT_DIR = Path(__file__).parent
PROTOTYPE_DIR = SCRIPT_DIR.parent

INPUT_FILE = PROTOTYPE_DIR / "20211217_124809487_iOS.jpg"
OUTPUT_FILE = PROTOTYPE_DIR / "hero-building-golden.jpg"


def create_sun_glow(width, height, sun_x, sun_y, radius=180):
    """Erzeugt einen realistischen Sonnen-Glow als Overlay."""
    glow = np.zeros((height, width, 3), dtype=np.float32)
    yy, xx = np.mgrid[0:height, 0:width]
    dist = np.sqrt((xx - sun_x)**2 + (yy - sun_y)**2)

    # Kern: heller weiss-gelber Punkt
    core = np.clip(1.0 - dist / (radius * 0.3), 0, 1) ** 2
    glow[:,:,0] += core * 255  # R
    glow[:,:,1] += core * 230  # G
    glow[:,:,2] += core * 180  # B

    # Mittlerer Ring: warmes Orange
    mid = np.clip(1.0 - dist / (radius * 0.8), 0, 1) ** 1.5
    glow[:,:,0] += mid * 160
    glow[:,:,1] += mid * 90
    glow[:,:,2] += mid * 30

    # Aeusserer Halo: sanftes Amber
    outer = np.clip(1.0 - dist / (radius * 2.0), 0, 1) ** 1.2
    glow[:,:,0] += outer * 80
    glow[:,:,1] += outer * 45
    glow[:,:,2] += outer * 10

    return np.clip(glow, 0, 255)


def apply_golden_hour(img):
    img = img.convert("RGB")
    arr = np.array(img, dtype=np.float32)
    height, width = arr.shape[:2]

    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

    # Vertikaler Gradient
    y_grad = np.linspace(0, 1, height).reshape(-1, 1)
    sky = np.clip(1.0 - y_grad * 3.0, 0, 1)
    ground = np.clip(y_grad * 2.0 - 0.8, 0, 1)

    # --- Globale Waerme ---
    r_out = r * 1.08 + 12
    g_out = g * 0.98
    b_out = b * 0.70 - 10

    # --- Himmel: Orange/Amber ---
    r_out += sky * 45
    g_out += sky * 15
    b_out -= sky * 25

    # --- Boden: warm-golden ---
    r_out += ground * 18
    g_out += ground * 5

    # --- Horizontale Lichtquelle links ---
    x_grad = np.linspace(1, 0, width).reshape(1, -1)
    sun_side = np.clip(x_grad * 1.5 - 0.3, 0, 1) * sky
    r_out += sun_side * 30
    g_out += sun_side * 10

    arr[:,:,0] = np.clip(r_out, 0, 255)
    arr[:,:,1] = np.clip(g_out, 0, 255)
    arr[:,:,2] = np.clip(b_out, 0, 255)

    # --- Sonne einfuegen (links oben, wie im ChatGPT-Bild) ---
    sun_x = int(width * 0.08)
    sun_y = int(height * 0.28)
    sun_glow = create_sun_glow(width, height, sun_x, sun_y, radius=200)

    # Additiv blenden (Screen-Modus: heller wird heller, dunkles bleibt)
    arr = arr + sun_glow * 0.7
    arr = np.clip(arr, 0, 255)

    img = Image.fromarray(arr.astype(np.uint8))

    # Kontrast + Saettigung
    img = ImageEnhance.Contrast(img).enhance(1.18)
    img = ImageEnhance.Color(img).enhance(1.15)

    # Vignette
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w // 2, h // 2
    max_dist = (cx**2 + cy**2) ** 0.5
    dist = np.sqrt((xx - cx)**2 + (yy - cy)**2) / max_dist
    mask_arr = np.clip((dist - 0.55) * 200, 0, 85).astype(np.uint8)
    vignette = Image.new("RGB", img.size, (0, 0, 0))
    mask = Image.fromarray(mask_arr)
    img = Image.composite(vignette, img, mask)

    # Sanfter Glow (simuliert Streulicht)
    glow = img.filter(ImageFilter.GaussianBlur(radius=25))
    img = Image.blend(img, glow, alpha=0.1)

    # Helligkeit
    img = ImageEnhance.Brightness(img).enhance(0.94)

    return img


def main():
    if not INPUT_FILE.exists():
        print(f"FEHLER: Eingabedatei nicht gefunden: {INPUT_FILE}")
        sys.exit(1)

    print(f"Lade Original: {INPUT_FILE.name}")
    img = Image.open(INPUT_FILE)
    print(f"  Groesse: {img.size[0]}x{img.size[1]}")

    print("Wende Golden Hour v4 an (Amber + Sonne)...")
    result = apply_golden_hour(img)

    result.save(OUTPUT_FILE, "JPEG", quality=95)
    print(f"Gespeichert: {OUTPUT_FILE}")
    print(f"  Groesse: {OUTPUT_FILE.stat().st_size // 1024} KB")
    print("Fertig.")


if __name__ == "__main__":
    main()
