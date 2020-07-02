import json

building_name = 'small-expo'

vertex = ['a', 'b', 'c', 'd', 'e', 'f']
edge_vertex = ['a', 'f']
# no cashier position
edges = [('a', 'b', {'district': 1, 'mean': 600, 'std': 300, 'min': 30,
                     'weight_add': 0}),
         ('a', 'c', {'district': 1, 'mean': 600, 'std': 300, 'min': 30,
                     'weight_add': 0}),
         ('b', 'c', {'district': 1, 'mean': 600, 'std': 300, 'min': 30,
                     'weight_add': 0}),
         ('b', 'd', {'district': 2, 'mean': 1200, 'std': 480, 'min': 60,
                     'weight_add': 0}),
         ('c', 'e', {'district': 4, 'mean': 300, 'std': 120, 'min': 15,
                     'weight_add': 0}),
         ('d', 'e', {'district': 3, 'mean': 900, 'std': 240, 'min': 45,
                     'weight_add': 0}),
         ('d', 'f', {'district': 3, 'mean': 900, 'std': 240, 'min': 45,
                     'weight_add': 0}),
         ('e', 'f', {'district': 3, 'mean': 900, 'std': 240, 'min': 45,
                     'weight_add': 0})]

edge_weight = {'usual': 3.0, 'likely': 0.5, 'unlikely': 0.1}
# should not have zero
district_weight_add_decay = [30, 15, 5, 2, 1]
assert 0 not in district_weight_add_decay

position_device_dict = [{'position': 'a', 'product': 'T', 'in_district': 1},
                        {'position': 'b', 'product': 'L', 'in_district': 2},
                        {'position': 'c', 'product': 'L', 'in_district': 4},
                        {'position': 'd', 'product': 'T', 'in_district': 3},
                        {'position': 'e', 'product': 'L', 'in_district': 3},
                        {'position': 'f', 'product': 'T', 'in_district': 3}]

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
guest_time_mean = 9000
guest_time_sigma = 3600
guest_time_min = 1800

if __name__ == '__main__':
    building_data = {'building_name': building_name,
                     'level_z': 1,
                     'atom_x': 2, 'atom_y': 2,
                     'lift': 0,
                     'escalator': 0,
                     'atom_mean': None,
                     'atom_std': None,
                     'atom_min': None,
                     'lift_escalator_mean': None,
                     'lift_escalator_std': None,
                     'lift_escalator_min': None,
                     'cashier_weight_add': None,
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
                     'districts': None,
                     'vertex': vertex,
                     'edge_vertex': edge_vertex,
                     'edges': edges,
                     'position_device_dict': position_device_dict}
    with open('./' + building_name + '.json', 'w') as c:
        c.writelines(json.dumps(building_data, indent=4))
