import networkx as nx
import numpy as np
import math


class Bug(object):

    def __init__(self, bug_id, time_currency, in_ts, entrance, exit_position,
                 arena, edge_weight_dict, district_weight_add_decay):
        super(Bug, self).__init__()
        assert arena is not None
        assert in_ts >= arena.graph['start_time']
        self.bug_id = bug_id
        self.time_currency = time_currency
        self.in_ts = in_ts
        self.entrance = entrance
        self.exit = exit_position
        self.arena = arena
        self.edge_weight_dict = edge_weight_dict
        self.district_weight_add_decay = district_weight_add_decay
        self.truth_path = []
        self.truth_path.append({'ts': in_ts,
                                'position': entrance})
        self.passed_district_dict = {}
        self.current_ts = in_ts
        self.current_position = entrance
        self.current_district = None
        self.last_position = None

    def ranger(self):
        while (self.time_currency > 0) and (
                self.current_ts < self.arena.graph['end_time']):
            next_node = self.choose_path()
            self.step(next_node)
        if self.current_position != self.exit:
            for n in nx.shortest_path(self.arena, self.current_position,
                                      self.exit):
                if self.current_position != n:
                    self.step(n, asap=True)

    def step(self, next_node, asap=False):
        mean = self.arena[self.current_position][next_node]['mean']
        std = self.arena[self.current_position][next_node]['std']
        min_time = self.arena[self.current_position][next_node]['min']
        if asap:
            time_cost = min_time
        else:
            time_cost = int(min(max(np.random.normal(mean, std), min_time),
                                self.time_currency, self.arena.graph[
                                    'end_time'] - self.current_ts))
        self.current_district = \
            self.arena[self.current_position][next_node]['district']
        self.last_position = self.current_position
        self.current_position = next_node
        self.current_ts += time_cost
        self.time_currency -= time_cost
        self.truth_path.append({'ts': self.current_ts,
                                'position': self.current_position})
        if time_cost > (1.01 * mean):
            if self.current_district not in self.passed_district_dict.keys():
                self.passed_district_dict[self.current_district] = 1
            else:
                self.passed_district_dict[self.current_district] += 1

    def choose_path(self):
        weight_dict = {}
        sum = 0
        for n in nx.neighbors(self.arena, self.current_position):
            weight_add = self.arena[self.current_position][n]['weight_add']
            candidate_d = self.arena[self.current_position][n]['district']
            if candidate_d not in self.passed_district_dict.keys():
                district_weight_add = self.district_weight_add_decay[0]
            else:
                ever = min(self.passed_district_dict[candidate_d],
                           len(self.district_weight_add_decay) - 1)
                district_weight_add = self.district_weight_add_decay[ever]
            if n == self.last_position:
                item = math.ceil(self.edge_weight_dict[
                                     'unlikely'] * (
                                         district_weight_add + weight_add))
                weight_dict[n] = range(sum, sum + item)
                sum += item
            elif self.arena[self.current_position][n]['district'] == \
                    self.current_district:
                item = math.ceil(self.edge_weight_dict[
                                     'likely'] * (
                                         district_weight_add + weight_add))
                weight_dict[n] = range(sum, sum + item)
                sum += item
            else:
                item = math.ceil(self.edge_weight_dict[
                                     'usual'] * (
                                             district_weight_add + weight_add))
                weight_dict[n] = range(sum, sum + item)
                sum += item
        seed = np.random.randint(sum)
        for node in weight_dict.keys():
            if seed in weight_dict[node]:
                return node
        return None

    def get_truth_path(self):
        return self.truth_path

    def get_personal_path_data(self):
        return {'bug_id': self.bug_id, 'path': self.truth_path}
