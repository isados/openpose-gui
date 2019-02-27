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
def setStopMode(_=None):
    app.disableButton('Start')
    app.enableButton('Stop')
    app.enableButton('Exit')

def setStartMode(_=None):
    thread['openpose']='stopped'
    app.enableButton('Start')
    app.disableButton('Stop')
    app.enableButton('Exit')
    print("OpenPose stopped")

def exitFunction():
    res=app.yesNoBox("Confirm Exit", "Are you sure you want to exit?")
    if res:
        disableButtons(list_buttons)
        thread['cmd']='stop'
        daemon.kill()
        setStartMode()
        while(not (thread['predictor'] == 'stopped' and \
                    thread['openpose'] == 'stopped')):
            pass

    return res

def doSomething(_=None):
    # Prediction algorithm, and pass the app object for writing labels
    return prediction(app)


def press(btn):
    if btn=='Start':
        #Start a thread, and disable GUI elements
        disableButtons(list_buttons)

        thread["predictor"]='running'
        thread['openpose']='running'
        thread['cmd']=''

        setStopMode()

        #Start OpenPose script
        app.thread(daemon.start)

        # Start Prediction
        app.thread(doSomething)

    elif btn=='Stop':
        disableButtons(list_buttons)

        #Stop OpenPose script
        app.threadCallback(daemon.kill,setStartMode)

        # Stops prediction
        thread["cmd"]='stop'
    elif btn=='Exit':
            app.stop()

# create a GUI variable called app
app = gui("GUI Interface", "400x300")
app.setBg("lightblue")
app.setFont(18)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Aqua Shield (Beta Edition v0.1)",0,0,3)
app.setLabelBg("title", "black")
app.setLabelFg("title", "lightblue")

# link the buttons to the function called

app.addButtons(list_buttons,press,1,0,3)
app.disableButton('Stop')

app.addMessage('target', """Welcome to the AquaShield - OpenPose Interface

Push the START button to begin...""")
app.setMessageBg('target','white')
app.setMessageAspect('target', 150)

# Remove .pid files that linger
[os.unlink(path) for path in glob.glob("*.pid")]

app.stopFunction=exitFunction

# start the GUI
app.go()
