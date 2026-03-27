# BearMode: Installation und Update Anleitung

Diese Anleitung beschreibt, wie du deine Angular Electron App (`BearMode`) auf deinem System installierst, aktualisierst und konfigurierst. 

## Inhaltsverzeichnis
1. [Konfiguration der Backend-URL](#konfiguration-der-backend-url)
2. [Anleitung für CachyOS (Linux)](#anleitung-für-cachyos-linux)
3. [Anleitung für Windows](#anleitung-für-windows)

---

## Konfiguration der Backend-URL

Bevor du die App baust, solltest du sicherstellen, dass die Applikation weiß, wo das Backend läuft (z.B. `localhost:55555`).

1. **Frontend (Angular):** Öffne die Datei `Frontend/bearmode/src/environments/environment.prod.ts` (und falls vorhanden `environment.ts`) und vergewissere dich, dass die URL für deine API hier richtig eingetragen ist:
   ```typescript
   export const environment = {
     production: true,
     apiUrl: 'http://localhost:55555' // Hier die Backend-URL anpassen
   };
   ```
2. **Backend / Docker:** Stelle sicher, dass die Ports für dein Backend in der `docker-compose.yml` und/oder der `Backend/.env` Datei korrekt auf `55555` gemappt sind, damit das Frontend das Backend dort auch erreichen kann.

---

## Anleitung für CachyOS (Linux)

### 1. Installation und Erstellen der ausführbaren Datei

1. **Abhängigkeiten:** Stelle sicher, dass Node.js/npm sowie Docker und Docker-Compose installiert sind.
2. **Backend starten:**
   Gehe in dein Hauptverzeichnis (`BearMode`) und starte die Docker-Container:
   ```bash
   docker-compose up -d
   ```
3. **Frontend bauen:**
   Wechsle in den Frontend-Ordner, installiere die Packages und baue die Electron-App:
   ```bash
   cd Frontend/bearmode
   npm install
   npm run build
   //npm run electron:build -- --linux
   npm run build:electron --linux 
   ```
   *(Tipp: Der genaue Build-Befehl hängt von deiner `package.json` ab. Manchmal reicht auch nur `npm run electron:build` oder `npm run make`.)*
   
   Nach dem Build-Prozess findest du (je nach Konfiguration) ein `.AppImage` oder ein entpacktes Verzeichnis mit dem Executable im Unterordner `dist/` oder `release/`.

### 2. Anwendungsstarter & Icon erstellen

Damit du das Programm direkt über dein Suchmenü (KDE/GNOME) in CachyOS starten kannst, legen wir eine `.desktop` Datei an.

1. **App ablegen:** Verschiebe die fertige ausführbare Datei (wie das AppImage) sowie ein Icon (`.png` oder `.svg`) in ein persistentes Verzeichnis, z.B. `~/Apps/BearMode/`.
2. **Desktop-Datei anlegen:**
   Erstelle eine Datei für den Application-Launcher:
   ```bash
   nano ~/.local/share/applications/bearmode.desktop
   ```
3. **Inhalt der `.desktop` Datei:** Füge Folgendes ein und passe die Dateipfade bei `Exec` und `Icon` exakt auf deine Struktur an:
   ```ini
   [Desktop Entry]
   Name=BearMode
   Comment=Meine BearMode Angular Electron App
   Exec=/home/DEIN_BENUTZERNAME/Apps/BearMode/BearMode.AppImage
   Icon=/home/DEIN_BENUTZERNAME/Apps/BearMode/icon.png
   Terminal=false
   Type=Application
   Categories=Utility;Application;
   ```
4. **Speichern und Anwenden:** Speichere die Datei. CachyOS sollte den neuen Eintrag im Anwendungsstarter innerhalb weniger Sekunden erkennen. Falls nicht, kannst du die Liste manuell aktualisieren mit:
   ```bash
   update-desktop-database ~/.local/share/applications/
   ```

### 3. Update durchführen (CachyOS)

Falls du das Programm erweiterst und updaten möchtest:
1. Navigiere in dein Projektverzeichnis und lade die aktuellen Änderungen (z.B. per `git pull`).
2. Passe bei Bedarf die Backend-URL an (wie oben beschrieben).
3. Wechsle in `Frontend/bearmode/` und erstelle den Linux-Build neu:
   ```bash
   npm run electron:build -- --linux
   ```
4. Ersetze die alte `.AppImage`-Datei in deinem `~/Apps/BearMode/` Ordner durch die neu gebaute Datei (Behalte einfach den gleichen Dateinamen, dann funktioniert dein Icon im Launcher weiterhin ohne Anpassung).
5. (Optional) Falls sich das Backend verändert hat, lade die Container neu:
   ```bash
   docker-compose up -d --build
   ```

---

## Anleitung für Windows

### 1. Installation

1. **Voraussetzungen:** Du benötigst Node.js, npm und Docker Desktop für Windows.
2. **Backend starten:**
   Öffne z.B. die PowerShell im Hauptverzeichnis `BearMode` und starte das Backend:
   ```cmd
   docker-compose up -d
   ```
3. **Frontend bauen:**
   Wechsle in den Frontend-Ordner, installiere die Dependencies und baue den Windows-Installer (eine `.exe` Datei):
   ```cmd
   cd Frontend\bearmode
   npm install
   npm run build
   npm run electron:build -- --win
   ```
4. **App installieren:**
   Führe die daraus resultierende `.exe`-Datei (meist im Ordner `dist` oder `release`) aus. Die Electron-Installation wird standardmäßig automatisch ein Icon auf deinem Desktop und im Windows-Startmenü anlegen, über das du das Programm direkt mit einem Klick aufrufen kannst.

### 2. Update durchführen (Windows)

1. **Schließen:** Beende die aktuell laufende BearMode Anwendung.
2. **Code aktualisieren:** Ziehe dir die neuen Erweiterungen und Änderungen aus deinem Repository.
3. **Backend-URL prüfen:** Passe falls nötig die Adresse in `environment.prod.ts` wieder an.
4. **App neu bauen:** Führe den Build-Befehl für Windows im Frontend-Ordner erneut aus (`npm run electron:build -- --win`).
5. **Drüber installieren:** Führe den neu erstellten Installer (`.exe`) einfach wieder aus. Das Programmdateien unter Windows werden idR. sauber überschrieben und das Programm ist auf dem neuesten Stand.
6. (Optional) Aktualisiere bei Backend-Änderungen deine Docker Container aus dem Hauptverzeichnis via `docker-compose up -d --build`.
