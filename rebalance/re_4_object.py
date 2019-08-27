from random import randint
from random import choice
import pandas as pd

def object(time_i, demand, zone, stations, zone_data, distance, time):
    # def random_start(length, demands_i, rate, len_rate):
    #     points = [randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
    #     points = [0] + sorted(points) + [100]  # 排个队
    #     points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
    #     start_demand = round(demands_i['start'][0] * (1 - rate / len_rate))
    #     start = [round(points[i] * start_demand) for i in range(length - 1)]
    #     start.append(start_demand - sum(start))
    #     return start
    #
    # def random_end(length, demands_i, rate, len_rate):
    #     points = [randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
    #     points = [0] + sorted(points) + [100]  # 排个队
    #     points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
    #     end_demand = round(demands_i['end'][0] * (1 - rate / len_rate))
    #     end = [round(points[i] * end_demand) for i in range(length - 1)]
    #     end.append(end_demand - sum(end))
    #     return end
    # def random_start(length, demands_i, rate, len_rate):
    #     points = [randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
    #     points = [0] + sorted(points) + [100]  # 排个队
    #     points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
    #     start_demand = round(demands_i['start'][0] * (1 - rate/len_rate))
    #     end_demand = round(demands_i['end'][0] * (1 - rate/len_rate))
    #     start = [round(points[i] * start_demand) for i in range(length - 1)]
    #     end = [round(points[i] * end_demand) for i in range(length - 1)]
    #     start.append(start_demand - sum(start))
    #     end.append(end_demand - sum(end))
    #     return start, end
    #
    # def station_init_bikes(reset_bikes, data, list, capacity_i):
    #     # data.loc[list, 'bikes'] = round(capacity_i * ((reset_bikes+1) / 20))  # 所有站点比例一致
    #     data.loc[list, 'bikes'] = round(capacity_i * randint(0, 100) / 100)  # 所有站点比例一致
    #     # data.loc[list, 'bikes'] = capacity_i.apply(lambda x: round(x * randint(0, 100) / 100))  # 站点比例不一致
    #     return data




    # stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量


    def rebalance_bikes(zone_data, demand_i, bikes, distance):
        # zone_data： 原始区域数据表
        # demand： 当日的需求量表
        zone_data_i = zone_data.copy()
        zone_data_i = pd.merge(zone_data_i, demand_i[['zone', 'gap']], how='left', on='zone')
        zone_data_i = zone_data_i.fillna(0)
        zone_data_i['bikes'] = zone_data_i['bikes'] + zone_data_i['gap']
        re_zone_out = zone_data_i[(zone_data_i['bikes'] > zone_data_i['capacity'])]
        re_zone_out['re_bikes'] = re_zone_out['bikes'] - re_zone_out['capacity']
        re_zone_in = zone_data_i[(zone_data_i['bikes'] < 0)]
        re_zone_in['re_bikes'] = re_zone_in['bikes']
        re_zone_in_list = list(re_zone_in['zone'])
        re_zone_out_list = list(re_zone_out['zone'])
        re_zone_out = re_zone_out.set_index('zone')
        re_zone_in = re_zone_in.set_index('zone')
        zone_data = zone_data.set_index('zone')
        zone_data_i = zone_data_i.set_index('zone')

        if re_zone_in_list is None and re_zone_out_list is None:
            return zone_data,  bikes

        distance_list = {}
        for i in re_zone_in_list:
            distance_list[i] = {}
            for j in re_zone_out_list:
                distance_list[i][j] = round(distance.loc[i, '%s' % j], 1)
        for i in re_zone_in_list:
            out_list = sorted(distance_list[i].items(), key=lambda d: d[1])
            for j in out_list:
                if j[1] > 5000:
                    continue
                else:
                    if re_zone_out.loc[j[0], 're_bikes'] <= abs(re_zone_in.loc[i, 're_bikes']):
                        re_bikes = re_zone_out.loc[j[0], 're_bikes']
                        zone_data.loc[i, 'bikes'] += re_bikes
                        zone_data.loc[j[0], 'bikes'] -= re_bikes
                        re_zone_in.loc[i, 're_bikes'] += re_bikes
                        re_zone_out.loc[j[0], 're_bikes'] -= re_bikes
                        bikes += re_bikes
                    else:
                        re_bikes = abs(re_zone_in.loc[i, 're_bikes'])
                        zone_data.loc[i, 'bikes'] += re_bikes
                        zone_data.loc[j[0], 'bikes'] -= re_bikes
                        re_zone_in.loc[i, 're_bikes'] += re_bikes
                        re_zone_out.loc[j[0], 're_bikes'] -= re_bikes
                        bikes += re_bikes
                        break
            if re_zone_in.loc[i, 're_bikes'] < 0:
                # re_bikes = z['bikes'] - z['capacity']
                distance_i = (distance.loc[i]).sort_values().drop(['%s' % i], axis=0).reset_index()
                distance_i.columns = ['id', 'distance']
                distance_i = distance_i[distance_i['distance'] <= 5000]
                for index, row in distance_i.iterrows():
                    re_zone_id = int(row['id'])
                    re_bikes = abs(re_zone_in.loc[i, 're_bikes'])
                    re_bikes_i = zone_data.loc[re_zone_id]['bikes']
                    if re_bikes_i <= re_bikes:
                        zone_data.loc[i, 'bikes'] += re_bikes_i
                        zone_data.loc[re_zone_id, 'bikes'] -= re_bikes_i
                        re_zone_in.loc[i, 're_bikes'] += re_bikes_i
                        bikes += re_bikes_i
                    else:
                        zone_data.loc[i, 'bikes'] += re_bikes
                        zone_data.loc[re_zone_id, 'bikes'] -= re_bikes
                        re_zone_in.loc[i, 're_bikes'] += re_bikes
                        bikes += re_bikes
                        break

        for i in re_zone_out_list:
            if re_zone_out.loc[i, 're_bikes'] <=0:
                continue
            else:
                distance_i = (distance.loc[i]).sort_values().drop(['%s' % i], axis=0).reset_index()
                distance_i.columns = ['id', 'distance']
                distance_i = distance_i[distance_i['distance'] <= 5000]
                for index, row in distance_i.iterrows():
                    re_zone_id = int(row['id'])
                    re_bikes = abs(re_zone_out.loc[i, 're_bikes'])
                    re_bikes_i = zone_data.loc[re_zone_id, 'capacity'] - zone_data.loc[re_zone_id, 'bikes']
                    if re_bikes_i <= re_bikes:
                        zone_data.loc[i, 'bikes'] -= re_bikes_i
                        zone_data.loc[re_zone_id, 'bikes'] += re_bikes_i
                        re_zone_out.loc[i, 're_bikes'] -= re_bikes_i
                        bikes += re_bikes_i
                    else:
                        zone_data.loc[i, 'bikes'] -= re_bikes
                        zone_data.loc[re_zone_id, 'bikes'] += re_bikes
                        re_zone_out.loc[i, 're_bikes'] -= re_bikes
                        bikes += re_bikes
                        break

        return zone_data,  bikes


    zone_list = demand.drop(demand[demand[['zone']].duplicated()].index, axis=0)['zone']  # 区域列
    re_bikes = 0
    for day in range(time):
        day = day + 1
        day_demand = demand[demand['day'] == day]
        zone_data, re_bikes = rebalance_bikes(zone_data, day_demand, re_bikes, distance)
        zone_data = pd.merge(zone_data, day_demand[['zone', 'gap']], how='left', on='zone')
        zone_data['bikes'] = zone_data['bikes'] + zone_data['gap']
        del zone_data['gap']
        print('day:', day, 're_bikes:', re_bikes)
    return re_bikes


        # day_demand_i['gap_sum'] = day_demand_i['gap_sum'] + day_demand_i['gap']
        # day_demand_i.gap_down[day_demand_i.gap_sum < 0] = 0 - day_demand_i.gap_sum
        # day_demand_i.gap_up[day_demand_i.gap_sum > 0] = 0 + day_demand_i.gap_sum
        # day_demand_i.judge[day_demand_i.gap_up - day_demand_i.gap_down <= day_demand_i.capacity] = 1
        # if day_demand.judge.sum != len(zone_list):
        #     re_zone_list = day_demand[day_demand['judge'] == 0]['zone']
        #     for index, z in enumerate(re_zone_list):
        #         re_bikes = z['capacity'] - (z[''])



def set_bikes(demand, zone_data):
    day = 1
    day_demand = demand[demand['day'] == day]
    # zone_data, re_bikes = rebalance_bikes(zone_data, day_demand, re_bikes, distance)
    zone_data = pd.merge(zone_data, day_demand[['zone', 'gap']], how='left', on='zone')
    zone_data = zone_data.fillna(0)
    zone_data['bikes'] = zone_data['bikes'] - zone_data['gap']
    zone_data['bikes'] = zone_data.apply(aaa, axis=1)
    del zone_data['gap']
    return zone_data

def aaa(t):
    if t['bikes'] < 0:
        t['bikes'] = 0
    if t['bikes'] > t['capacity']:
        t['bikes'] = t['capacity']
    return t['bikes']














