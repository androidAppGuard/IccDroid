import os

from configure import Configuration
from exploration import AutoSQDroid
from util.util import Util

if __name__ == '__main__':

    apk_dir = r'F:\Tmp\AutoSQDroid\target_app\apks_2'
    for apk_name in os.listdir(apk_dir):
        if apk_name.endswith(".apk"):
            apk_path = os.path.join(apk_dir,apk_name)
            autoSQDroid = AutoSQDroid(apk_path)
            autoSQDroid.exploration()
