import argparse
import json
from random import choice

import tools.basic as basic
from entity.bug import Bug
import numpy as np

parser = argparse.ArgumentParser(description='simulate retail data')
parser.add_argument('--building_name', default='galaxy-tower-0', type=str,
                    help='building name with location information')
parser.add_argument('--date', default='2020-07-03', type=str,
                    help='building name with location information')
args = parser.parse_args()

# building = importlib.import_module('config.' + args.building_name)

with open('./config/' + args.building_name + '.json') as d:
    building_dict = json.load(d)


class Building(object):
    pass


building = Building()
for k in building_dict.keys():
    setattr(building, k, building_dict[k])

mean_daily_size = building.mean_daily_size
mean_vip_ratio = building.mean_vip_ratio
daily_size = max(0,
                 int(np.random.normal(mean_daily_size, 0.3 * mean_daily_size)))
vip_ratio = max(0.0001, np.random.normal(mean_vip_ratio, 0.3 * mean_vip_ratio))
am_size = int(daily_size * building.am_size_ratio)
pm_size = daily_size - am_size
vip_list = basic.get_uuid_list(building.vip_size)
staff_list = basic.get_uuid_list(building.staff_size)
guest_list = basic.get_uuid_list(building.guest_size)

arena = basic.make_arena(building.start_time, building.end_time,
                         building.last_in_time,
                         building.min_correct_alert_ratio,
                         building.max_missing_alert_ratio,
                         building.vertex, building.edges)
face_buckets = basic.get_face_buckets(arena, vip_list, staff_list,
                                      mean_vip_ratio,
                                      building.guest_time_mean)
product_list = basic.get_product_list(arena, face_buckets,
                                      building.position_device_dict)
mini_num = 0
multi_num = 0
for p in product_list:
    if p.product_name == 'Mini':
        mini_num += 1
    else:
        multi_num += 1
print('mini num:', mini_num)
print('multi num:', multi_num)
daily_guest_list, vip_num = basic.get_daily_guest_list(daily_size,
                                                       vip_ratio,
                                                       guest_list,
                                                       vip_list, staff_list)
in_time_data = basic.simulate_in_time_data(building.am_peak_time,
                                           building.am_sigma, am_size,
                                           building.pm_peak_time,
                                           building.pm_sigma, pm_size, arena)
time_currency_data = basic.simulate_time_currency_data(
    building.guest_time_mean,
    building.guest_time_sigma,
    building.guest_time_min,
    daily_size)

file_prefix = args.building_name + '_' + args.date + '_'
with open('./data/' + file_prefix + 'truth_path.json', 'w') as tp, \
        open('./data/' + file_prefix + 'truth_inout.json', 'w') as ti, \
        open('./data/' + file_prefix + 'real_inout.json', 'w') as ri, \
        open('./data/' + file_prefix + 'truth_recognition.json', 'w') as tr, \
        open('./data/' + file_prefix + 'real_recognition.json', 'w') as rr:
    for index in range(daily_size):
        b = Bug(daily_guest_list[index], time_currency_data[index],
                in_time_data[index], choice(building.edge_vertex),
                choice(building.edge_vertex), arena, building.edge_weight,
                building.district_weight_add_decay)
        b.ranger()
        bug_path_data = b.get_personal_path_data()
        tp.writelines(json.dumps(bug_path_data) + '\n')
        for p in product_list:
            t_inout_data, r_inout_data = p.get_inout_data(b)
            ti.writelines(json.dumps(t_inout_data) + '\n')
            ri.writelines(json.dumps(r_inout_data) + '\n')
            if p.product_name == 'Multi':
                t_recognition_data, r_recognition_data = \
                    p.get_recognition_data(b)
                tr.writelines(json.dumps(t_recognition_data) + '\n')
                rr.writelines(json.dumps(r_recognition_data) + '\n')
        tp.flush()
        ti.flush()
        ri.flush()
        tr.flush()
        rr.flush()

snapshot_num = 0
count_num = 0
for p in product_list:
    count_num += p.count_event_num
    if p.product_name == 'Multi':
        snapshot_num += p.snapshot_num
print("daily_size:", daily_size)
print("vip_num:", vip_num)
print("snapshot_num:", snapshot_num)
print("count_num:", count_num)
