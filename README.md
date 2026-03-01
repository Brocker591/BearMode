# BearMode

## Projekt starten

### Web-Anwendung (Browser)
Um die Anwendung im Browser zu starten:

1. Navigieren Sie in das Frontend-Verzeichnis:
   ```bash
   cd Frontend/bearmode
   ```
2. Starten Sie den Entwicklungsserver:
   ```bash
   npm start
   ```
3. Die Anwendung ist unter `http://localhost:4200` erreichbar.

### Desktop-Anwendung (Electron)
Um die Anwendung als Desktop-App (Electron) im Entwicklungsmodus zu starten:

1. Navigieren Sie in das Frontend-Verzeichnis:
   ```bash
   cd Frontend/bearmode
   ```
2. Führen Sie den Electron-Dev-Befehl aus:
   ```bash
   npm run electron:dev
   ```
   Dies startet sowohl den Angular-Server als auch das Electron-Fenster.

### Installation auf CachyOS (Arch Linux)

Da die Anwendung für Linux unter anderem als AppImage verpackt wird, können Sie diese unter CachyOS recht einfach selber bauen und ausführen.

1. **Voraussetzungen installieren:**
   Sollten Node.js und npm noch nicht auf Ihrem System installiert sein, installieren Sie diese über das Terminal:
   ```bash
   sudo pacman -S nodejs npm
   ```

2. **In das Frontend-Verzeichnis wechseln:**
   ```bash
   cd Frontend/bearmode
   ```

3. **Abhängigkeiten installieren:**
   ```bash
   npm install
   ```

4. **Electron-App bauen:**
   Dieser Befehl kompiliert die Angular-Anwendung und paketiert sie über den `electron-builder`. Dabei wird im Ordner `release` ein `.AppImage` erzeugt.
   ```bash
   npm run build:electron
   ```

5. **AppImage ausführbar machen und starten:**
   Navigieren Sie in den `release`-Ordner und geben Sie dem AppImage die nötigen Ausführungsrechte:
   ```bash
   cd release/
   chmod +x BearMode-*.AppImage
   ./BearMode-*.AppImage
   ```

*Zusatztipp für CachyOS:* Um die App bequem in Ihr Startmenü zu integrieren, können Sie Tools wie den [AppImageLauncher](https://github.com/TheAssassin/AppImageLauncher) verwenden oder eine entsprechende `.desktop`-Datei anlegen.
