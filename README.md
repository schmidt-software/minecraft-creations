# Minecraft Creations Galerie

Statische Webseite (reines HTML/CSS, keine Datenbank, kein Server-Code
nötig), die alle Skins aus `../skins/` als Karten mit Vorschaubild und
Download-Link anzeigt.

**Live:** https://schmidt-software.github.io/minecraft-creations/
**Repo:** https://github.com/schmidt-software/minecraft-creations

## Inhalt aktualisieren

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
5. Live veröffentlichen:
   ```
   git add -A
   git commit -m "Update gallery"
   git push
   ```
   GitHub Pages baut danach automatisch neu (dauert meist ~1 Minute).

Kein manuelles HTML-Schreiben nötig - jede Änderung läuft über
`build_site.py` + `git push`.

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

## Hosting

Bereits eingerichtet: GitHub Pages, Quelle = `main`-Branch, Repo-Root.
Jeder `git push` auf `main` löst automatisch einen neuen Build aus.

Da die Seite rein statisch ist, ließe sie sich genauso gut auf Netlify
oder Cloudflare Pages hosten, falls das mal gewechselt werden soll -
einfach den `website/`-Ordner (ohne `venv/`) dorthin verbinden.
