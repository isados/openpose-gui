import time

thread={'status':'stopped','cmd':''} # Global flag

switch_colors=['blue','red']
labels=['left arm up','right arm up']
def prediction(sec,app,orig_color):
    for x in range(sec):
        time.sleep(1)
        app.queueFunction(app.setLabelBg,"target",switch_colors[x%2])
        app.queueFunction(app.setLabel,"target",labels[x%2])
        if thread["cmd"]=='stop':
            return None
    return None

def delete_all_images():
    pass
