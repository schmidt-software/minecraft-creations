# Minecraft Skin Galerie

Statische Webseite (reines HTML/CSS, keine Datenbank, kein Server-Code
nötig), die alle Skins aus `../skins/` als Karten mit Vorschaubild und
Download-Link anzeigt.

## Inhalt aktualisieren (der einzige Schritt)

1. Neue 64x64-Skin-PNG in `../skins/` ablegen (der Ordner eine Ebene
   über diesem hier).
2. Optional: in `build_site.py` im `CONTENT`-Dict einen Titel/eine
   Beschreibung für den exakten Dateinamen hinzufügen. Ohne Eintrag
   wird automatisch ein Titel aus dem Dateinamen erzeugt.
3. Ausführen:
   ```
   ./venv/bin/python build_site.py
   ```
   Das kopiert die PNGs nach `assets/skins/`, erzeugt Vorschaubilder in
   `assets/thumbnails/` und schreibt `index.html` komplett neu.
4. `index.html` lokal im Browser öffnen (Doppelklick) zum Prüfen.

Kein manuelles HTML-Schreiben nötig - jede Änderung läuft über
`build_site.py`.

## Erstmaliges Setup (nur einmal nötig)

```
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

## Lokale Vorschau

```
python3 -m http.server 8000
```
und dann `http://localhost:8000` öffnen.

## Veröffentlichen (Hosting-Optionen, alle kostenlos)

Diese Seite ist rein statisch - der ganze `website/`-Ordner (inklusive
`assets/`, `index.html`, `style.css`, aber ohne `venv/`) kann direkt auf
jeden statischen Hoster kopiert werden:

- **GitHub Pages**: Ordner in ein GitHub-Repo pushen, in den
  Repo-Einstellungen unter "Pages" den Branch/Ordner auswählen. Update
  = `git push`.
- **Netlify Drop**: den Ordner per Drag & Drop auf https://app.netlify.com/drop
  ziehen - sofort live, kein Account zwingend nötig für die erste Version.
- **Cloudflare Pages**: ähnlich wie GitHub Pages, verbindet sich direkt
  mit einem Git-Repo.

Am wartungsärmsten ist GitHub Pages, wenn du ohnehin ein GitHub-Konto
hast: einmal einrichten, danach reicht `git add`, `git commit`,
`git push` nach jedem `build_site.py`-Lauf.
