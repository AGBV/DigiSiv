import glob
import os
from pathlib import Path

import numpy as np
import rasterio
import scipy.io
from rasterio.enums import Resampling
from rasterio.windows import Window, bounds

# --- KONFIGURATION ---

# 1. Pfad zum Sentinel-2 Ordner (.SAFE Verzeichnis oder der Ordner mit den jp2 Dateien)
# Beispiel: 'S2A_MSIL2A_20230701T0900...'
# INPUT_DIR = "./S2_Daten/GRANULE/L2A_T33SVA.../IMG_DATA/R10m/"
INPUT_DIR = (
    Path.home()
    / "Downloads/S2A_MSIL2A_20250316T094121_N0511_R036_T33SWC_20250316T134912.SAFE/GRANULE/L2A_T33SWC_A050827_20250316T094116/IMG_DATA/R20m"
)
# HINWEIS: Bei L2A (Atmosphären-korrigiert) liegen 10m und 20m oft in getrennten Ordnern (R10m, R20m).
# Man muss die Pfade ggf. sammeln. Siehe unten im Skript für eine smarte Suche.

OUTPUT_FILE = "milazzo_subset.mat"

# 2. PIXEL-KOORDINATEN (Basierend auf 10m Auflösung!)
# Format: (x_offset, y_offset, breite, hoehe)
# x_offset: Wie viele Pixel von links?
# y_offset: Wie viele Pixel von oben?
# breite/hoehe: Größe des Ausschnitts in Pixeln
CROP_PIXELS = (900, 3200, 300, 300)

# Bänder Konfiguration (Bleibt gleich)
BANDS_CONFIG = {
    "B02": {"name": "Blue"},  # 10m
    "B03": {"name": "Green"},  # 10m
    "B04": {"name": "Red"},  # 10m (Referenz)
    "B08": {"name": "NIR"},  # 10m
    "B05": {"name": "RedEdge1"},  # 20m
    "B06": {"name": "RedEdge2"},  # 20m
    "B11": {"name": "SWIR1"},  # 20m
    "B12": {"name": "SWIR2"},  # 20m
}


def find_band_path(base_dir, band_id):
    """Sucht Pfad zur .jp2 Datei."""
    search_pattern = f"**/*{band_id}*.jp2"
    files = glob.glob(os.path.join(base_dir, search_pattern), recursive=True)
    print(base_dir, band_id, files)
    for f in files:
        if "preview" in f:
            continue
        return f
    return None


def crop_by_pixels(bands_config, pixel_window_tuple, base_dir):
    """
    Schneidet Bänder basierend auf Pixel-Koordinaten des 10m Bandes aus.
    """
    col_off, row_off, width, height = pixel_window_tuple

    # 1. Referenz-Band (10m) öffnen, um die Geodaten des Fensters zu holen
    ref_band = "B04"
    ref_path = find_band_path(base_dir, ref_band)
    if not ref_path:
        print(ref_path)
        raise FileNotFoundError(f"Referenz {ref_band} nicht gefunden.")

    with rasterio.open(ref_path) as src:
        # Erstelle das Rasterio Window Objekt
        ref_window = Window(col_off, row_off, width, height)

        # WICHTIG: Wir berechnen die geografischen Grenzen dieses Pixel-Fensters.
        # Das brauchen wir, um die 20m Bänder korrekt zu finden.
        win_bounds = bounds(ref_window, src.transform)

        print(f"Pixel-Ausschnitt entspricht UTM Koordinaten: {win_bounds}")
        print(f"Ziel-Größe: {width} x {height} Pixel")

    # 2. Daten laden
    stacked_data = []
    band_names = []
    wls_list = []

    # Wellenlängen Mapping (ca. nm)
    wls_map = {
        "B02": 490,
        "B03": 560,
        "B04": 665,
        "B05": 705,
        "B06": 740,
        "B08": 842,
        "B11": 1610,
        "B12": 2190,
    }

    for band_id, info in bands_config.items():
        path = find_band_path(base_dir, band_id)
        if not path:
            continue

        print(f"Lade {band_id}...")

        with rasterio.open(path) as src:
            # Trick: Wir nutzen die geografischen Bounds (win_bounds), die wir oben
            # aus den Pixeln berechnet haben. Rasterio rechnet das für das aktuelle
            # Band (z.B. 20m) automatisch wieder in die dortigen Pixel um.

            # window berechnen basierend auf bounds
            win = rasterio.windows.from_bounds(*win_bounds, transform=src.transform)

            # Lesen und Resampling auf die Zielgröße (width/height vom 10m Band)
            data = src.read(
                1,
                window=win,
                out_shape=(height, width),  # Erzwingt 10m Raster auch für 20m Bänder
                resampling=Resampling.bilinear,
            )

            # Normierung auf 0..1
            data = data.astype(np.float32) / 10000.0

            stacked_data.append(data)
            band_names.append(info["name"])
            wls_list.append(wls_map.get(band_id, 0))

    # Stack (Height, Width, Bands)
    return np.stack(stacked_data, axis=-1), band_names, wls_list


# --- MAIN ---
if __name__ == "__main__":
    # Hier deinen Pfad anpassen
    # SAFE_PATH = "S2A_MSIL2A_2023....SAFE"
    SAFE_PATH = INPUT_DIR

    try:
        cube, names, wls = crop_by_pixels(BANDS_CONFIG, CROP_PIXELS, SAFE_PATH)

        scipy.io.savemat(
            OUTPUT_FILE, {"Mixture": cube, "BandNames": names, "Lambda": wls}
        )
        print(f"Erfolg! {OUTPUT_FILE} gespeichert. Shape: {cube.shape}")

    except Exception as e:
        print(f"Fehler: {e}")
