import os
import time
import json

thread={'predictor':'stopped','openpose':'stopped','cmd':''} # Global flag
folder='../data/keypoint_json'
# switch_colors=['blue','red']
# labels=['left arm up','right arm up']
def _delete_all_json_files():
    for file in os.listdir(folder):
        os.unlink(os.path.join(folder,file))

def prediction(sec,app,orig_color):
    # for x in range(sec):
    #     time.sleep(1)
    #     app.queueFunction(app.setLabelBg,"target",switch_colors[x%2])
    #     app.queueFunction(app.setLabel,"target",labels[x%2])
    _delete_all_json_files()
    prev_label=None # This is to note the last predicted class, to avoid printing it twice
    folder_empty=False # Flag to avoid printing "Folder is Empty" mess twice
    while(1):
        list_of_files=sorted(os.listdir(folder))
        if len(list_of_files) ==0 and folder_empty==False:
            label='Folder Empty'
            prev_label=None
            folder_empty=True
        elif len(list_of_files)==0 and folder_empty==True:
            pass
        else: #Folder not empty
            folder_empty=False
            try: #Check if second last json file can be read
                with open(os.path.join(folder,list_of_files[-2])) as file:
                    keypoint_dict=json.load(file)
                    keypoint_dict= keypoint_dict['people']
                    num_of_persons = len(keypoint_dict)
                    if num_of_persons > 0:
                        posekeypoints=keypoint_dict[0]['pose_keypoints'] #extract the first person's list of coordinates
                        keypoint_parts_to_POSE18={'right_shoulder':2,'right_hand':4, \
                                                    'left_shoulder':5,'left_hand':7}

                        keypoint_parts_list=list(keypoint_parts_to_POSE18.keys())
                        keypoint_indices=list(keypoint_parts_to_POSE18.values())
                        cordinates={keypoint_parts_list[index]:posekeypoints[keypoint_indices[index]*3+1] \
                            for index in range(4) \
                                if posekeypoints[keypoint_indices[index]*3+2]>0 }
                        # print(cordinate)
                        #Judgment
                        right_arm_up=False
                        left_arm_up=False

                        if cordinates.get('right_hand') is not None and cordinates.get('right_shoulder') is not None:
                            if cordinates.get('right_hand')<cordinates.get('right_shoulder'):
                                right_arm_up=True

                        if cordinates.get('left_hand') is not None and cordinates.get('left_shoulder') is not None:
                            if cordinates.get('left_hand')<cordinates.get('left_shoulder'):
                                left_arm_up=True

                        if left_arm_up and right_arm_up:
                            label='Both Arms Up'
                        elif left_arm_up:
                            label='Left Arm\'s Up'
                        elif right_arm_up:
                            label='Right Arm\'s Up'
                        else:
                            label='Both Arms Down'
                    else:
                        label='No one in sight'
            except:
                label='Folder Empty'
        # Change label
        if prev_label!=label:
            prev_label=label
            app.queueFunction(app.setLabel,"target",label)
        else:
            pass
        #Exit Flag
        if thread["cmd"]=='stop':
            _stop_prediction(app,orig_color);return

def _stop_prediction(app,orig_color):
    _delete_all_json_files()
    app.queueFunction(app.setLabel,"target","")
    thread["cmd"]=''
    thread["predictor"]='stopped'
    print("Prediction stopped...")
