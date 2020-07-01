import numpy as np


class BaseCount(object):

    def __init__(self, arena, position, in_district, in_possibility,
                 out_possibility):
        super(BaseCount, self).__init__()
        self.arena = arena
        self.position = position
        self.in_district = in_district
        self.in_possibility = in_possibility
        self.out_possibility = out_possibility

    def get_inout_data(self, bug):
        truth_data = []
        real_data = []
        truth_path = bug.get_truth_path()
        for index in range(len(truth_path)):
            ts = truth_path[index]['ts']
            position = truth_path[index]['position']
            if position != self.position:
                continue
            data_type = self._judge_inout_data_type(index, truth_path)
            if data_type:
                truth_data.append(
                    {'ts': ts, 'position': position, data_type: 1})
                seed = np.random.rand()
                if data_type == 'in' and seed < self.in_possibility:
                    real_data.append(
                        {'ts': ts, 'position': position, data_type: 1})
                if data_type == 'out' and seed < self.out_possibility:
                    real_data.append(
                        {'ts': ts, 'position': position, data_type: 1})
        return truth_data, real_data

    def _judge_inout_data_type(self, index, truth_path):
        if index == 0:
            return 'in'
        elif index == len(truth_path) - 1:
            return 'out'
        else:
            last_position = truth_path[index - 1]['position']
            current_position = truth_path[index]['position']
            next_position = truth_path[index + 1]['position']
            if self.arena[last_position][current_position]['district'] != \
                    self.arena[current_position][next_position]['district']:
                if self.arena[current_position][next_position]['district'] == \
                        self.in_district:
                    return 'in'
                else:
                    return 'out'
            else:
                return None
