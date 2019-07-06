import pandas as pd
import numpy as np
from random import randint
from object_new import object
import time

# 读取区域需求量
# demand_i = pd.read_csv('E:/python/shared_bikes/main_code/datas/zone_demands_day.csv')
demand_i = pd.read_csv('E:/python/shared_bikes/main_code/datas/zone_demands_day_new.csv')
# 读取区域包含的站点信息
zone_i = pd.read_csv('E:/python/shared_bikes/main_code/datas/station_datas.csv').rename(
    columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
# 读取站点信息
stations_i = pd.read_csv('E:/python/shared_bikes/main_code/datas/station_datas.csv')[['station_id', 'capacity']].\
    rename(columns={'station_id': 'id'})
### t = demand_i.groupby(['start', 'end']).count().reset_index()

def main(demand, zone, stations, day):
    # 构建新站点
    new_zone = pd.DataFrame()
    new_stations = pd.DataFrame()
    # 新站点构建
    # new_zone['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index, axis=0)['zone']
    # new_zone['id'] = new_zone['zone'].apply(lambda x: int(str(x)[::]))
    # new_stations['id'] = new_zone['id']
    # new_stations['capacity_up'] = 60
    # new_stations['capacity'] = 60
    # 新站点分割线
    object_list = []
    best_gap, best_start_demands, best_end_demands, best_bikes, best_capacity = 10000000, 0, 0, 10000000, 10000000
    best_object, best_stations = (), pd.DataFrame()
    new_stations_best = new_stations.copy()
    stations_i = pd.concat([stations, new_stations])  # 加入新站点
    zone_i = pd.concat([new_zone, zone], sort=True)  # 加入新站点
    zone_count_stations = zone_i.groupby(['zone'])['id'].count().reset_index()  # 统计每个区域的站点数量
    demand_i = demand
    # demand_i = pd.merge(demand, zone_count_stations, how='left', on='zone').rename(columns={'id': 'count_stations'})
    stations_i['bikes'] = round(stations_i['capacity'] * 0.5)  # 设置车子数量
    # stations_i['bikes'] = round(stations_i['capacity'] * 0.6)  # 设置车子数量
    # stations_i['bikes'] = stations_i['capacity'].apply(lambda x: x * randint(4, 7)/10)  # 设置车子数量
    # stations_i['bikes'] = stations_i['capacity'].apply(lambda x: round(x * randint(2, 9)/10))  # 设置车子数量
    stations_i = stations_i.set_index('id')
    for time_i in range(1):
        gap, start_demands, end_demands = object(time_i, demand_i, zone_i, stations_i, day)
        object_i = (gap, start_demands, end_demands)
        object_list.append(object_i)
        # new_stations['capacity'] = new_stations['capacity_up'].apply(lambda x: round(x * randint(40, 100) / 100))
        random_num = randint(0, 100)
        t = False
        if best_start_demands < start_demands or best_end_demands < end_demands:
            best_gap, best_start_demands, best_end_demands = gap, start_demands, end_demands
            best_object = object_i
            new_stations_best = stations_i.copy()
            t = True

        # if best_bikes > bikes and best_capacity > capacity:
        #     best_bikes, best_capacity = bikes, capacity
        #     best_object = object_i
        #     new_stations_best = new_stations.copy()
        #     t = True
        if t is False and random_num <= 10:
            stations_i['bikes'] = stations_i['capacity'].apply(lambda x: round(x * randint(0, 100) / 100))
        else:
            stations_i['bikes'] = new_stations_best['bikes'].apply(lambda x: round(x * randint(90, 110) / 100))
        print(best_object)
    # new_stations_best.to_csv('./best_stations.csv', index=None)
    return object_list

start_time = time.time()
z = main(demand_i, zone_i, stations_i, 14)
end_time = time.time()
print(z)
print('用时：%s s' % round(end_time - start_time))
print('新站点求可以满足的最大需求量')
# print('原站点求可以满足的最大需求量')



# 在容量固定的情况下，看可以满足的最大需求量

# 原站点 车子0.5  31day [(43564.0, 684084.0, 684964.0)]
# 新站点 上限60 车子0.5  [(60378.0, 899478.0, 900160.0)]

# 加入算法  31day
# 原站点 车子0.5
# 新站点 上限60 车子0.5



# 新站点 上限60 车子0.5 [(12438.0, 135112.0, 135162.0)] [(12400.0, 134913.0, 134963.0)] [(12419.0, 135075.0, 135102.0)]
# 原站点 车子0.5  5day [(11539.0, 128367.0, 128404.0)]




# 修改为最大满足需求量的目标函数

# 开始结束需求量分配比例一致
# 所有站点初始比例 0.5 / day5  12754.0 136985.0 136983.0/12776.0 136985.0 136983.0/12756.0 136985.0 136983.0/12746.0 136985.0 136983.0/12766.0 136985.0 136983.0
# 所有站点初始比例 0.6 / day5  12770.0 136985.0 136983.0/12764.0 136985.0 136983.0/12780.0 136985.0 136983.0/12764.0 136985.0 136983.0
# 所有站点初始比例 0.4-0.6 / day5  12750.0 136985.0 136983.0/12756.0 136985.0 136983.0/12760.0 136985.0 136983.0/12764.0 136985.0 136983.0
# 所有站点初始比例 0.2-0.8 / day5  12770.0 136985.0 136983.0/12770.0 136985.0 136983.0/12633.0 136723.0 136588.0/12762.0 136985.0 136983.0

# 原站点 初始比例 0.5 / day5  11820.0 130692.0 130586.0/11806.0 130692.0 130586.0/11808.0 130692.0 130586.0/11816.0 130692.0 130586.0/11788.0 130692.0 130586.0/11810.0 130692.0 130586.0
# 原站点 初始比例 0.6 / day5  11822.0 130692.0 130586.0/11806.0 130692.0 130586.0/11808.0 130692.0 130586.0/11804.0 130692.0 130586.0
# 所有站点初始比例 0.4-0.6 / day5  11808.0 130692.0 130586.0/11812.0 130692.0 130586.0/11814.0 130692.0 130586.0






#  开始结束需求量分配比例不同
# 所有站点初始比例 0.5 / day5  40670.0 114765.0 114851.0/42953.0 113712.0 113813.0/41784.0 115108.0 115020.0/40687.0 111665.0 111634.0/39514.0 110371.0 110331.0


# 原站点/初始车子比例 0.5/不断改变需求量无法分配的站点初始比例/day1  2554.0 30228.0 30228.0 / 2564.0 30228.0 30228.0 / 2556.0 30228.0 30228.0
# 原站点/初始车子比例 0.5/不断改变需求量无法分配的站点初始比例/day1-2  4569.0 48228.0 48227.0 / 4577.0 48228.0 48227.0/4575.0 48228.0 48227.0
