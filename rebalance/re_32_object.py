from random import randint
from random import choice
import pandas as pd

def object(time_i, demand, zone, stations, zone_data, time):
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


    def rebalance_bikes(zone_data, demand_i, bikes):
        # zone_data： 原始区域数据表
        # demand_i： 当日的需求量表
        zone_data_i = zone_data.copy()
        zone_data_i = pd.merge(zone_data_i, demand_i[['zone', 'gap']], how='left', on='zone')
        zone_data_i['bikes'] = zone_data_i['bikes'] + zone_data_i['gap']
        re_zone = zone_data_i[(zone_data_i['bikes'] < 0) | (zone_data_i['bikes'] > zone_data_i['capacity'])]
        re_zone_list = list(re_zone['zone'])
        zone_list = list(zone_data['zone'])
        re_zone_list_i = [i for i in zone_list if i not in re_zone_list]
        zone_data_i = zone_data_i.set_index('zone')
        demand_i = demand_i.set_index('zone')
        re_zone = re_zone.set_index('zone')
        zone_data = zone_data.set_index('zone')
        for z_i in re_zone_list:
            z = re_zone.loc[z_i]
            out_in = 0
            if z['bikes'] > 0:
                re_bikes = z['bikes'] - z['capacity']
                for i in range(100):
                    re_zone_id = choice(re_zone_list_i)
                    if zone_data_i.loc[re_zone_id]['capacity'] - zone_data_i.loc[re_zone_id]['bikes'] > re_bikes:
                        zone_data.loc[re_zone_id, 'bikes'] += re_bikes
                        demand_i.loc[z_i, 'gap'] -= re_bikes
                        out_in = 1
                        bikes += re_bikes
                        break
            if z['bikes'] < 0:
                re_bikes = abs(z['bikes'])
                for i in range(100):
                    re_zone_id = choice(re_zone_list_i)
                    if zone_data_i.loc[re_zone_id]['bikes'] > re_bikes:
                        zone_data.loc[re_zone_id, 'bikes'] -= re_bikes
                        demand_i.loc[z_i, 'gap'] += re_bikes
                        out_in = 2
                        bikes += abs(re_bikes)
                        break
        return zone_data, demand_i.reset_index(), bikes


    zone_list = demand.drop(demand[demand[['zone']].duplicated()].index, axis=0)['zone']  # 区域列
    re_bikes = 0
    for day in range(time):
        day = day + 1
        day_demand = demand[demand['day'] == day]
        zone_data, day_demand, re_bikes = rebalance_bikes(zone_data, day_demand, re_bikes)
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
















