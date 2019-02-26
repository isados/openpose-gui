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
    _delete_all_images()
    app.queueFunction(app.setLabel,"target","")
    app.queueFunction(app.setLabelBg,"target","purple")
    thread["cmd"]=''
    thread["predictor"]='stopped'
    print("Prediction stopped...")

def _delete_all_images():
    pass

"""
1)  Read the last json file in the keypoints_json folder
2)  Convert to dict and find how many persons exist
3)  if no one: do nothing
4)  if >=1: extract the first person's object..
5)          read the 2nd and 4th keypoint.. and the other shoulder's keypoints as well
            .. the y coordinates to be exact
            and make a judgment to predict classes (separate function)
            [both_arms_up, right_arm_up, left_arm_up, both_arms_down]

6)  check exit flag

[posekeypoints[keypoint_indices[index]*3+1] \
    for index in range(4) \
        if posekeypoints[keypoint_indices[index]*3+2]>1]


"""
