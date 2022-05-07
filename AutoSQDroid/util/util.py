import os
import random
import subprocess
import time

import cv2

from configure import Configuration
from core.action import Action


class Util(object):
    FILE_ID = 1

    @staticmethod
    def random_text():
        text_style = random.randint(0, 8)
        text_length = random.randint(1, 5)
        nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                   "u", "v", "w", "x", "y", "z"]
        symbols = [",", ".", "!", "?"]
        i = 0
        random_string = ""
        if text_style == 0:
            while i < text_length:
                now_num = nums[random.randint(0, len(nums) - 1)]
                random_string = random_string + now_num
                i = i + 1
        elif text_style == 1:
            while i < text_length:
                now_letters = letters[random.randint(0, len(nums) - 1)]
                random_string = random_string + now_letters
                i = i + 1
        elif text_style == 2:
            while i < text_length:
                s_style = random.randint(0, 2)
                if s_style == 0:
                    now_letters = nums[random.randint(0, len(nums) - 1)]
                    random_string = random_string + now_letters
                elif s_style == 1:
                    now_letters = letters[random.randint(0, len(letters) - 1)]
                    random_string = random_string + now_letters
                elif s_style == 2:
                    now_letters = symbols[random.randint(0, len(symbols) - 1)]
                    random_string = random_string + now_letters
                i = i + 1
        elif text_style == 3:
            country = ["Beijing", "London", "Paris", "New York", "Tokyo"]
            countrynum = random.randint(0, 4)
            random_string = country[countrynum]
        elif text_style == 4:
            random_string = letters[random.randint(0, len(letters) - 1)]
        elif text_style == 5:
            random_string = nums[random.randint(0, len(nums) - 1)]
        elif text_style == 6:
            special_text = ["www.google.com", "t"]
            specialnum = random.randint(0, len(special_text) - 1)
            random_string = special_text[specialnum]
        return random_string

    @staticmethod
    def execute_cmd(cmd):
        with os.popen(cmd) as console:
            result = console.read()
        return result

    @staticmethod
    def random_system_action():
        index = random.randint(0, len(Configuration.SYSTEM_ACTIONS) - 1)
        action = Action(None, Configuration.SYSTEM_ACTIONS[index], None,
                        's' + str(index))
        return action

    @staticmethod
    def record_state_action_img(device, state_t, action_t):
        path = "./output/ui_" + str(Util.FILE_ID) + ".png"
        Util.FILE_ID += 1
        device.screenshot(path)
        img = cv2.imread(path)
        if action_t == None:
            cv2.addText(img, "State is None",
                        (int(Configuration.DEVICE_SCREEN_WIDTH / 2), int(Configuration.DEVICE_SCREEN_HEIGHT / 2)),
                        cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
        elif action_t.type in Configuration.SYSTEM_ACTIONS:
            cv2.addText(img, action_t.id,
                        (int(Configuration.DEVICE_SCREEN_WIDTH / 2), int(Configuration.DEVICE_SCREEN_HEIGHT / 2)),
                        cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
        else:
            cv2.rectangle(img, (action_t.view.xmin, action_t.view.ymin), (action_t.view.xmax, action_t.view.ymax),
                          (0, 255, 0), 2)
        cv2.imwrite(path, img)

    @staticmethod
    def save_event_sequence(event_sequence, file_path):
        if len(event_sequence) == 0:
            return
        # save each action
        with open(file_path, 'a+', encoding='utf-8') as file:
            file.write("test case length:" + str(len(event_sequence)) + "\n")
            for action in event_sequence:
                info = dict()
                if action.type == Configuration.ACTION_TYPE_CLICK:
                    info.update({"type": "click"})
                elif action.type == Configuration.ACTION_TYPE_LONGCLICK:
                    info.update({"type": "longClick"})
                elif action.type == Configuration.ACTION_TYPE_EDIT:
                    info.update({"type": "edit", "text": action.text})
                elif action.type == Configuration.ACTION_TYPE_RESTART:
                    info.update({"type": "restart"})
                elif action.type == Configuration.ACTION_TYPE_BACK:
                    info.update({"type": "back"})
                elif action.type == Configuration.ACTION_TYPE_SCROLL:
                    info.update({"type": "scroll"})
                info.update({"cmds": action.cmds})
                file.write(str(info))
                file.write("\n")
