import pandas as pd
import numpy as np
from random import randint
from object_test import object


# 读取区域需求量
demand_i = pd.read_csv('F:/bikedata/bike_datas/test/zone_day.csv')
# 读取区域包含的站点信息
zone_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
    columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
# 读取站点信息
stations_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv')[['station_id', 'capacity']].\
    rename(columns={'station_id': 'id'})
new_station_i = pd.DataFrame()

# 主函数
def main(demand, zone, stations, new_station, day):
    # 构建新站点
    new_station['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index,axis=0)['zone']
    new_station['id'] = new_station['zone'].apply(lambda x: int(str(x)[::]))
    capacity_i = new_station[['id']]
    capacity_i['capacity'] = 60
    stations = pd.concat([stations, capacity_i])  # 加入新站点
    stations['bikes'] = stations['capacity'].apply(lambda x: x * randint(2, 9)/10)  # 设置车子数量
    # 加入新站点
    zone = pd.concat([new_station, zone])  # 加入新站点
    zone_count_stations = zone.groupby(['zone'])['id'].count().reset_index()  # 统计每个区域的站点数量
    demand = pd.merge(demand, zone_count_stations, how='left', on='zone').rename(columns={'id': 'count_stations'})
    # stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
    # stations['bikes'] = round(stations['capacity'] * 0.6)  # 设置车子数量
    # stations['bikes'] = stations['capacity'].apply(lambda x: x * random.randint(4, 7)/10)  # 设置车子数量
    stations = stations.set_index('id')

    object(demand, zone, stations, day)


main(demand_i, zone_i, stations_i, new_station_i, 5)


# object(demand, zone, stations, 1)
#  原数据一天   gap 3346.0  start 30228  end 30228

#  开始结束需求量分配比例不同
#  原站点 初始车子比例 0.6  4773.0 28576.0 28485.0 / 4825.0 28462.0 28287.0 /4759.0 29059.0 28936.0 /4574.0 27875.0 27775.0
#  加入新站点 车子比例 0.6  8059.0 28529.0 28528.0 / 8378.0 29365.0 29315.0 /7822.0 28795.0 28737.0 /8126.0 28312.0 28286.0

#  开始结束需求量分配比例一致
#  原站点 初始车子比例 0.6  2382.0 29530.0 29398.0 / 2384.0 29530.0 29398.0 / 2388.0 29530.0 29398.0 / 2384.0 29530.0 29398.0
#  原站点 初始车子比例 0.5  2368.0 29430.0 29362.0 / 2374.0 29430.0 29362.0 / 2370.0 29430.0 29362.0 / 2370.0 29430.0 29362.0
#  原站点 初始车子比例 0.4-0.6 2358.0 29450.0 29368.0 / 2342.0 29229.0 29169.0 / 2351.0 29420.0 29369.0 / 2319.0 29203.0 29164.0

#  加入新站点 车子比例 0.6  2509.0 29836.0 29777.0 / 2519.0 29836.0 29777.0 / 2503.0 29836.0 29777.0 / 2513.0 29836.0 29777.0
#  加入新站点 车子比例 0.5  2574.0 30228.0 30228.0 / 2578.0 30228.0 30228.0 / 2572.0 30228.0 30228.0 / 2564.0 30228.0 30228.0
#  加入新站点 车子比例 0.4-0.6  2566.0 30228.0 30228.0 / 2570.0 30228.0 30228.0 / 2566.0 30228.0 30228.0 / 2576.0 30228.0 30228.0

# 开始结束需求量分配比例一致
# 原站点/初始车子比例 0.5/不断改变需求量无法分配的站点初始比例/day1  2554.0 30228.0 30228.0 / 2564.0 30228.0 30228.0 / 2556.0 30228.0 30228.0
# 原站点/初始车子比例 0.5/不断改变需求量无法分配的站点初始比例/day1-2  4569.0 48228.0 48227.0 / 4577.0 48228.0 48227.0/4575.0 48228.0 48227.0

# 加入新站点/所有站点初始比例随机/不断改变需求量无法分配的站点初始比例/day5 12770.0 136985.0 136983.0/ 12748.0 136985.0 136983.0 /12742.0 136985.0 136983.0 / 12776.0 136985.0 136983.0 /12758.0 136985.0 136983.0
