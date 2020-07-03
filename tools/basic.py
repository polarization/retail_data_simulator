import uuid
from random import sample, shuffle

import networkx as nx
import numpy as np

from entity.face_bucket import FaceBucket
from product.landscape_view import Multi
from product.top_view import Mini


def make_arena(start_time, end_time, last_in_time, min_correct_alert_ratio,
               max_missing_alert_ratio, vertex, edges):
    G = nx.Graph(start_time=start_time, end_time=end_time,
                 last_in_time=last_in_time,
                 min_correct_alert_ratio=min_correct_alert_ratio,
                 max_missing_alert_ratio=max_missing_alert_ratio)
    G.add_nodes_from(vertex)
    G.add_edges_from(edges)
    nx.adjacency_matrix(G)
    print(nx.to_numpy_matrix(G))
    assert nx.algebraic_connectivity(G) > 0
    return G


def get_uuid_list(size):
    uuid_list = []
    for i in range(size):
        uuid_list.append(str(uuid.uuid4()))
    return uuid_list


def get_daily_guest_list(daily_size, vip_ratio, guest_list, vip_list,
                         staff_list):
    vip_guest = sample(vip_list, round(daily_size * vip_ratio))
    normal_guest = sample(guest_list,
                          int(daily_size - len(vip_guest) - len(staff_list)))
    daily_guest_list = normal_guest + vip_guest + staff_list
    shuffle(daily_guest_list)
    assert len(daily_guest_list) == daily_size
    return daily_guest_list, len(vip_guest)


def get_face_buckets(arena, vip_list, staff_list, vip_ratio, guest_time_mean):
    time_ratio = float(
        arena.graph['end_time'] - arena.graph['start_time']) / guest_time_mean
    staff_ratio = len(staff_list) * 1.0 / len(vip_list) * time_ratio
    vip_face_bucket = FaceBucket('vip', vip_list,
                                 './face_triple_data/triple_private.csv',
                                 vip_ratio, arena)
    staff_face_bucket = FaceBucket('staff', staff_list,
                                   './face_triple_data/triple_private.csv',
                                   staff_ratio, arena)
    return [vip_face_bucket, staff_face_bucket]


def get_product_list(arena, face_buckets, position_device_dict):
    product_list = []
    for m in position_device_dict:
        if m['product'] == 'T':
            product_list.append(Mini(arena, m['position'], m['in_district']))
        if m['product'] == 'L':
            product_list.append(
                Multi(arena, m['position'], m['in_district'], face_buckets))
    return product_list


def simulate_in_time_data(am_peak_timestamp, am_sigma,
                          am_in_num, pm_peak_timestamp,
                          pm_sigma, pm_in_num, arena):
    am_list = generate_time_array(am_peak_timestamp, am_sigma,
                                  am_in_num, arena)
    pm_list = generate_time_array(pm_peak_timestamp, pm_sigma,
                                  pm_in_num, arena)
    return am_list + pm_list


def generate_time_array(peak, sigma, size, arena):
    in_time_list = []
    while len(in_time_list) < size:
        seed = np.random.normal(peak, sigma)
        if arena.graph['start_time'] < seed < arena.graph['last_in_time']:
            in_time_list.append(int(seed))
    return in_time_list


def simulate_time_currency_data(peak, sigma, min_currency, size):
    time_currency_list = []
    while len(time_currency_list) < size:
        seed = np.random.normal(peak, sigma)
        if seed > min_currency:
            time_currency_list.append(int(seed))
    return time_currency_list
