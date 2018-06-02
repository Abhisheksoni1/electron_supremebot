const electron = require('electron')
const { spawn } = require('child_process');
var kill = require('tree-kill');
var hostile = require('hostile');
var server;
var worker;
var harvester;

// Module to control application life.
const app = electron.app
// Module to create native browser window.
const BrowserWindow = electron.BrowserWindow

const path = require('path')
const url = require('url')
var fs = require('fs');

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow

function createWindow () {

  if (fs.existsSync(path.join(app.getAppPath(), 'server')))
  src_path = path.join(app.getAppPath(), 'server');
  else
  src_path = path.join(app.getAppPath(), '..', 'server');
  
  server = spawn(path.join(src_path,'winvenv/Scripts/python.exe'),[path.join(src_path,'manage.py'),'runserver'],{'detached':true,shell:true});
  worker = spawn(path.join(src_path,'winvenv/Scripts/python.exe'),[path.join(src_path,'manage.py'),'manage_worker'],{'detached':true,shell:true});
  harvester = spawn(path.join(src_path,'winvenv/Scripts/python.exe'),[path.join(src_path,'manage.py'),'start_harvester'],{'detached':true,shell:true});
  hostile.set('127.0.0.1', 'cartchefs.supremenewyork.com', function (err) {
    if (err) {
      console.error(err)
    } else {
      console.log('set /etc/hosts successfully!')
    }
  })
  console.log("system started")


  // Create the browser window.
//  mainWindow = new BrowserWindow({width: 800, height: 600})
 mainWindow = new BrowserWindow({fullscreen:true, webPreferences: {
    nodeIntegration: false }})
  // and load the index.html of the app.
  mainWindow.loadURL(
    "http://127.0.0.1:8000/"
    // url.format({
    // pathname: path.join(__dirname, 'index.html'),
    // protocol: 'file:',
    // slashes: true
  // })
)

  // Open the DevTools.
//   mainWindow.webContents.openDevTools()

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)


app.on('activate', function () {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) {
    createWindow()
  }
})

app.on('quit', () => {
   kill(server.pid, 'SIGKILL');
   kill(worker.pid, 'SIGKILL');
   kill(harvester.pid, 'SIGKILL');
  });

app.on('window-all-closed', () => {
  app.quit();
});
// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
