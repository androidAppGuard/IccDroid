from configure import Configuration
import random
from core.view import View

"""
Record the information of the app's action
"""


class Action(object):

    def __init__(self, view, type, text, id):
        self.view = view
        self.type = type
        self.text = text
        self.id = str(id)
        self.frequency = 0.0
        self.cmds = self.get_adb_cmds()

    def get_adb_cmds(self):
        cmds = []
        if self.type == Configuration.ACTION_TYPE_CLICK:
            cmd = "adb -s " + Configuration.DEVICE_ID + " shell input tap " + str(self.view.x) + " " + str(self.view.y)
            cmds.append(cmd)
        elif self.type == Configuration.ACTION_TYPE_LONGCLICK:  # 500ms
            cmd = "adb -s " + Configuration.DEVICE_ID + " shell input swipe " + str(self.view.x) + " " + str(
                self.view.y) + " " + str(self.view.x) + " " + str(self.view.y) + " 500"
            cmds.append(cmd)
        elif self.type == Configuration.ACTION_TYPE_EDIT:
            # invoke the keyboard
            cmd = "adb -s " + Configuration.DEVICE_ID + " shell input tap " + str(self.view.x) + " " + str(self.view.y)
            cmds.append(cmd)
            if random.randint(0, 2) % 2 == 0:  # randomly clean text
                for i in range(0, len(self.view.text)):
                    cmd = "adb -s " + Configuration.DEVICE_ID + " shell input"
                    cmd += 'keyevent' + ' 67'
                    cmds.append(cmd)
            # fill the text
            cmd = "adb -s " + Configuration.DEVICE_ID + " shell input text \"" + self.text + "\""
            cmds.append(cmd)
            # exit the keyboard
            cmd = "adb -s " + Configuration.DEVICE_ID + " shell input keyevent 4"
            cmds.append(cmd)

        # system action
        elif self.type == Configuration.ACTION_TYPE_SCROLL:
            cmd = "adb -s " + Configuration.DEVICE_ID + " shell input swipe " + str(
                Configuration.DEVICE_SCREEN_WIDTH / 2) + " " + str(Configuration.DEVICE_SCREEN_HEIGHT / 2) + " " + str(
                Configuration.DEVICE_SCREEN_WIDTH / 2) + " 0 1000"
            cmds.append(cmd)
        elif self.type == Configuration.ACTION_TYPE_BACK:
            cmd = "adb -s " + Configuration.DEVICE_ID + " shell input keyevent 4"
            cmds.append(cmd)
        elif self.type == Configuration.ACTION_TYPE_RESTART:
            cmd = "adb -s " + Configuration.DEVICE_ID + " shell input keyevent 3"
            cmds.append(cmd)
        return cmds
