from tools.face_recognition import get_fr_phase_transition_point


class FaceBucket(object):

    def __init__(self, name, id_list, triple_data_path, ratio_gallery_imposter,
                 arena, threshold=None):
        super(FaceBucket, self).__init__()
        self.name = name
        self.id_list = id_list
        self.algorithm = triple_data_path
        self.ratio_gallery_imposter = ratio_gallery_imposter
        self.threshold = threshold
        self.arena = arena
        self.threshold, self.pgc, self.pvc, self.pvw, self.pvm = \
            get_fr_phase_transition_point(
                self.algorithm, len(self.id_list),
                self.ratio_gallery_imposter,
                self.arena.graph[
                    'min_correct_alert_ratio'],
                self.arena.graph[
                    'max_missing_alert_ratio'],
                self.threshold)
