import json
from random import choice

import numpy as np

# shopping mall config
building_name = 'galaxy-tower-0'
level_z = 4
atom_x, atom_y = 5, 3
lift = [(1, 0), (3, 0), (1, 2), (3, 2)]
escalator = [(1, 1), (3, 1)]
atom_mean = 120
atom_std = 480
atom_min = 30
lift_escalator_mean = 10
lift_escalator_std = 0
lift_escalator_min = 10
cashier_weight_add = 3

# common config
edge_weight = {'usual': 3.0, 'likely': 0.5, 'unlikely': 0.1}
# should not have zero
district_weight_add_decay = [30, 15, 5, 2, 1]
assert 0 not in district_weight_add_decay
daily_size = 30000
am_size = 9000
am_peak_time = 3600 * 12
am_sigma = 2700
pm_peak_time = 3600 * 18
pm_sigma = 5400
vip_size = 1000
staff_size = 30
guest_size = 1000000
start_time = 3600 * 10
end_time = 3600 * 22
last_in_time = 3600 * 21.5
min_correct_alert_ratio = 0.9
max_missing_alert_ratio = 0.1
vip_ratio = 0.001
guest_time_mean = 10800
guest_time_sigma = 3600
guest_time_min = 1800

# core data structure
districts = {}
vertex = []
edge_vertex = []
edges = []
position_device_dict = []


def is_entrance(x, y, z):
    if (z is not 0) or ((x not in [0, atom_x - 1]) and (
            y not in [0, atom_y - 1])):
        return False
    else:
        return True


def choose_product(position_name):
    if position_name.find('inner') >= 0:
        return 'L'
    if position_name.find('lift') >= 0:
        return 'T'
    if position_name.find('escalator') >= 0:
        return 'T'
    seed = np.random.random()
    if seed <= 0.5:
        return 'T'
    else:
        return 'L'


def choose_in_district(position_name, districts_dict):
    candidate = []
    for d in districts_dict.keys():
        for v in districts_dict[d]:
            if v == position_name:
                candidate.append(d)
    return choice(candidate)


# init districts dict
for z in range(level_z):
    for x in range(atom_x):
        for y in range(atom_y):
            d_name = "atom-%s-%s-%s" % (z, x, y)
            districts[d_name] = []
for j in range(len(lift)):
    districts["lift-%s-%s" % (lift[j][0], lift[j][1])] = []
for k in range(len(escalator)):
    for z in range(level_z - 1):
        d_name = "escalator-%s-%s-level-%s->%s" % (
            escalator[k][0], escalator[k][1], z, z + 1)
        districts[d_name] = []

# init atom district connection position
for z in range(level_z):
    for x in range(atom_x):
        for y in range(atom_y):
            d_name = "atom-%s-%s-%s" % (z, x, y)
            if is_entrance(x, y, z):
                v_name = "out->atom-%s-%s-%s" % (z, x, y)
                vertex.append(v_name)
                edge_vertex.append(v_name)
                districts[d_name].append(v_name)
            if x + 1 < atom_x:
                dx = "atom-%s-%s-%s" % (z, x + 1, y)
                v_name = d_name + "->" + dx
                vertex.append(v_name)
                districts[d_name].append(v_name)
                districts[dx].append(v_name)
            if y + 1 < atom_y:
                dy = "atom-%s-%s-%s" % (z, x, y + 1)
                v_name = d_name + "->" + dy
                vertex.append(v_name)
                districts[d_name].append(v_name)
                districts[dy].append(v_name)

# init atom district inner position
for z in range(level_z):
    for x in range(atom_x):
        for y in range(atom_y):
            d_name = "atom-%s-%s-%s" % (z, x, y)
            seed = max(int(np.random.normal(1.0, 1.0)), 0)
            for i in range(seed):
                v_name = d_name + "-inner-%s" % i
                vertex.append(v_name)
                districts[d_name].append(v_name)

# init lift position
for x in range(atom_x):
    for y in range(atom_y):
        if (x, y) in lift:
            d_name = "lift-%s-%s" % (x, y)
            for z in range(level_z):
                atom_d_name = "atom-%s-%s-%s" % (z, x, y)
                v_name = d_name + "-level-%s" % z
                vertex.append(v_name)
                districts[d_name].append(v_name)
                districts[atom_d_name].append(v_name)

