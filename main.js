const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  mainWindow.loadFile('index.html');
   
  pythonProcess = spawn('python', ['./backend/app.py']);
  pythonProcess.stdout.on('data', (data) => {
    console.log(`Flask server output: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Flask server error: ${data}`);
  });

  mainWindow.on('closed', function () {
    if (pythonProcess) {
      pythonProcess.kill('SIGINT');
    }
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', function () {
  if (mainWindow === null) createWindow();
});
