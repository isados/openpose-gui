import time

thread={'predictor':'stopped','openpose':'stopped','cmd':''} # Global flag

switch_colors=['blue','red']
labels=['left arm up','right arm up']
def prediction(sec,app,orig_color):
    for x in range(sec):
        time.sleep(1)
        app.queueFunction(app.setLabelBg,"target",switch_colors[x%2])
        app.queueFunction(app.setLabel,"target",labels[x%2])
        if thread["cmd"]=='stop':
            _stop_prediction(app,orig_color);return

    _stop_prediction(app,orig_color)

def _stop_prediction(app,orig_color):
    delete_all_images()
    app.queueFunction(app.setLabel,"target","")
    app.queueFunction(app.setLabelBg,"target","purple")
    thread["cmd"]=''
    thread["predictor"]='stopped'
    print("Prediction stopped...")

def delete_all_images():
    pass