# init escalator position
for x in range(atom_x):
    for y in range(atom_y):
        if (x, y) in escalator:
            for z in range(level_z - 1):
                d_name = "escalator-%s-%s-level-%s->%s" % (x, y, z, z + 1)
                down_atom_d_name = "atom-%s-%s-%s" % (z, x, y)
                up_atom_d_name = "atom-%s-%s-%s" % (z + 1, x, y)
                down_v_name = d_name + "-down"
                up_v_name = d_name + "-up"
                vertex.append(down_v_name)
                vertex.append(up_v_name)
                districts[d_name].append(down_v_name)
                districts[d_name].append(up_v_name)
                districts[down_atom_d_name].append(down_v_name)
                districts[up_atom_d_name].append(up_v_name)

# init edges
for d in districts.keys():
    if d.startswith("escalator"):
        vs = districts[d]
    for v1 in districts[d]:
        for v2 in districts[d]:
            if v1 != v2:
                if d.startswith("atom"):
                    edges.append((v1, v2,
                                  {'district': d, 'mean': atom_mean,
                                   'std': atom_std, 'min': atom_min,
                                   'weight_add': 0}))
                else:
                    edges.append((v1, v2,
                                  {'district': d, 'mean': lift_escalator_mean,
                                   'std': lift_escalator_std,
                                   'min': lift_escalator_min,
                                   'weight_add': 0}))

# init position device dict
for v_name in vertex:
    position_device_dict.append(
        {'position': v_name, 'product': choose_product(v_name), 'in_district':
            choose_in_district(v_name, districts)})

if __name__ == '__main__':
    print("=====================district=========================")
    print("district num:", len(districts.keys()))
    assert len(districts.keys()) == level_z * atom_x * atom_y + len(
        lift) + len(
        escalator) * (level_z - 1)
    for d_name in districts.keys():
        print(d_name)
    print("=====================vertex=========================")
    print("position num:", len(vertex))
    for v_name in vertex:
        print(v_name)
    print("=====================edges=========================")
    print("edge num:", len(edges) / 2)
    for e in edges:
        print(e)
    print("=====================product=========================")
    mini_num = 0
    multi_num = 0
    for p in position_device_dict:
        print(p)
        if p['product'] == 'T':
            mini_num += 1
        else:
            multi_num += 1
    print('mini num:', mini_num)
    print('multi num:', multi_num)
    building_data = {'building_name': building_name,
                     'level_z': level_z,
                     'atom_x': atom_x, 'atom_y': atom_y,
                     'lift': lift,
                     'escalator': escalator,
                     'atom_mean': atom_mean,
                     'atom_std': atom_std,
                     'atom_min': atom_min,
                     'lift_escalator_mean': lift_escalator_mean,
                     'lift_escalator_std': lift_escalator_std,
                     'lift_escalator_min': lift_escalator_min,
                     'cashier_weight_add': cashier_weight_add,
                     'edge_weight': edge_weight,
                     'district_weight_add_decay': district_weight_add_decay,
                     'daily_size': daily_size,
                     'am_size': am_size,
                     'am_peak_time': am_peak_time,
                     'am_sigma': am_sigma,
                     'pm_peak_time': pm_peak_time,
                     'pm_sigma': pm_sigma,
                     'vip_size': vip_size,
                     'staff_size': staff_size,
                     'guest_size': guest_size,
                     'start_time': start_time,
                     'end_time': end_time,
                     'last_in_time': last_in_time,
                     'min_correct_alert_ratio': min_correct_alert_ratio,
                     'max_missing_alert_ratio': max_missing_alert_ratio,
                     'vip_ratio': vip_ratio,
                     'guest_time_mean': guest_time_mean,
                     'guest_time_sigma': guest_time_sigma,
                     'guest_time_min': guest_time_min,
                     'districts': districts,
                     'vertex': vertex,
                     'edge_vertex': edge_vertex,
                     'edges': edges,
                     'position_device_dict': position_device_dict}
    with open('./' + building_name + '.json', 'w') as c:
        c.writelines(json.dumps(building_data, indent=4))
