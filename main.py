# import the library
import os
import glob

from appJar import gui

from prediction import *
from pythondaemon.mydaemon import *

list_buttons=['Start','Stop','Exit']

# Define the Daemon
daemon=MyDaemon("mydaemon.pid")

def disableButtons(btns):
    for btn in btns: app.disableButton(btn)

# Control what elements are enabled
def setStopMode():
    app.disableButton('Start')
    app.enableButton('Stop')
    app.enableButton('Exit')

def setStartMode():
    app.enableButton('Start')
    app.disableButton('Stop')
    app.enableButton('Exit')
#
# def enableButtons(btns):
#     for btn in btns: app.enableButton(btn)
def stopFunction():
    res=app.yesNoBox("Confirm Exit", "Are you sure you want to exit?")
    if res:
        disableButtons(list_buttons)
        thread['cmd']='stop'
        daemon.kill()
        while(thread['status'] is not 'stopped'):
            continue
    return res

def doSomething(_=None):
    # Prediction algorithm, and pass the app object for writing labels
    return prediction(7,app,"purple")

def stopSomething(_=None):
    delete_all_images()
    app.setLabel("target","")
    app.setLabelBg("target","purple")
    thread["cmd"]=''
    thread["status"]='stopped'

def btn_functions(btn):
    if btn=='Start':
        #Start a thread, and disable GUI elements
        setStopMode()

        #Start OpenPose script
        app.thread(daemon.start)

        # Start Prediction
        thread["status"]='running'
        thread['cmd']=''
        app.threadCallback(doSomething,stopSomething)
    elif btn=='Stop':
        setStartMode()

        #Stop OpenPose script
        app.thread(daemon.kill)

        # Stops prediction
        thread["cmd"]='stop'
    elif btn=='Exit':
            app.stop()

# create a GUI variable called app
app = gui("OpenPose Interface", "400x200")
app.setBg("orange")
app.setFont(18)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Welcome to appJar")
app.setLabelBg("title", "blue")
app.setLabelFg("title", "orange")

# link the buttons to the function called

app.addButtons(list_buttons,btn_functions)
app.disableButton('Stop')

app.addLabel("target", "")
app.setLabelBg("target", "purple")
[os.unlink(path) for path in glob.glob("*.pid")]

app.stopFunction=stopFunction

# start the GUI
app.go()
