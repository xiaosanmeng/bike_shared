import pandas as pd
import numpy as np
from random import randint
from re_32_object import object
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


def main(demand, zone, stations, day, re_times):
    # 构建新站点
    new_zone = pd.DataFrame()
    new_stations_i = pd.DataFrame()
    zone_count_stations = zone.groupby(['zone'])['id'].count().reset_index().rename(columns={'id': 'count_stations'}) # 统计每个区域的站点数量

    # 设置每个区域新站点的容量（取平均）
    zone_capacity = pd.merge(stations, zone, how='left', on='id')
    zone_capacity = zone_capacity.groupby('zone')['capacity'].sum().reset_index()
    zone_capacity = pd.merge(zone_capacity, zone_count_stations, how='left', on='zone')
    zone_capacity['capacity'] = round(zone_capacity['capacity'] / zone_capacity['count_stations'])

    # 新站点构建
    new_zone['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index, axis=0)['zone']
    new_zone['id'] = new_zone['zone'].apply(lambda x: int(str(x)[::]))
    new_stations_i['id'] = new_zone['id']
    new_stations_i = pd.merge(new_stations_i, zone_capacity[['zone', 'capacity']],
                            how='left', left_on='id', right_on='zone')[['id', 'capacity']]

    # 选取新站点
    new_stations = new_stations_i.sample(50)
    stations_i = pd.concat([stations, new_stations])  # 加入新站点
    zone_i = pd.concat([new_zone, zone], sort=True)  # 加入新站点
    zone_count_stations = zone_i.groupby(['zone'])['id'].count().reset_index()  # 统计每个区域的站点数量
    zone_data_i = pd.merge(stations_i, zone_i, how='left', on='id')
    zone_data_i = zone_data_i.groupby('zone')['capacity'].sum().reset_index()
    zone_data_i['bikes'] = round(zone_data_i['capacity'] * 0.5)

    demand['gap'] = demand['end'] - demand['start']
    stations_i = stations_i.set_index('id')

    y1 = []
    y2 = []
    best_object = 1000000
    best_bikes = 1000000
    best_zone = pd.DataFrame()
    for time_i in range(re_times):
        re_bikes = object(time_i, demand_i, zone_i, stations_i, zone_data_i, day)
        random_num = randint(0, 100)
        t = False
        if best_object > re_bikes:
            best_object = re_bikes
            best_zone = zone_data_i.copy()
            t = True
        if t is False and random_num <= 10:
            zone_data_i['bikes'] = zone_data_i['capacity'].apply(lambda x: round(x * randint(0, 100) / 100))
        else:
            zone_data_i['bikes'] = best_zone['bikes'].apply(lambda x: round(x * randint(80, 120) / 100))
        print(time_i + 1, best_object)

        y1.append(re_bikes)
        y2.append(best_object)
    print(y1)
    return best_object, y1, y2







if __name__ == "__main__":
    start_time = time.time()
    re_bikes, y1, y2 = main(demand_i, zone_i, stations_i, 7, 1)
    end_time = time.time()
    print(re_bikes)
    print('用时：%s s' % round(end_time - start_time))
    print('再平衡,14day,原站点')

    # def DrawLinechart(y1, y2, title):
    #     x = range(len(y1))  # 生成0-10
    #     plt.plot(x, y1, c="R", label='common')
    #     plt.plot(x, y2, c='B', label='best')
    #     plt.legend(loc='upper left')  # 图例的位置是左上
    #     plt.xlabel('round')  # X轴标签
    #     plt.ylabel('re_bikes')  # Y轴标签
    #     plt.title(title)  # 折线图标题
    #     plt.show()
    #
    #
    # DrawLinechart(y1, y2, 're_bikes')
    # DrawLinechart(bikes_list, bikes_best_list, 'bikes')



# 再平衡 原站点 10day
#  0.5 500轮  （50, 2190）
#  0.5 2000轮 （1200, 2175.0）

# 0.5 31day  100轮
# 新站点 20267.0
# 老站点 24828.0

# 0.5 7day  100轮
# 新站点 760
# 老站点 2212.0

# 0.5 14day 100轮
# 新站点   4671
# 老站点 7807
# 0.5 14day 2000轮
# 新站点   （170  4641.0）
# 老站点 （7507   503.0）

# 40  832.0  50 741.0  60 610.0