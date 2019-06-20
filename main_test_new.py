import pandas as pd
import numpy as np
from random import randint
from object_test_new import object

#  加入新站点寻求可行解的目标函数

# 读取区域需求量
demand_i = pd.read_csv('F:/bikedata/bike_datas/test/zone_day.csv')
# 读取区域包含的站点信息
zone_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
    columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
# 读取站点信息
stations_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv')[['station_id', 'capacity']].\
    rename(columns={'station_id': 'id'})
stations_i['bikes'] = round(stations_i['capacity'] * 0.5)

def main(demand, zone, old_stations, days):
    # 构建新站点
    new_station = pd.DataFrame()
    new_station['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index, axis=0)['zone']
    new_station['id'] = new_station['zone'].apply(lambda x: int(str(x)[::]))  # 新站点命名，与区域名字相同
    new_capacity = new_station[['id']]
    new_capacity['capacity'] = 60
    new_capacity['bikes'] = new_capacity['capacity'].apply(lambda x: x * randint(4, 7) / 10)
    #
    old_stations['label'] = 0
    zone['label'] = 0
    new_capacity['label'] = 1
    new_station['label'] = 1
    old_stations = old_stations.set_index('id')
    new_capacity = new_capacity.set_index('id')

    # stations = pd.concat([stations, new_capacity])  # 往原站点数据加入新站点
    # zone = pd.concat([new_station, zone])  # 往区域数据中加入新站点
    # zone_count_stations = zone.groupby(['zone'])['id'].count().reset_index()  # 统计每个区域的站点数量
    # demand = pd.merge(demand, zone_count_stations, how='left', on='zone').rename(columns={'id': 'count_stations'})
    # stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
    # stations['bikes'] = round(stations['capacity'] * 0.6)  # 设置车子数量
    # stations['bikes'] = stations['capacity'].apply(lambda x: x * random.randint(4, 7)/10)  # 设置车子数量


    object(demand, zone, old_stations, days, new_capacity, new_station)


main(demand_i, zone_i, stations_i, 5)


# 204区域 3000501     216区域  3003300