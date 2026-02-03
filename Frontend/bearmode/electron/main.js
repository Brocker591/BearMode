const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');

const indexPath = path.join(__dirname, '../dist/bearmode/browser/index.html');
const useDevServer =
  process.env.NODE_ENV === 'development' ||
  (process.argv || []).includes('--dev') ||
  !fs.existsSync(indexPath);

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    },
    autoHideMenuBar: true, // <-- Menü automatisch ausblenden
  });

  if (useDevServer) {
    mainWindow.loadURL('http://localhost:4200');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(indexPath);
  }

  mainWindow.on('closed', () => {
    app.quit();
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
