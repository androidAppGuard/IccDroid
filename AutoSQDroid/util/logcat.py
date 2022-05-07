import os
from queue import Queue

from configure import Configuration
from util.util import Util


class LogcatTasks(object):
    def __init__(self, device, log_dir):
        self.device = device
        self.log_dir = log_dir
        self.queue = Queue()

        self._running = True
        self.crash_id = 1
        if os.path.exists(self.log_dir) == False:
            os.mkdir(self.log_dir)
            log_file = self.log_dir + r'/log.txt'
            file = open(log_file, 'a+', encoding='utf-8')
            file.close()
        # clean logcat cache
        Util.execute_cmd("adb -s " + Configuration.DEVICE_ID + " logcat -c")

    def terminate(self):
        self._running = False

    def run(self):
        lines = self.device.shell("logcat", stream=True)
        try:
            for line in lines.iter_lines():  # r.iter_lines(chunk_size=512, decode_unicode=None, delimiter=None)
                if self._running == False:
                    break
                # record log and crash log
                row_content = line.decode('utf-8') + '\n'
                with open(self.log_dir + r'/log.txt', 'a+', encoding='utf-8') as log_file:
                    log_file.write(row_content)
                self.queue.put(row_content)
        finally:
            lines.close()  # this method must be called

    def check_crash(self, event_sequence):
        content = ''
        size = self.queue.qsize()
        while size > 0:
            size -= 1
            content += self.queue.get(timeout=0.5)
        if 'Exception' in content:
            log_file_path = self.log_dir + r'/crash_log_' + str(self.crash_id) + r'.txt'
            crash_event_path = self.log_dir + r'/crash_event_' + str(self.crash_id) + r'.txt'
            self.crash_id += 1
            with open(log_file_path, 'a+', encoding='utf-8') as log_file:
                log_file.write(content)
            Util.save_event_sequence(event_sequence, crash_event_path)
