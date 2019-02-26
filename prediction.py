import time
import json

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
            [both_arms_up, right_arm_up, left_arm_up, both_arms_down, nothing_in_sight]

6)  check exit flag

[posekeypoints[keypoint_indices[index]*3+1] \
    for index in range(4) \
        if posekeypoints[keypoint_indices[index]*3+2]>1]



while(1):
    with open("path_to_keypoint_folder") as file:
        keypoint_dict=json.load(file)
        keypoint_dict= # extract the right parts
        num_of_persons = len(kdjfkaf)
        if num_of_persons > 0:
            posekeypoints=keypoint_dict[0] #extract the first person's list of coordinates
            keypoint_parts_to_POSE18={'right_shoulder':2,'right_hand':4, \
                                        'left_shoulder':5,'left_hand':7}
            keypoint_parts_list=list(keypoint_parts_to_POSE18.keys())
            keypoint_indices=list(keypoint_parts_to_POSE18.values())
        else:
            label='No one in sight'



def judge():
    right_hand=False
    left_hand=False

    if right_hand is not None and right_shoulder is not None:
        if right_hand<right_shoulder:
            right_arm_up=True
    if left_hand is not None and left_shoulder is not None:
        ifr left_hand<left_shoulder:
            left_arm_up=True

    if left_arm_up and right_arm_up:
        label='Both Arms Up'
    elif left_arm_up:
        label='Left Arm\'s Up'
    elif right_arm_up:
        label='Right Arm\'s Up'
    else:
        label='Both Arms Down'
"""
