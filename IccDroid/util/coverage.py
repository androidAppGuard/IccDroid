import os
import time
from threading import Thread

from configure import Configuration
from util.util import Util


class CoverageTasks(object):
    def __init__(self, coverage_dir, package_name):
        self.coverage_dir = coverage_dir
        self.package_name = package_name

        self.coverage_file_id = 1
        self._running = True

        if os.path.exists(coverage_dir) == False:
            os.mkdir(coverage_dir)

    def run(self):
        while self._running == True:
            # 1s record once time
            file_path = self.coverage_dir + '/coverage_' + str(self.coverage_file_id) + '.ec'
            # adb shell am broadcast -a edu.gatech.m3.emma.COLLECT_COVERAGE
            cmd = "adb -s " + Configuration.DEVICE_ID + " shell am broadcast -a edu.gatech.m3.emma.COLLECT_COVERAGE"

            Util.execute_cmd(cmd)
            # /data/data/#{app_package_name}/files/coverage.ec
            cmd = "adb -s " + Configuration.DEVICE_ID + " pull /data/data/" + self.package_name + r"/files/coverage.ec " + file_path
            Util.execute_cmd(cmd)
            print(cmd)

            self.coverage_file_id += 1
            time.sleep(2)

    def terminate(self):
        self._running = False
