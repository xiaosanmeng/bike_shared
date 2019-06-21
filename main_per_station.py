import pandas as pd
import numpy as np
from random import randint
from object_per_station import object


def main(demand, zone, stations, day):
    # 构建新站点
    new_station = pd.DataFrame()
    new_station['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index, axis=0)['zone']
    new_station['id'] = new_station['zone'].apply(lambda x: int(str(x)[::]))
    capacity_i = new_station[['id']]
    capacity_i['capacity'] = 60
    stations = pd.concat([stations, capacity_i])  # 加入新站点
    # stations['bikes'] = stations['capacity'].apply(lambda x: round(x * randint(2, 9)/10))  # 设置车子数量
    # 加入新站点
    zone = pd.concat([new_station, zone], sort=True)  # 加入新站点
    zone_count_stations = zone.groupby(['zone'])['id'].count().reset_index()  # 统计每个区域的站点数量
    demand = pd.merge(demand, zone_count_stations, how='left', on='zone').rename(columns={'id': 'count_stations'})
    stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
    # stations['bikes'] = round(stations['capacity'] * 0.6)  # 设置车子数量
    # stations['bikes'] = stations['capacity'].apply(lambda x: x * random.randint(4, 7)/10)  # 设置车子数量
    stations = stations.set_index('id')
    object(demand, zone, stations, day)


# 读取区域需求量
demand_i = pd.read_csv('F:/bikedata/bike_datas/test/zone_day.csv')
# 读取区域包含的站点信息
zone_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
    columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
# 读取站点信息
stations_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv')[['station_id', 'capacity']].\
    rename(columns={'station_id': 'id'})
main(demand_i, zone_i, stations_i, 5)
