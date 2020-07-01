import csv


def calculate_lower_limit(triple_data, num_gallery,
                          ratio_gallery_imposter, min_correct_alert_ratio):
    fit_range_set = []
    for row in triple_data:
        pre_condition, target = calculate_rac(num_gallery,
                                              ratio_gallery_imposter, row)
        if target > min_correct_alert_ratio and pre_condition < 0.1:
            fit_range_set.append(row['th'])
    return fit_range_set


def calculate_rac(num_gallery, ratio_gallery_imposter, row):
    pre_condition = num_gallery * row['FPR']
    t = ratio_gallery_imposter * row['TPR']
    target = t * (1 - pre_condition / 2.0) / (
            pre_condition + t * (1 - pre_condition))
    return pre_condition, target


def calculate_upper_limit(triple_data, num_gallery, max_missing_alert_ratio):
    fit_range_set = []
    for row in triple_data:
        _, target = calculate_ram(num_gallery, row)
        if target < max_missing_alert_ratio:
            fit_range_set.append(row['th'])
    return fit_range_set


def calculate_ram(num_gallery, row):
    pre_condition = num_gallery * row['FPR']
    target = (1 - row['TPR']) * (1 - pre_condition)
    return pre_condition, target


def find_best_threshold(triple_data, available_range, num_gallery,
                        ratio_gallery_imposter):
    best_threshold = 0
    max_value = 0
    tpr = 0.0
    fpr = 0.0
    for row in triple_data:
        if row['th'] in available_range:
            _, rac = calculate_rac(num_gallery,
                                   ratio_gallery_imposter, row)
            _, ram = calculate_ram(num_gallery, row)
            r = 1 / (1 - rac) / ram
            if r > max_value:
                max_value = r
                best_threshold = row['th']
                tpr = row['TPR']
                fpr = row['FPR']
    pgc = 1 - num_gallery * fpr
    pvc = tpr * (1 - num_gallery * fpr / 2.0)
    pvw = (1 - tpr / 2.0) * num_gallery * fpr
    pvm = (1 - tpr) * (1 - num_gallery * fpr)
    return best_threshold, pgc, pvc, pvw, pvm


def get_phase_transition_point_by_threshold(triple_data, num_gallery,
                                            threshold):
    pgc, pvc, pvw, pvm = 0.0, 0.0, 0.0, 0.0
    for row in triple_data:
        if int(row['th']) == threshold:
            tpr = row['TPR']
            fpr = row['FPR']
            pgc = 1 - num_gallery * fpr
            pvc = tpr * (1 - num_gallery * fpr / 2.0)
            pvw = (1 - tpr / 2.0) * num_gallery * fpr
            pvm = (1 - tpr) * (1 - num_gallery * fpr)
    return threshold, pgc, pvc, pvw, pvm


def get_fr_phase_transition_point(triple_data_path, num_gallery,
                                  ratio_gallery_imposter,
                                  min_correct_alert_ratio,
                                  max_missing_alert_ratio,
                                  threshold=None):
    with open(triple_data_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=' ')
        triple_data = []
        for row in reader:
            triple_data.append({'FPR': float(row['FPR']),
                                'TPR': float(row['TPR']),
                                'th': row['th']})
        range_A = calculate_lower_limit(triple_data, num_gallery,
                                        ratio_gallery_imposter,
                                        min_correct_alert_ratio)
        range_B = calculate_upper_limit(triple_data, num_gallery,
                                        max_missing_alert_ratio)
        available_range = sorted(list(set(range_A).intersection(set(range_B))))
        if threshold is None:
            return find_best_threshold(triple_data,
                                       available_range,
                                       num_gallery,
                                       ratio_gallery_imposter)
        else:
            return get_phase_transition_point_by_threshold(triple_data,
                                                           num_gallery,
                                                           threshold)


if __name__ == '__main__':
    print(
        get_fr_phase_transition_point('../face_triple_data/triple_private.csv',
                                      1000, 0.001, 0.9, 0.1))
    for i in range(100):
        print(
            get_fr_phase_transition_point(
                '../face_triple_data/triple_private.csv',
                1000, 0.001, 0.9, 0.1, i))
