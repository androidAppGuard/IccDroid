import json
import os
import time

from graphviz import Digraph


class Graph(object):
    STATE_NUMBER = 1

    graph = Digraph()

    def __init__(self, root, env, device):
        self.root = root
        self.device = device
        self.env = env

        self.states = {root.type_hash: root}  # dict=>{state.hash:state}
        self.transitions = []
        self.transitions_hash = []
        self.icc_infos = dict()

    def add_iccInfo(self, icc_info, icc_file_path):
        if icc_info == None:
            return
        else:
            key = icc_info['sendComponent'] + "->" + icc_info['targetComponent']
            if key not in self.icc_infos.keys():
                self.icc_infos.update({key: icc_info})
        # write icc Info
        with open(icc_file_path, 'a+', encoding='utf-8') as icc_file:
            icc_file.write(json.dumps(icc_info))

    def save_icc_call_graph(self, icc_call_graph, icc_call_graph_path, stage):

        with open(icc_call_graph_path, 'a+', encoding='utf-8') as icc_file:
            icc_file.write('*********'+ stage + str(len(icc_call_graph.keys())) + '************')
            for key in icc_call_graph.keys():
                icc_file.write(key + " : " + str(icc_call_graph[key]))

    def add_transition(self, state_t, action_t, state_t1, dataflow):
        if self.device.info['currentPackageName'] != self.env.package:
            return
        # state_t/state_t1/action_t is must not null
        # maintain the graph property  graph.states
        if state_t.type_hash not in self.states.keys():
            self.states.update({state_t.type_hash: state_t})
        if state_t1.type_hash not in self.states.keys():
            self.states.update({state_t1.type_hash: state_t1})
        transition_hash = state_t.type_hash + action_t.id
        if transition_hash not in self.transitions_hash:
            # maintain the state node
            self.states[state_t.type_hash].transitions.append((action_t, state_t1, dataflow))

            # self.transitions
            self.transitions.append((action_t, state_t1, dataflow))
            self.transitions_hash.append(transition_hash)

            # # each graph edge
            # Graph.graph.edge(state_t.type_hash, state_t1.type_hash, action_t.id)
            # Graph.graph.render('graph.gv', view=True)
