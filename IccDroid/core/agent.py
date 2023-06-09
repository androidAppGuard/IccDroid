# notice exploration should maintian graph
# first stage exploration; second exploration limit length of test case and time
import hashlib
import os

from configure import Configuration
from core.state import State
import random

from util.util import Util
import time


class Agent(object):

    def __init__(self, device, app_path):
        self.device = device  # u2.connect_usb()
        self.q_table = dict()  # <hash(state.type_hash + action.id), value>

        out_dir = os.path.dirname(app_path) + r'/' + os.path.basename(app_path).split('.')[0]
        if os.path.exists(out_dir) == False:
            os.mkdir(out_dir)
        self.tmp_dir = out_dir + r'/tmp'
        if os.path.exists(self.tmp_dir) == False:
            os.mkdir(self.tmp_dir)
        # enable adb view server
        cmd = "adb -s " + Configuration.DEVICE_ID + " shell service call window 1 i32 4939"
        Util.execute_cmd(cmd)

    def observe_env(self):  # return State
        ## uiautomator2 get uihierarchy.xml
        xml = self.device.dump_hierarchy()
        file = open(self.tmp_dir + '/ui.xml', 'w', encoding='utf-8')
        file.write(xml)
        file = open(self.tmp_dir + '/ui.xml', 'r', encoding='utf-8')

        ## adb get uihierarchy.xml
        # cmd = "adb -s " + Configuration.DEVICE_ID + " shell uiautomator dump --compressed  /data/uidump.xml"
        # print(cmd)
        # Util.execute_cmd(cmd)
        # cmd = "adb -s " + Configuration.DEVICE_ID + " pull /data/uidump.xml " + self.tmp_dir + '/ui.xml'
        # print(cmd)
        # Util.execute_cmd(cmd)
        # file = open(self.tmp_dir + '/ui.xml', 'r', encoding='utf-8')
        lines = file.readlines()
        state = State(lines)
        if len(state.all_actions) == 0:
            return None
        return state

    def sample(self, state):  # return Action (None represent no action)
        # init action not in Q-table
        for action in state.all_actions:
            key = state.type_hash + action.id
            if key not in self.q_table.keys():
                self.q_table.update({key: Configuration.Q_TABLE_INITVALUE})

        # 0.05 probability select system action
        probility = random.randint(1, 100) / 100
        if (probility <= Configuration.SYSTEM_ACTION_PROBABILITY):
            return Util.random_system_action()

        # select ui action with max value  from Q-table
        selected_actions = []
        cur_val = 0.0
        for action in state.all_actions:
            key = state.type_hash + action.id
            if self.q_table[key] > cur_val:
                selected_actions.clear()
                selected_actions.append(action)
                cur_val = self.q_table[key]
            elif self.q_table[key] == cur_val:
                selected_actions.append(action)
            else:
                continue
        if len(selected_actions) == 0:
            return None
        return selected_actions[random.randint(0, len(selected_actions) - 1)]

    def get_frequency_reward(self, action):
        # system action do not consider
        if action.type in Configuration.SYSTEM_ACTIONS:
            return 0
        return 1.0 / action.frequency

    def get_iccreward(self, icc_info, icc_results):
        if icc_results == None or len(icc_results.keys()) == 0 or icc_info == None:
            return 0
        cur_icc = icc_info["sendComponent"] + "->" + icc_info["targetComponent"]
        reward = 0
        for key in icc_results.keys():
            if cur_icc == key and icc_results[key] > 0:
                icc_results[key] = 0
                reward = 1
        return reward

    def get_type_reward(self, state_t, state_t1):
        count = 0
        for elem in state_t1.classname_list:
            if elem not in state_t.classname_list:
                count += 1
        return count * 1.0 / len(state_t1.classname_list)

    # TODO untesting
    def get_function_reward(self, seq, functions_table, functions_md5, functions_order_visit_flags):
        if len(functions_md5) == 0:
            return 0
        # function_table: [[s1,s2,..],[s1,s2,..]]
        # functions_md5: [md5_1,md5_2,...]
        # functions_order_visit_flags: [md5_2,?]
        #  function_table may be None when calculating reward
        # part1: calculate explored function reward
        sub_sequence_md5s = []
        for i in range(len(seq)):
            content = ""
            for j in range(i, len(seq)):
                content += seq[j]
                md5_value = hashlib.md5(content.encode('utf8')).hexdigest()
                sub_sequence_md5s.append(md5_value)
        count = 0
        function_order = []  # record the function order
        for sub_sequence_md5 in sub_sequence_md5s:
            # can not ignore repeat state sequence
            for function_md5 in functions_md5:
                flag = True
                if sub_sequence_md5 == function_md5:
                    count += 1
                    if flag:
                        flag = False
                        function_order.append(function_md5)
        explored_function_reward = count * 1.0 / len(functions_md5)

        # part2 calculate promising-to-explore function reward
        last_state = seq[len(seq) - 1]
        count = 0
        for function in functions_table:
            if function[len(function) - 1] == last_state:
                count += 1
        promising_explore_function_reward = count * 1.0 / len(functions_table)

        # part3 calculate order reward
        order_reward = 0.0
        if len(function_order) != 0:
            content = ""
            for each_order in function_order:
                content += each_order
            order_md5 = hashlib.md5(content.encode('utf8')).hexdigest()
            if order_md5 not in functions_order_visit_flags:
                order_reward = 1.0
                functions_order_visit_flags.append(order_md5)
        return explored_function_reward + promising_explore_function_reward + order_reward

    # Q_table update
    def updateQ_table(self, state_t, action_t, state_t1, reward):
        # get max target value in state_t1
        target = 0.0
        for action in state_t1.all_actions:
            key = state_t1.type_hash + action.id
            if self.q_table[key] >= target:
                target = self.q_table[key]
        # get value of action_t in state_t
        source_key = state_t.type_hash + action_t.id
        # system action
        if source_key not in self.q_table.keys():
            self.q_table[source_key] = Configuration.Q_TABLE_INITVALUE
        # update
        self.q_table[source_key] = self.q_table[source_key] + Configuration.Q_TABLE_LEARNING_RATE * (
                reward + Configuration.Q_TABLE_GAMMY * target - self.q_table[source_key]
        )

    # clean one action value to 0
    def clean_action_value(self, state_t, action_t):
        key = state_t.type_hash + action_t.id
        self.q_table[key] = 0.0
