from queue import Queue

class FunctionExtraction(object):

    def __init__(self):
        pass


    def get_edges(self, root_state):
        self.action_visit_flags = []
        self.edges = []
        self.traverse(root_state)
        return self.edges

    def traverse(self, root):
        for transition in root.transitions:
            (action_t, state_t1, dataflow) = transition
            action_key = root.type_hash + action_t.id
            if action_key not in self.action_visit_flags:
                self.edges.append((root, action_t, state_t1, dataflow))
                self.action_visit_flags.append(action_key)
                self.traverse(state_t1)

    def get_dataflow_function_table(self, root):
        function_table = []
        self.extract_functions(root)
        for dataflow_function in self.dataflow_functions:
            s0 = dataflow_function[0][0]
            state_sequence = [s0.type_hash]
            for transition in dataflow_function:
                state_sequence.append(transition[1].type_hash)
            function_table.append(state_sequence)
        return function_table

    def extract_functions(self, root):
        self.transition_visit_flags = []
        self.dataflow_functions = []
        self.queue = Queue()
        # step2 search startpoint
        self.recursive_analysis(root)
        while self.queue.qsize() > 0:
            tmp = self.queue.get()
            (s_t, s_t1, d_t_t1, action_flags) = tmp[len(tmp) - 1]
            flag = True
            for transition in s_t1.transitions:
                (a_t1, s_t2, d_t1_t2) = transition
                action_key = s_t1.type_hash + a_t1.id
                # ensure different transition
                if action_key not in action_flags:
                    action_flags.append(action_key)
                    # ensure consecutive and identical dataflow
                    if s_t1.type_hash != s_t2.type_hash and d_t_t1['activity'] == d_t1_t2['activity'] and d_t_t1[
                        'fragment'] == d_t1_t2['fragment']:
                        tmp.append((s_t1, s_t2, d_t1_t2, action_flags))
                        flag = False
            if flag:
                self.dataflow_functions.append(tmp)

    def recursive_analysis(self, state):
        for transition in state.transitions:
            (action_t, state_t1, dataflow) = transition
            action_key = state.type_hash + action_t.id
            if action_key not in self.transition_visit_flags:
                self.transition_visit_flags.append(action_key)
                # exclude the edge(si->si) for exist many
                if (dataflow['activity'] != "NoDataPassing" or dataflow[
                    'fragment'] != "NoDataPassing") and state.type_hash != state_t1.type_hash:
                    action_flags = [action_key]
                    self.queue.put([(state, state_t1, dataflow, action_flags)])
                self.recursive_analysis(state_t1)
