import pandas as pd
from numpy import random

# 读取区域需求量
demand = pd.read_csv('F:/bikedata/bike_datas/test/zone_day.csv')
# 读取区域包含的站点信息
zone = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
    columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
# 读取站点信息
stations = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv')[['station_id', 'capacity']].\
    rename(columns={'station_id': 'id'})
new_station = pd.DataFrame()
#############################  加入新站点
# new_station['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index,axis=0)['zone']
# new_station['id'] = new_station['zone'].apply(lambda x: int(str(x)[::]))
# capacity_i = new_station[['id']]
# capacity_i['capacity'] = 60
# stations = pd.concat([stations, capacity_i])  # 加入新站点
###############################
zone = pd.concat([new_station, zone])  # 加入新站点
zone_count_stations = zone.groupby(['zone'])['id'].count().reset_index()  # 统计每个区域的站点数量
demand = pd.merge(demand, zone_count_stations, how='left', on='zone').rename(columns={'id': 'count_stations'})
stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
# stations['bikes'] = round(stations['capacity'] * 0.6)  # 设置车子数量
# stations['bikes'] = stations['capacity'].apply(lambda x: x * random.randint(4, 7)/10)  # 设置车子数量
stations = stations.set_index('id')

# 读取站点空白表
stations_demands = pd.read_csv('F:/bikedata/bike_datas/test/empty.csv')

