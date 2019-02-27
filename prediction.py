import os
import time
import json
import serial

thread={'predictor':'stopped','openpose':'stopped','cmd':''} # Global flag
folder='../data/keypoint_json'
arduino_device="/dev/ttyUSB0"
# switch_colors=['blue','red']
# labels=['left arm up','right arm up']

def prediction(app):
    # for x in range(sec):
    #     time.sleep(1)
    #     app.queueFunction(app.setMessageBg,"target",switch_colors[x%2])
    #     app.queueFunction(app.setMessage,"target",labels[x%2])
    _delete_all_json_files()
    prev_label=None # This is to note the last predicted label, to avoid printing it twice

    # Access serial port for write operations
    past=time.time()
    try:
        ser = serial.Serial(arduino_device,115200)
    except:
        ser = None

    while(1):
        list_of_json_files=sorted(os.listdir(folder))

        if len(list_of_json_files)==0:
            label='Folder Empty'
        else: #Folder not empty
            label=_return_label_from_jsonfiles(list_of_json_files)

        # Display label and serial write to Arduino in fixed time intervals
        if prev_label!=label:
            prev_label=label
            app.queueFunction(app.setMessage,"target",label)
            if ser is not None and (time.time() - past) > 1:
                ser.write(f'{label}'.encode())
                past=time.time()
        
        # To prevent overloading the disk
        if len(list_of_json_files) > 300:
            _delete_all_json_files()

        #Exit Flag
        if thread["cmd"]=='stop':
            _stop_prediction(app,ser);return

def _return_label_from_jsonfiles(list_of_json_files):
    try: #Check if second last json file can be read
        with open(os.path.join(folder,list_of_json_files[-2])) as file:
            keypoint_dict=json.load(file)
            keypoint_dict= keypoint_dict['people']
            num_of_persons = len(keypoint_dict)

            if num_of_persons == 0:
                return 'No one in sight'
            else:
                list_of_persons_label=[]
                for person in keypoint_dict:
                    pose_keypoints = person['pose_keypoints']

                    # Define body parts of interest
                    parts_to_POSE18format = {'right_shoulder':2,'right_hand':4, \
                                                'left_shoulder':5,'left_hand':7}

                    keypoint_parts_list=list(parts_to_POSE18format.keys())
                    keypoint_indices=list(parts_to_POSE18format.values())

                    # Obtain Y coordinates of each body part
                    cordinates={keypoint_parts_list[index]:pose_keypoints[keypoint_indices[index]*3+1] \
                                for index in range(4) \
                                    if pose_keypoints[keypoint_indices[index]*3+2] > 0}
                    # cordinates={part:pose_keypoints[parts_to_POSE18format[part]*3+1] \
                    #             for part in keypoint_parts_list \
                    #             if pose_keypoints[parts_to_POSE18format[part]*3+1] > 0}

                    # Judgment
                    right_arm_up=False
                    left_arm_up=False

                    if cordinates.get('right_hand') is not None and cordinates.get('right_shoulder') is not None:
                        if cordinates.get('right_hand') < cordinates.get('right_shoulder'):
                            right_arm_up=True

                    if cordinates.get('left_hand') is not None and cordinates.get('left_shoulder') is not None:
                        if cordinates.get('left_hand') < cordinates.get('left_shoulder'):
                            left_arm_up=True

                    if left_arm_up and right_arm_up:
                        label='Both Arms Up'
                    elif left_arm_up:
                        label='Left Arm\'s Up'
                    elif right_arm_up:
                        label='Right Arm\'s Up'
                    else:
                        label='Both Arms Down'

                    #Append a label to the list
                    list_of_persons_label.append(label)

            """
            Labels have to be shown in this manner

            Person 1 : Right Arm Up
            Person 2 : Left Arm Up
            .
            .
            .
            Person N : ....
            """
            return "\n".join([f'Person {i+1} : {list_of_persons_label[i]}' for i in range(num_of_persons)])

    except:
        return 'Folder Empty'

def _stop_prediction(app,serial_port):
    _delete_all_json_files()
    if serial_port is not None: serial_port.write(b'off'); serial_port.close()
    app.queueFunction(app.setMessage,"target","")
    thread["cmd"]=''
    thread["predictor"]='stopped'
    print("Prediction stopped...")

def _delete_all_json_files():
    for file in os.listdir(folder):
        os.unlink(os.path.join(folder,file))
