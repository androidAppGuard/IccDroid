import os
import socket

from configure import Configuration
from util.util import Util


class Client(object):

    def __init__(self, host, port):
        # start server command
        # this command only send once
        if Configuration.SOCKET_FLAG == False:
            Util.execute_cmd("adb -s " + Configuration.DEVICE_ID + " forward tcp:" + str(port) + " tcp:" + str(port))
            SOCKET_FLAG = True
        Util.execute_cmd("adb -s " + Configuration.DEVICE_ID + " shell am broadcast -a edu.dhu.cs.816space")
        try:
            self.socket = socket.socket()
            self.socket.connect((host, port))
            self.socket.settimeout(1)
            # self.socket.setblocking(False)
        except Exception as exception:
            print("catch Socket connect Exception")
            print(exception)

    def restartServer(self):
        Util.execute_cmd("adb -s " + Configuration.DEVICE_ID + " shell am broadcast -a edu.dhu.cs.816space")
        try:
            self.socket = socket.socket()
            self.socket.settimeout(1)
            # self.socket.setblocking(False)
            self.socket.connect((self.host, self.port))
        except Exception as exception:
            print("catch Socket connect Exception")
            print(exception)

    def check_server_state(self):
        try:
            self.socket.send("state\n".encode("utf-8"))
            data = self.socket.recv(1024).decode("utf-8").strip()
        except Exception as exception:
            print("catch Socket check_server_state Exception")
            self.restartServer()
            print(exception)
        finally:
            data = False
        if data == "true":
            return True
        else:
            return False

    def start_server(self):
        Util.execute_cmd("adb -s " + Configuration.DEVICE_ID + " shell am broadcast -a edu.dhu.cs.816space")

    def exit(self):
        try:
            self.socket.send("exit\n".encode("utf-8"))
            data = self.socket.recv(1024).decode("utf-8").strip()
        except Exception as exception:
            print("catch Socket exit Exception")
            self.restartServer()
            print(exception)
        finally:
            data = False
        if data == "true":
            return True
        else:
            return False

    # consider the server stop for the app may crash
    # return {'activity': '938e58dcce19b1d0d2c87e9527518b84', 'fragment': 'NoDataPassing'}
    def get_dataflow(self):
        result = dict()
        try:
            # activity dataflow {NoActivity NoDataPassing DataPassing_XX app_crash}
            self.socket.send("getActivityDataflow\n".encode("utf-8"))
            data = self.socket.recv(1024).decode("utf-8").strip()
        except Exception as exception:
            print("catch Socket get_dataflow Exception")
            self.restartServer()
            print(exception)
        finally:
            data = "NoDataPassing"
        # DataPassing_938e58dcce19b1d0d2c87e9527518b84 NoDataPassing NoActivity ""
        if data == "NoDataPassing" or data == "NoActivity":
            result.update({"activity": "NoDataPassing"})
        elif data.startswith("DataPassing_"):
            result.update({"activity": data.split("DataPassing_")[1]})
        else:
            result.update({"activity": "NoDataPassing"})
        # fragment dataflow
        try:
            self.socket.send("getFragementDataflow\n".encode("utf-8"))
            data = self.socket.recv(1024).decode("utf-8").strip()
        except Exception as exception:
            print("catch Socket get_dataflow Exception")
            self.restartServer()
            print(exception)
        finally:
            data = "NoDataPassing"
        # DataPassing_938e58dcce19b1d0d2c87e9527518b84 NoDataPassing NoActivity ""
        if data == "NoDataPassing" or data == "NoActivity" or data == "NoFragment":
            result.update({"fragment": "NoDataPassing"})
        elif data.startswith("DataPassing_"):
            result.update({"fragment": data.split("DataPassing_")[1]})
        else:
            result.update({"fragment": "NoDataPassing"})
        return result
