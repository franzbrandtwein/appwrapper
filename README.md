# AppWrapper

Eine konfigurierbare Android-App, die eine PWA (Progressive Web App) als native App verpackt.  
Gebaut mit **Python 3** und **PySide6 / Qt**.

## Aktuell konfiguriert für

**[essen.new-ages.de](https://essen.new-ages.de/)**

## Funktionsweise

Die App öffnet eine WebView, die die in `config.json` definierte URL lädt – vollständig konfigurierbar ohne Code-Änderungen.

## Konfiguration (`config.json`)

```json
{
  "app_name": "Essen New Ages",
  "package_name": "de.newages.essen",
  "version": "1.0.0",
  "url": "https://essen.new-ages.de/",
  "orientation": "portrait",
  "status_bar_color": "#1a1a2e",
  "fullscreen": false,
  "allow_navigation": true,
  "user_agent_suffix": "AppWrapper/1.0"
}
```

| Feld | Beschreibung |
|------|-------------|
| `app_name` | App-Name (Titel & Android-Label) |
| `package_name` | Android-Package-ID (z.B. `com.example.app`) |
| `version` | App-Version |
| `url` | URL der PWA |
| `orientation` | `portrait` oder `landscape` |
| `status_bar_color` | Farbe der Statusleiste (Hex) |
| `fullscreen` | Vollbild-Modus |
| `allow_navigation` | Navigation zu externen Seiten erlauben |
| `user_agent_suffix` | Wird an den User-Agent angehängt |

## Lokal ausführen (Desktop)

```bash
pip install PySide6
python main.py
```

## Android APK bauen

### Voraussetzungen

- Python 3.10+
- Android SDK + NDK (26.x)
- Qt 6.7 für Android (`android_arm64_v8a`)
- PySide6 6.7

### Build

```bash
pip install "PySide6>=6.7"

pyside6-android-deploy \
  --name "Essen New Ages" \
  --arch arm64-v8a \
  main.py
```

### Via GitHub Actions

Beim Push auf `main` oder beim Erstellen eines Tags (`v*`) wird automatisch eine APK gebaut.  
Die fertige APK ist als Artefakt im entsprechenden Workflow-Run verfügbar.

**Release erstellen:**
```bash
git tag v1.0.0
git push origin v1.0.0
```

## Projektstruktur

```
appwrapper/
├── main.py              # Python-Einstiegspunkt
├── main.qml             # QML-UI mit WebView
├── config.json          # App-Konfiguration
├── pyproject.toml       # Projekt-Metadaten & Build-Konfiguration
└── .github/
    └── workflows/
        └── build-android.yml   # GitHub Actions CI/CD
```

## Neue PWA konfigurieren

Nur `config.json` anpassen:

```json
{
  "app_name": "Meine App",
  "package_name": "com.example.meineapp",
  "url": "https://meine-pwa.de/"
}
```

Dann committen, pushen – GitHub Actions baut automatisch eine neue APK.
