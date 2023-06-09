import os
import time

from configure import Configuration
from core.client import Client
from util.util import Util


class Env(object):
    def __init__(self, device, app_path):
        self.device = device
        self.app_path = app_path
        self.package = self.get_app_package(app_path)
        self.activity = self.get_app_lunch_activity(app_path)
        self.client = None

    def get_app_package(self, app_path):
        cmd = "aapt dump badging " + app_path + "| findstr package:"
        result = Util.execute_cmd(cmd)
        package = result.strip().split(" ")[1].split("'")[1]
        return package

    def get_app_lunch_activity(self, app_path):
        if "Signal" in app_path:
            return 'org.thoughtcrime.securesms.registration.RegistrationNavigationActivity'
        if "SimpleFileManager" in app_path:
            return 'com.simplemobiletools.filemanager.pro.activities.MainActivity'
        if "uhabits" in app_path:
            return "org.isoron.uhabits.activities.intro.IntroActivity"

        cmd = "aapt dump badging " + app_path + "| findstr launchable-activity:"
        result = Util.execute_cmd(cmd)
        activity = result.strip().split(" ")[1].split("'")[1]
        return activity

    def install_app(self):
        Util.execute_cmd( 'adb -s ' + Configuration.DEVICE_ID + ' install -t '+ self.app_path)
        # self.device.app_install(self.app_path)

    def uninstall_app(self):
        self.device.app_uninstall(self.package)

    def start_app(self):
        cmd = 'adb -s ' + Configuration.DEVICE_ID + " shell am start " + self.package + "/" + self.activity
        Util.execute_cmd(cmd)
        # update client
        self.client = Client(Configuration.SERVER_HOST, Configuration.SERVER_PORT)
        if self.client.check_server_state() == False:
            time.sleep(1)
            self.client.start_server()

    def stop_app(self):
        cmd = 'adb -s ' + Configuration.DEVICE_ID + ' shell am force-stop ' + self.package
        Util.execute_cmd(cmd)
        self.client.exit()
        self.client = None

    def restart_app(self):
        self.stop_app()
        self.start_app()
        time.sleep(1)

    def step(self, action):
        # system action
        for cmd in action.cmds:
            # Util.execute_cmd(cmd) exclude adb -s xxx shell :prefix
            Util.execute_cmd(cmd)
            # cmd = cmd[27:]
            # self.device.shell(cmd, stream=False)
        action.frequency += 1
        # recommend to sleep some time
        time.sleep(0.5)