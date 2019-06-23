import pandas as pd
import numpy as np
from random import randint
from object_per_station import object
import time
import matplotlib.pyplot as plt


# 读取区域需求量
demand_i = pd.read_csv('F:/bikedata/bike_datas/test/zone_day.csv')
# 读取区域包含的站点信息
zone_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
    columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
# 读取站点信息
stations_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv')[['station_id', 'capacity']].\
    rename(columns={'station_id': 'id'})
# demand_i['start'] = round(demand_i['start'] * 0.5)
# demand_i['end'] = round(demand_i['end'] * 0.5)


def main(demand, zone, stations, day):
    # 构建新站点
    new_zone = pd.DataFrame()
    new_zone['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index, axis=0)['zone']
    new_zone['id'] = new_zone['zone'].apply(lambda x: int(str(x)[::]))
    new_stations = new_zone[['id']]
    object_list, bikes_list, capacity_list, bikes_best_list, capacity_best_list = [], [], [], [], []
    new_stations['capacity_up'] = 80
    new_stations['capacity'] = 80
    best_gap, best_start_demands, best_end_demands, best_bikes, best_capacity = 10000000, 0, 0, 10000000, 10000000
    best_object = ()
    new_stations_best = new_stations.copy()
    for time_i in range(100):
        # 加入新站点
        stations_i = pd.concat([stations, new_stations])  # 加入新站点
        zone_i = pd.concat([new_zone, zone], sort=True)  # 加入新站点
        zone_count_stations = zone_i.groupby(['zone'])['id'].count().reset_index()  # 统计每个区域的站点数量
        demand_i = pd.merge(demand, zone_count_stations, how='left', on='zone').rename(columns={'id': 'count_stations'})
        stations_i['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
        # stations['bikes'] = round(stations['capacity'] * 0.6)  # 设置车子数量
        # stations['bikes'] = stations['capacity'].apply(lambda x: x * randint(4, 7)/10)  # 设置车子数量
        # stations['bikes'] = stations['capacity'].apply(lambda x: round(x * randint(2, 9)/10))  # 设置车子数量
        stations_i = stations_i.set_index('id')
        gap, start_demands, end_demands, bikes = object(time_i, demand_i, zone_i, stations_i, day)
        capacity = stations_i['capacity'].sum()
        object_i = (gap, start_demands, end_demands, bikes, capacity)
        object_list.append(object_i)

        random_num = randint(0, 100)
        t = False
        # if best_gap > gap and best_start_demands < start_demands and best_end_demands < end_demands:
        #     best_gap, best_start_demands, best_end_demands = gap, start_demands, end_demands
        #     best_object = object_i
        #     new_stations_best = new_stations.copy()

        if best_bikes > bikes and best_capacity > capacity:
            best_bikes, best_capacity = bikes, capacity
            best_object = object_i
            new_stations_best = new_stations.copy()
            t = True
        if t is False and random_num < 10:
            new_stations['capacity'] = new_stations_best['capacity_up'].apply(lambda x: round(x * randint(70, 100) / 100))
        else:
            new_stations['capacity'] = new_stations_best['capacity'].apply(lambda x: round(x * randint(80, 100) / 100))

        bikes_list.append(bikes)
        capacity_list.append(capacity)
        bikes_best_list.append(best_bikes)
        capacity_best_list.append(best_capacity)
    print(best_object)
    return object_list, bikes_list, capacity_list, bikes_best_list, capacity_best_list


start_time = time.time()
object_list, bikes_list, capacity_list, bikes_best_list, capacity_best_list = main(demand_i, zone_i, stations_i, 5)
end_time = time.time()
print(object_list)
print('用时：%s s' % round(end_time - start_time))


def DrawLinechart(y1, y2, title):
    x = range(len(y1))  # 生成0-10
    plt.plot(x, y1, c="R", label='common')
    plt.plot(x, y2, c='B', label='best')
    plt.legend(loc = 'upper left')#图例的位置是左上
    plt.xlabel('round')#X轴标签
    plt.ylabel('value')#Y轴标签
    plt.title(title)#折线图标题

    plt.show()
# DrawLinechart(bikes_list, bikes_best_list, 'bikes')
DrawLinechart(capacity_list, capacity_best_list, 'capacity')

# 容量0.4-1[(12780.0, 136985.0, 136983.0), (12548.0, 136457.0, 136403.0), (12526.0, 136457.0, 136403.0), (12631.0, 136723.0, 136588.0), (12568.0, 136457.0, 136403.0), (12536.0, 136457.0, 136403.0), (12659.0, 136719.0, 136798.0), (12556.0, 136457.0, 136403.0), (12554.0, 136457.0, 136403.0), (12637.0, 136723.0, 136588.0), (12649.0, 136723.0, 136588.0), (12635.0, 136723.0, 136588.0), (12615.0, 136723.0, 136588.0), (12544.0, 136457.0, 136403.0), (12536.0, 136457.0, 136403.0), (12635.0, 136723.0, 136588.0), (12532.0, 136457.0, 136403.0), (12568.0, 136457.0, 136403.0), (12552.0, 136457.0, 136403.0), (12544.0, 136457.0, 136403.0)]

# 增加站点容量和车子数量的目标函数

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
