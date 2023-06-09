import hashlib
import os
import time
from threading import Thread

import uiautomator2 as u2
from graphviz import Digraph

from configure import Configuration
from core.agent import Agent
from core.env import Env
from core.extraction import FunctionExtraction
from core.graph import Graph
from util.coverage import CoverageTasks
from util.logcat import LogcatTasks
from util.util import Util


class IccDroid(object):

    def __init__(self, app_path, icc_results):
        self.device = u2.connect_usb(Configuration.DEVICE_ID)
        self.device.implicitly_wait(5.0)
        self.agent = Agent(self.device, app_path)
        self.env = Env(self.device, app_path)
        self.icc_results = icc_results
        self.function_extraction = FunctionExtraction()
        self.functions_table = None

        out_dir = os.path.dirname(app_path) + r'/' + os.path.basename(app_path).split('.')[0]
        if os.path.exists(out_dir) == False:
            os.mkdir(out_dir)
        self.log_dir = out_dir + r'/log'
        self.coverage_dir = out_dir + r'/coverage'
        self.icc_file_path = out_dir + r'/dynamic_icc.txt'
        self.logcat_tasks = LogcatTasks(self.device, self.log_dir)
        self.logcat_thread = Thread(target=self.logcat_tasks.run)
        self.coverage_tasks = CoverageTasks(self.coverage_dir, self.env.package)
        self.coverage_thread = Thread(target=self.coverage_tasks.run)

        self.icc_call_graph = dict()

    def push_files(self):
        files_dir = os.path.join(os.path.abspath(os.path.curdir), 'files')
        for file_name in os.listdir(files_dir):
            file_path = os.path.join(files_dir, file_name)
            cmd = 'adb -s ' + Configuration.DEVICE_ID + " push " + file_path + r" /sdcard/tmp"
            Util.execute_cmd(cmd)

    def prepare_Q_learningExploration(self):
        Util.execute_cmd('adb root')
        self.push_files()
        # install app
        self.env.install_app()
        self.env.start_app()
        time.sleep(2)

    def Q_learningExploration(self): # Graph Enhancement Exploration
        # prepare initial environment
        self.prepare_Q_learningExploration()
        self.logcat_thread.start()
        self.coverage_thread.start()

        # step1: observe state and sample action in state
        state_t = self.agent.observe_env()
        action_t = self.agent.sample(state_t)
        self.graph = Graph(state_t, self.env, self.device)
        activity_t = None
        test_case = []

        self.start_time = time.time()
        last_model_size = -1
        cur_model_size = len(self.graph.transitions_hash)
        # judge the model stablize or over 1 hour
        while time.time() - self.start_time <= Configuration.STAGE_ONE_TIME:  # and last_model_size != cur_model_size:  # real condition is the model stablizes
            # is in package or action is None
            # package is not
            if len(test_case) >= 100 or (
                    self.device.info['currentPackageName'] != self.env.package and self.device.info[
                'currentPackageName'] not in Configuration.DEVICE_PACKAGE):
                # restart and assign state_t/action_t
                self.env.restart_app()
                state_t = self.agent.observe_env()
                action_t = self.agent.sample(state_t)
                activity_t = self.device.app_current()['activity']
                test_case = []
            # action is none
            if action_t == None:
                self.agent.clean_action_value(state_t, action_t)
                self.env.restart_app()
                state_t = self.agent.observe_env()
                action_t = self.agent.sample(state_t)
                activity_t = self.device.app_current()['activity']
                test_case = []

            # step2: execute action and fetch dataflow (stop() will crash the client)
            self.env.step(action_t)
            test_case.append(action_t)
            dataflow = self.env.client.get_dataflow()
            print("geting dataflow(icc_info): ", dataflow)
            icc_info = self.env.client.get_iccinfo()
            print("geting icc_info: ", icc_info)
            self.logcat_tasks.check_crash(test_case)  # reocrde log and crash

            # step3: jump to new state
            state_t1 = self.agent.observe_env()
            activity_t1 = self.device.app_current()['activity']

            # no actions in state_t1
            if state_t1 == None:
                self.agent.clean_action_value(state_t, action_t)
                self.agent.clean_action_value(state_t, action_t)
                self.env.restart_app()
                state_t = self.agent.observe_env()
                action_t = self.agent.sample(state_t)
                activity_t = self.device.app_current()['activity']
                test_case = []
                continue
            # record ICC call graph
            if activity_t != None and activity_t1 != "" and activity_t1 != activity_t:
                cur_component = activity_t
                target_component = activity_t1
                key = cur_component + '->' + target_component
                if key not in self.icc_call_graph.keys():
                    self.icc_call_graph.update({key: 1})
                else:
                    self.icc_call_graph[key] = self.icc_call_graph[key] + 1

            action_t1 = self.agent.sample(state_t1)

            # step4: update Q-table
            frequency_reward = self.agent.get_frequency_reward(action_t)
            # type_reward = self.agent.get_type_reward(state_t, state_t1)
            icc_reward = self.agent.get_iccreward(icc_info, self.icc_results)
            self.agent.updateQ_table(state_t, action_t, state_t1, frequency_reward + icc_reward)

            # maintain the graph and save ICC info into files
            self.graph.add_transition(state_t, action_t, state_t1, dataflow)
            self.graph.add_iccInfo(icc_info, self.icc_file_path)
            if int(time.time() - self.start_time) % 600 == 0:
                last_model_size = cur_model_size
                cur_model_size = len(self.graph.transitions_hash)

            # step5: recycle
            state_t = state_t1
            action_t = action_t1
            # break
        # stop server connection
        self.env.client.exit()
        self.graph.save_icc_call_graph(self.icc_call_graph, self.icc_file_path, "Q-learn UIExploration edge count： ")


    def prepare_Inter_functionExploration(self):
        self.env.restart_app()
        # init function_visit_flags
        self.functions_order_visit_flags = []
        self.functions_md5 = []
        for function in self.functions_table:
            content = ""
            for state_hash in function:
                content += state_hash
            md5_value = hashlib.md5(content.encode('utf8')).hexdigest()
            self.functions_md5.append(md5_value)

    def Q_LearningInter_functionExploration(self):  # ICC-Guided Exploration
        self.prepare_Inter_functionExploration()

        # step1: observe state and sample action in state
        state_t = self.agent.observe_env()
        action_t = self.agent.sample(state_t)
        activity_t = None
        # record the state sequence
        seq = [state_t.type_hash]
        test_case = []

        while time.time() - self.start_time <= Configuration.STAGE_ONE_TIME + Configuration.STAGE_TWO_TIME:  # two hour exploration
            # package is not: the length of test case should further set
            if len(test_case) > 100 or (self.device.info['currentPackageName'] != self.env.package and self.device.info[
                'currentPackageName'] not in Configuration.DEVICE_PACKAGE):
                # restart and assign state_t/action_t
                self.env.restart_app()
                state_t = self.agent.observe_env()
                action_t = self.agent.sample(state_t)
                activity_t = self.device.app_current()['activity']
                seq = [state_t.type_hash]
                test_case = []

            # action is none
            if action_t == None:
                self.agent.clean_action_value(state_t, action_t)
                self.env.restart_app()
                state_t = self.agent.observe_env()
                action_t = self.agent.sample(state_t)
                activity_t = self.device.app_current()['activity']
                seq = [state_t.type_hash]
                test_case = []

            # step2: execute action (stop() will crash the client)
            self.env.step(action_t)
            test_case.append(action_t)
            self.logcat_tasks.check_crash(test_case)

            # step3: jump to new state
            state_t1 = self.agent.observe_env()
            activity_t1 = self.device.app_current()['activity']

            # no actions in state_t1
            if state_t1 == None:
                self.agent.clean_action_value(state_t, action_t)
                self.env.restart_app()
                state_t = self.agent.observe_env()
                action_t = self.agent.sample(state_t)
                activity_t = self.device.app_current()['activity']
                seq = [state_t.type_hash]
                test_case = []
                continue

            # record ICC call graph
            if activity_t != None and activity_t1 != "" and activity_t1 != activity_t:
                cur_component = activity_t
                target_component = activity_t1
                key = cur_component + '->' + target_component
                if key not in self.icc_call_graph.keys():
                    self.icc_call_graph.update({key: 1})
                else:
                    self.icc_call_graph[key] = self.icc_call_graph[key] + 1

            action_t1 = self.agent.sample(state_t1)
            seq.append(state_t1.type_hash)

            # step4: update Q-table
            function_reward = self.agent.get_function_reward(seq, self.functions_table, self.functions_md5,
                                                             self.functions_order_visit_flags)
            print(seq, function_reward)
            self.agent.updateQ_table(state_t, action_t, state_t1, function_reward)

            # step5: recycle
            state_t = state_t1
            action_t = action_t1

        self.graph.save_icc_call_graph(self.icc_call_graph, self.icc_file_path, "ICC-guided Exploration edge count： ")

    def end_exploration(self):
        # stop log_thread
        self.logcat_tasks.terminate()
        self.coverage_tasks.terminate()
        self.logcat_thread.join()
        self.coverage_thread.join()
        # uninstall apk
        uninstall_apk_cmd = 'adb -s ' + Configuration.DEVICE_ID + ' uninstall ' + self.env.package
        Util.execute_cmd(uninstall_apk_cmd)

    def exploration(self):
        # self.Q_learningExploration()
        # self.functions_table = self.function_extraction.get_dataflow_function_table(self.graph.root)
        # self.Q_LearningInter_functionExploration()
        # self.end_exploration()

        self.Q_learningExploration()
