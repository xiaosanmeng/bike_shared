import pandas as pd
import numpy as np
from random import randint
from re_4_object import object, set_bikes, aaa
import time
import matplotlib.pyplot as plt
import random


def main(demand, zone, stations, distance, day, re_times, stations_type, new_stations_num):
    # 构建新站点
    new_zone = pd.DataFrame()
    new_stations_i = pd.DataFrame()
    new_stations = pd.DataFrame()
    zone_count_stations = zone.groupby(['zone'])['id'].count().reset_index().rename(columns={'id': 'count_stations'}) # 统计每个区域的站点数量

    # 设置每个区域新站点的容量（取平均）
    zone_capacity = pd.merge(stations, zone, how='left', on='id')
    zone_capacity = zone_capacity.groupby('zone')['capacity'].sum().reset_index()
    zone_capacity = pd.merge(zone_capacity, zone_count_stations, how='left', on='zone')
    # zone_capacity['capacity'] = 60
    zone_capacity['capacity'] = round(zone_capacity['capacity'] / zone_capacity['count_stations'])
    demand['gap'] = demand['end'] - demand['start']

    # 新站点构建
    new_zone['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index, axis=0)['zone']
    new_zone['id'] = new_zone['zone'].apply(lambda x: int(str(x)[::]))
    new_stations_i['id'] = new_zone['id']
    new_stations_i = pd.merge(new_stations_i, zone_capacity[['zone', 'capacity']],
                            how='left', left_on='id', right_on='zone')[['id', 'capacity']]
    # 选取新站点
    best_object_sum = 10000000
    best_object = 1000000
    object_list = []
    best_bikes = None
    #

    y1 = []
    y2 = []
    if stations_type == 0:
        re_times = 1
    c = [stations_type] * new_stations_num + [0] * (379 - new_stations_num)  # 控制新站点
    for j in range(re_times):
        random.shuffle(c)
        new_stations_i['t'] = c
        new_stations = new_stations_i[new_stations_i['t'] == 1][['id', 'capacity']]
        stations_i = pd.concat([stations, new_stations])  # 加入新站点
        zone_i = pd.concat([new_zone, zone], sort=True)  # 加入新站点
        zone_data_i = pd.merge(stations_i, zone_i, how='left', on='id')
        zone_data_i = zone_data_i.groupby('zone')['capacity'].sum().reset_index()
        zone_data_i['bikes'] = round(zone_data_i['capacity'] * 0.5)
        zone_data_i = set_bikes(demand, zone_data_i)
        stations_i = stations_i.set_index('id')

    #  确定车子数量分割线
    #     best_zone = pd.DataFrame()
    #     re_bikes = object(1, demand, zone_i, stations_i, zone_data_i.copy(), distance, day)
    #     if best_object >= re_bikes:
    #         best_object = re_bikes
    #         best_bikes = zone_data_i
    #     y1.append(re_bikes)
    #     y2.append(best_object)
    #     print(j + 1, best_object)
    # return best_object, y1, y2

        y1 = []
        y2 = []


        best_object = 1000000
        best_zone = pd.DataFrame()
        for time_i in range(500):
            zone_data_i['bikes'] = zone_data_i.apply(aaa, axis=1)  # 限制车子数量在容量范围内
            re_bikes = object(time_i, demand, zone_i, stations_i, zone_data_i.copy(), distance, day)
            t = False
            if best_object >= re_bikes:
                best_object = re_bikes
                best_zone = zone_data_i.copy()
                t = True
            if t is False and np.random.rand() <= 0.1:
                zone_data_i['bikes'] = zone_data_i['capacity'].apply(lambda x: round(x * randint(0, 100) / 100))
            else:
                zone_data_i['bikes'] = best_zone['bikes'].apply(lambda x: round(x * randint(80, 120) / 100))
            print(j+1, time_i + 1, best_object)

            # y1.append(re_bikes)
            # y2.append(best_object)
        if best_object_sum > best_object:
            best_object_sum = best_object
            best_bikes = best_zone

        y1.append(best_object)
        y2.append(best_object_sum)

    print(best_object_sum, y1)
    best_bikes.to_csv('F:/bikedata/bike_datas/output/output.csv', index=None)
    return best_object_sum, y1, y2

if __name__ == "__main__":
    # 读取区域需求量
    demand_i = pd.read_csv('F:/bikedata/bike_datas/test/zone_day.csv')
    # 读取区域包含的站点信息
    zone_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
        columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
    # 读取站点信息
    stations_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv')[['station_id', 'capacity']]. \
        rename(columns={'station_id': 'id'})
    distance = pd.read_csv('F:/bikedata/bike_datas/zones_distance_matrix.csv')
    distance = distance.set_index('Unnamed: 0')

    start_time = time.time()
    stations_type = 0  # 0-原站点  1-加入新站点
    new_stations = 120  # 构建的新站点个数
    days = 7
    re_bikes, y1, y2 = main(demand_i, zone_i, stations_i, distance, days, 100, stations_type, new_stations)
    end_time = time.time()
    print(re_bikes)
    print('用时：%s s' % round(end_time - start_time))
    if stations_type == 0:
        print('原站点')
    else:
        print('构建%s个新站点' % new_stations)

    def DrawLinechart(y1, y2, title):
        x = range(len(y1))  # 生成0-10
        plt.plot(x, y1, c="R", label='common')
        plt.plot(x, y2, c='B', label='best')
        plt.legend(loc='upper left')  # 图例的位置是左上
        plt.xlabel('round')  # X轴标签
        plt.ylabel('re_bikes')  # Y轴标签
        plt.title(title)  # 折线图标题
        plt.show()


    DrawLinechart(y1, y2, 're_bikes')
    # DrawLinechart(y1, bikes_best_list, 'bikes')

