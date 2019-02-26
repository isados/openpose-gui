from pythondaemon.daemon import Daemon
import sys
import os

init_script="pid"

class MyDaemon(Daemon):
    def __init__(self, *args, **kwargs):
        super(MyDaemon, self).__init__(*args, **kwargs)

    def run(self):
        # Launch the OpenPose script & save the PID to a file
        os.system(f"./{init_script}.sh")

    def kill(self):
        # Read the PID from file; and kill the OpenPose program
        if os.path.isfile(f"{init_script}.pid"):
            with open(f"{init_script}.pid") as pidfile:
                pid=pidfile.readline().strip()
                os.system(f"kill -9 {pid}")
                # os.system(f"docker stop {pid}")
                os.unlink(f"./{init_script}.pid")
                self.stop()
        else: print("Process has not started!")