#  计算每个区域分配给站点的需求量
def random_start(length, demands_i):
    points = [random.randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
    points = [0] + sorted(points) + [100]  # 排个队
    points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
    start = [round(points[i] * demands_i['start']) for i in range(length - 1)]
    start.append(demands_i['start'] - sum(start))
    return start
def random_end(length, demands_i):
    points = [random.randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
    points = [0] + sorted(points) + [100]  # 排个队
    points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
    start = [round(points[i] * demands_i['end']) for i in range(length - 1)]
    start.append(demands_i['end'] - sum(start))
    return start


t = 1
gap_sum = 0

for day in range(t):  # 按时间段依此读取数据
    day_demand = demand[demand['day'] == day+1].reset_index(drop=True)
    stop = 0  # 用于不可行解的判断
    stop_list = [] # 用于不可行解的判断
    len_day_demand = len(day_demand)  # 统计区域数量
    for z in range(len_day_demand):
        zone_data = day_demand.loc[z]  # 依此读取每个区域的数据
        length_stations = int(zone_data['count_stations'])  # 获取该区域站点的数量
        stations_list = list(zone[zone['zone'] == zone_data['zone']]['id'])  # 获取该区域站点的id
        capacity = stations.loc[stations_list]['capacity']  # 获取区域内站点的容量
        bikes = stations.loc[stations_list]['bikes']  # 获取区域内站点的车子数量
        for time_1 in range(3000):
            print('day:', day, 'zone:', z, len_day_demand, time_1)
            start_demands = random_start(length_stations, zone_data)  # 分配区域借车量
            end_demands = random_end(length_stations, zone_data)  # 分配区域还车量
            judge = start_demands <= bikes + end_demands  #  判断借车量是否小于等于站点车子数量+换车数量
            judge_i = end_demands <= capacity - bikes + start_demands #  判断还车量是否小于等于站点空桩数量+换车数量
            if judge[judge == True].sum() == length_stations and judge_i[judge_i == True].sum() == length_stations:  #如果两者都满足，分配借还量
                break
            elif time_1 == 2999:
                stop = 1
        if stop == 1: #统计不可行解
            print('无解')
            print('区域：', zone_data['zone'])
            stop_list.append(zone_data['zone'])
            stop = 0
        else:
            gap = [end_demands[i] - start_demands[i] for i in range(length_stations)]  # 站点车子数量变动过程
            stations.loc[stations_list, 'bikes'] = bikes + gap
            gap = [abs(i) for i in gap]
            gap_sum += sum(gap)
print(stop_list)
print(gap_sum)





#  day1[1005502.0, 1010300.0, 1014300.0, 1014900.0, 1019000.0, 3003300.0, 3055500.0]  尝试在这些区域加站点
#  day2[1004200.0, 3000501.0, 3002100.0]  [1004200.0, 1014300.0, 3000501.0, 3002100.0]
#  day3[1003400.0, 1004500.0, 1004700.0, 1004800.0, 1005400.0, 1005501.0, 1005700.0, 1014300.0, 1014900.0, 1015300.0, 3000501.0, 3000700.0, 3002100.0, 3003300.0, 3004100.0, 3013300.0, 3015500.0, 3019700.0, 3020500.0, 3027500.0, 3055100.0]
#  day4[1003002.0, 1003800.0, 1004200.0, 1004800.0, 1006000.0, 1006700.0, 1008000.0, 1011202.0, 1011700.0, 1012900.0, 1014300.0, 1014402.0, 1014500.0, 1016500.0, 1017300.0, 1018300.0, 3000100.0, 3000501.0, 3000700.0, 3002901.0, 3006700.0, 3012901.0, 3021100.0, 3021900.0, 3026500.0, 3028501.0, 3052500.0, 3054300.0, 3055100.0, 3057900.0]

# 0.4[1005502.0, 1010300.0, 1011202.0, 1014300.0, 1014500.0, 1014900.0, 3003300.0]
# 0.5[1005502.0, 1010300.0, 1014300.0, 1014900.0, 1019000.0, 3003300.0, 3055500.0]
# 0.6[1004800.0, 1005502.0, 1007800.0, 1008000.0, 1010300.0, 1011202.0, 1014500.0, 1014900.0, 3003300.0, 3052500.0,
# 3055100.0]

# 0.7[1002202.0, 1005502.0, 1010300.0, 1011700.0, 1013600.0, 1014300.0, 1019000.0, 3002100.0, 3003300.0, 3012902.0,
# 3018501.0, 3021100.0, 3055500.0]

# 0.8[1000700.0, 1001002.0, 1002202.0, 1003002.0, 1003700.0, 1004200.0, 1004400.0, 1005502.0, 1008601.0, 1009900.0,
# 1010300.0, 1011700.0, 1012100.0, 1012800.0, 1013600.0, 1014300.0, 1014402.0, 1015500.0, 1019000.0, 3002100.0,
# 3003300.0, 3012902.0, 3018501.0, 3020300.0, 3021100.0, 3024500.0, 3054300.0, 3055500.0]

# 0.9[1000700.0, 1001002.0, 1001200.0, 1001800.0, 1002201.0, 1002202.0, 1002800.0, 1003002.0, 1003602.0, 1003700.0,
# 1004000.0, 1004200.0, 1004400.0, 1004700.0, 1004900.0, 1005501.0, 1005502.0, 1005700.0, 1006200.0, 1008601.0,
# 1009900.0, 1010300.0, 1011100.0, 1011300.0, 1011700.0, 1012100.0, 1012400.0, 1012800.0, 1013600.0, 1013800.0,
# 1014300.0, 1014401.0, 1014402.0, 1014700.0, 1015500.0, 1015602.0, 1015900.0, 1018000.0, 1018300.0, 1018700.0,
# 1019000.0, 1019800.0, 1020600.0, 3002100.0, 3002901.0, 3003300.0, 3004500.0, 3005300.0, 3006500.0, 3006700.0,
# 3006900.0, 3011900.0, 3012902.0, 3013300.0, 3013900.0, 3018501.0, 3020100.0, 3020300.0, 3021100.0, 3021700.0,
# 3022100.0, 3024100.0, 3024500.0, 3026900.0, 3027500.0, 3028501.0, 3051700.0, 3054300.0, 3054700.0, 3055500.0,
# 3055700.0, 3056500.0, 3057900.0, 4005500.0, 4008100.0, 4009700.0]


# [1000700, 1005502, 1009900, 1010300, 1012100, 1014300, 1014900, 1019000, 3002100, 3003300, 3055500]
# [1005502, 1009900, 1010300, 1012100, 1014300, 1014900, 1019000, 3003300, 3055500]


demand['abs'] = abs(demand['start'] - demand['end'])
demand['abs'].sum()

# 原站点0.6    [4574.0  ，4840.0  4583.0  4818.0  4675.0]