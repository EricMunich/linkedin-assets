# linkedin-assets

Öffentliche Bildablage für Eric Knapes LinkedIn-Posts. Enthält ausschließlich Post-Bilder (PNG/PDF) und ihre HTML-Vorlagen. Kein Bezug zu anderen Projekten.

**Ablauf:** Eine HTML-Vorlage wird nach `posts/<JJJJ-MM-TT_thema>/` gelegt (`image.html` für Einzelbilder, `carousel.html` für Karussells). GitHub Actions rendert daraus automatisch `<slug>.png` bzw. `<slug>.pdf` plus `<slug>-cover.png` und legt sie im selben Ordner ab.

**Abrufadresse:** `https://raw.githubusercontent.com/EricMunich/linkedin-assets/main/posts/<slug>/<slug>.png`

Gestaltung, Texte und Freigabe laufen außerhalb dieses Repositories (Notion). Hier liegt nur, was für die Veröffentlichung abgeholt wird.
