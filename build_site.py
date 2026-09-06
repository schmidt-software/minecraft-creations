#!/usr/bin/env python3
"""
Regenerates index.html for the public skin gallery.

HOW TO ADD A NEW SKIN:
  1. Drop the 64x64 skin PNG into ../skins/ (the folder next to this website/).
  2. (Optional) Add a title/description for it in the CONTENT dict below,
     keyed by the exact filename. If you skip this, a reasonable title is
     guessed from the filename automatically.
  3. Run:  ./venv/bin/python build_site.py
  4. Open index.html to check it, then deploy the whole website/ folder
     (see README.md for hosting options).

That's the entire update workflow - no server, no database, no CMS.
"""
import shutil
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
SKINS_SRC = HERE.parent / "skins"
SKINS_OUT = HERE / "assets" / "skins"
THUMBS_OUT = HERE / "assets" / "thumbnails"

SKINS_OUT.mkdir(parents=True, exist_ok=True)
THUMBS_OUT.mkdir(parents=True, exist_ok=True)

# Optional hand-written title/description per filename. Anything not
# listed here still gets a page (title guessed from the filename).
CONTENT = {
    "michael_jackson_skin.png": {
        "title": "Michael Jackson",
        "description": "Schwarzer Anzug mit rotem Akzent, weißer Handschuh, Fedora.",
    },
    "captain_picard_skin.png": {
        "title": "Captain Picard",
        "description": "Star Trek TNG - rote Kommandouniform, goldenes Communicator-Abzeichen.",
    },
    "superman_skin.png": {
        "title": "Superman",
        "description": "Blauer Anzug, Brustschild, roter Umhang (nur von hinten sichtbar).",
    },
    "trump_skin.png": {
        "title": "Donald Trump",
        "description": "Stilisierte Karikatur - Anzug, lange rote Krawatte, markante Frisur.",
    },
    "spock_skin.png": {
        "title": "Mr. Spock",
        "description": "Star Trek TOS - blaue Wissenschaftsuniform, Bowl-Cut, angedeutete Spitzohren.",
    },
    "data_skin.png": {
        "title": "Lieutenant Commander Data",
        "description": "Star Trek TNG - goldene Operations-Uniform, blass-goldene Haut, gelbe Augen.",
    },
    "geordi_la_forge_skin.png": {
        "title": "Geordi La Forge",
        "description": "Star Trek TNG - goldene Uniform mit dem markanten VISOR über den Augen.",
    },
}


def guess_title(stem: str) -> str:
    words = stem.replace("_skin", "").replace("_", " ").split()
    return " ".join(w.capitalize() for w in words)


def render_front_view(skin_path: Path) -> Image.Image:
    """Composite a simple standing front-view from the flat skin texture."""
    img = Image.open(skin_path).convert("RGBA")

    def crop(box):
        return img.crop(box)

    def paste_over(base, overlay, x, y):
        base.paste(overlay, (x, y), overlay)

    canvas = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
    paste_over(canvas, crop((8, 8, 16, 16)), 4, 0)     # head
    paste_over(canvas, crop((40, 8, 48, 16)), 4, 0)    # hat overlay (if any)
    paste_over(canvas, crop((20, 20, 28, 32)), 4, 8)   # torso
    paste_over(canvas, crop((44, 20, 48, 32)), 0, 8)   # right arm
    paste_over(canvas, crop((36, 52, 40, 64)), 12, 8)  # left arm
    paste_over(canvas, crop((4, 20, 8, 32)), 4, 20)    # right leg
    paste_over(canvas, crop((20, 52, 24, 64)), 8, 20)  # left leg
    return canvas.resize((16 * 20, 32 * 20), Image.NEAREST)


def build():
    skin_files = sorted(SKINS_SRC.glob("*.png"))
    if not skin_files:
        print(f"No PNG files found in {SKINS_SRC}")
        return

    cards = []
    for skin_path in skin_files:
        name = skin_path.name
        shutil.copyfile(skin_path, SKINS_OUT / name)

        thumb = render_front_view(skin_path)
        thumb_name = skin_path.stem + ".png"
        bg = Image.new("RGBA", thumb.size, (245, 245, 245, 255))
        bg.paste(thumb, (0, 0), thumb)
        bg.save(THUMBS_OUT / thumb_name)

        meta = CONTENT.get(name, {})
        title = meta.get("title", guess_title(skin_path.stem))
        description = meta.get("description", "")

        cards.append(
            f"""
      <article class="card">
        <img src="assets/thumbnails/{thumb_name}" alt="{title}" loading="lazy">
        <h2>{title}</h2>
        <p>{description}</p>
        <a class="download" href="assets/skins/{name}" download>Skin herunterladen (.png)</a>
      </article>"""
        )

    html = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Minecraft Skin Galerie</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <h1>Minecraft Skin Galerie</h1>
    <p>Eine Sammlung selbstgemachter 64x64 Minecraft-Skins. PNG herunterladen und
       im eigenen Client hochladen, oder per <a href="https://github.com/AlexProgrammerDE/SkinsRestorer" target="_blank" rel="noopener">SkinsRestorer</a>
       serverseitig zuweisen.</p>
  </header>
  <main class="grid">
    {''.join(cards)}
  </main>
  <footer>
    <p>Generiert mit build_site.py &middot; {len(cards)} Skins</p>
  </footer>
</body>
</html>
"""
    (HERE / "index.html").write_text(html, encoding="utf-8")
    print(f"Built index.html with {len(cards)} skin(s).")


if __name__ == "__main__":
    build()
