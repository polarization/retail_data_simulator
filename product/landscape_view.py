from random import choice

import numpy as np

from product.base_count import BaseCount


class Multi(BaseCount):

    def __init__(self, arena, position, in_district,
                 face_buckets=None, in_possibility=0.98,
                 out_possibility=0.95, face_possibility=0.9):
        super(Multi, self).__init__(arena, position, in_district,
                                    in_possibility, out_possibility)
        self.product_name = 'Multi'
        self.face_possibility = face_possibility
        self.face_buckets = face_buckets
        self.snapshot_num = 0

    def get_recognition_data(self, bug):
        truth_data = []
        real_data = []
        truth_path = bug.get_truth_path()
        for index in range(len(truth_path)):
            truth_hits = []
            real_hits = []
            ts = truth_path[index]['ts']
            position = truth_path[index]['position']
            if position != self.position:
                continue
            if self._judge_face_emerge(index, truth_path):
                for bucket in self.face_buckets:
                    if bug.bug_id in bucket.id_list:
                        truth_hits.append({'bucket_name': bucket.name,
                                           'face_id': bug.bug_id})
                if truth_hits:
                    truth_data.append(
                        {'ts': ts, 'position': position, 'bug_id': bug.bug_id,
                         'hits': truth_hits})
                seed = np.random.rand()
                if seed < self.face_possibility:
                    self.snapshot_num += 1
                    for bucket in self.face_buckets:
                        if bug.bug_id in bucket.id_list:
                            face_seed = np.random.rand()
                            if face_seed < bucket.pvc:
                                real_hits.append({'bucket_name': bucket.name,
                                                  'face_id': bug.bug_id})
                            elif face_seed < 1 - bucket.pvm:
                                real_hits.append({'bucket_name': bucket.name,
                                                  'face_id': choice(
                                                      bucket.id_list)})
                        else:
                            if np.random.rand() > bucket.pgc:
                                real_hits.append({'bucket_name': bucket.name,
                                                  'face_id': choice(
                                                      bucket.id_list)})
                    if real_hits:
                        real_data.append(
                            {'ts': ts, 'position': position,
                             'bug_id': bug.bug_id,
                             'hits': real_hits})
        return truth_data, real_data

    def _judge_face_emerge(self, index, truth_path):
        if index is not 0:
            last_position = truth_path[index - 1]['position']
            current_position = truth_path[index]['position']
            if self.arena[last_position][current_position]['district'] == \
                    self.in_district:
                return False
            else:
                return True
        else:
            return True
