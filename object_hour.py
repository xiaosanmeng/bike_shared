import pandas as pd
from numpy import random


# 读取区域需求量
demand = pd.read_csv('F:/bikedata/bike_datas/test/zone_hour.csv')
# 读取区域包含的站点信息
zone = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
    columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
# 读取站点信息
stations = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv')[['station_id', 'capacity']].\
    rename(columns={'station_id': 'id'})
# 创建新站点
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
# stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
# stations['bikes'] = round(stations['capacity'] * 0.6)  # 设置车子数量
stations['bikes'] = stations['capacity'].apply(lambda x: x * random.randint(4, 7)/10)  # 设置车子数量
stations = stations.set_index('id')

# 读取站点空白表
stations_demands = pd.read_csv('F:/bikedata/bike_datas/test/empty.csv')



#  计算每个区域分配给站点的需求量
def random_start(length, demands_i):
    points = [random.randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
    points = [0] + sorted(points) + [100]  # 排个队
    points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
    start = [round(points[i] * demands_i['start']) for i in range(length - 1)]
    end = [round(points[i] * demands_i['end']) for i in range(length - 1)]
    start.append(demands_i['start'] - sum(start))
    end.append(demands_i['end'] - sum(end))
    return start,end
# def random_end(length, demands_i):
#     points = [random.randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
#     points = [0] + sorted(points) + [100]  # 排个队
#     points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
#     start = [round(points[i] * demands_i['end']) for i in range(length - 1)]
#     start.append(demands_i['end'] - sum(start))
#     return start


t = 24
stop_list_set = []
demand = demand[demand['day'] == 1]
gap_sum = 0
for hour in range(t):  # 按时间段依此读取数据
    stop_list = []
    day_demand = demand[demand['hour'] == hour].reset_index(drop=True)
    stop = 0
    len_day_demand = len(day_demand)
    for z in range(len_day_demand):
        zone_data = day_demand.loc[z]  # 依此读取每个区域的数据
        length_stations = int(zone_data['count_stations'])  # 获取该区域站点的数量
        stations_list = list(zone[zone['zone'] == zone_data['zone']]['id'])  # 获取该区域站点的id
        capacity = stations.loc[stations_list]['capacity']  # 获取区域内站点的容量
        bikes = stations.loc[stations_list]['bikes']  # 获取区域内站点的车子数量
        for time_1 in range(2000):
            print('hour:', hour, 'zone:', z, len_day_demand, time_1)
            start_demands, end_demands = random_start(length_stations, zone_data)  # 分配区域借车量
            judge = start_demands <= bikes + end_demands
            judge_i = end_demands <= capacity - bikes + start_demands
            if judge[judge == True].sum() == length_stations and judge_i[judge_i == True].sum() == length_stations:
                break
            elif time_1 == 1999:
                stop = 1
        if stop == 1:
            print('无解')
            print('区域：', zone_data['zone'])
            stop_list.append(zone_data['zone'])
            stop = 0
        else:
            gap = [end_demands[i] - start_demands[i] for i in range(length_stations)]
            stations.loc[stations_list, 'bikes'] = bikes + gap
            gap = [abs(i) for i in gap]
            gap_sum += sum(gap)
    stop_list_set.append(('hour%s' % hour, stop_list))
print(stop_list_set)
print(gap_sum)

#  原站点 0.5[('day0', []), ('day1', []), ('day2', []), ('day3', []), ('day4', []), ('day5', []), ('day6', []), ('day7', [1010300.0]), ('day8', [1010400.0, 1011500.0]), ('day9', [1002800.0, 1003200.0, 1003400.0, 1005502.0, 1005600.0, 1006000.0, 1008200.0, 1009200.0, 1010100.0, 1010200.0, 1010300.0, 1011203.0, 1011401.0, 1011500.0, 3003300.0, 3018300.0, 3055100.0]), ('day10', [1005600.0, 1005800.0, 1009200.0, 1010100.0, 1010200.0, 3006300.0, 3018300.0]), ('day11', [1002800.0, 1004000.0, 1005700.0, 1010100.0, 1010200.0, 1011203.0, 3006300.0]), ('day12', [1001300.0, 1002000.0, 1004100.0, 1005502.0, 1005600.0, 1006000.0, 1011201.0, 3026500.0]), ('day13', [1000202.0, 3021100.0]), ('day14', [1000202.0, 1005400.0, 1010400.0, 3024500.0, 3026500.0, 3055100.0]), ('day15', [3003300.0, 3018700.0, 3024500.0]), ('day16', [1005400.0, 1010300.0, 1011500.0, 3003300.0]), ('day17', [1004800.0, 1010300.0, 3021100.0]), ('day18', [1005600.0, 1014500.0, 3021100.0]), ('day19', [1004800.0, 1011202.0, 1019000.0]), ('day20', [1007800.0, 1014900.0]), ('day21', []), ('day22', [1014900.0]), ('day23', [])]
#  原站点 0.6[('day0', []), ('day1', []), ('day2', []), ('day3', []), ('day4', []), ('day5', []), ('day6', []), ('day7', []), ('day8', [1005600.0, 1009200.0, 1010200.0, 1010300.0, 1010400.0, 1011203.0, 1011401.0]), ('day9', [1001300.0, 1003900.0, 1004500.0, 1005502.0, 1005600.0, 1005800.0, 1006000.0, 1006200.0, 1008200.0, 1009600.0, 1010100.0, 1010300.0, 1011201.0, 1011500.0, 1012500.0, 3003300.0, 3021100.0]), ('day10', [1002800.0, 1003400.0, 1004700.0, 1005400.0, 1005700.0, 1010200.0, 1013100.0, 3003300.0, 3018300.0]), ('day11', [1002800.0, 1003400.0, 1004100.0, 1005400.0, 1008200.0, 1010200.0, 1010400.0, 1011500.0, 3001100.0, 3006300.0, 3055100.0]), ('day12', [1002800.0, 1003900.0, 1004100.0, 1004700.0, 1005502.0, 1005600.0, 1008700.0, 3003300.0, 3024500.0]), ('day13', [1003200.0, 1013100.0, 3001100.0, 3002100.0, 3024500.0, 3055100.0]), ('day14', [1010400.0, 3002100.0, 3024500.0, 3026500.0, 3055100.0]), ('day15', [3003300.0, 3024500.0]), ('day16', [1005400.0, 1010300.0, 3003300.0, 3006300.0]), ('day17', [1010300.0, 3021100.0]), ('day18', [1005600.0, 1019000.0, 3021100.0]), ('day19', [1019000.0]), ('day20', []), ('day21', []), ('day22', [1014900.0, 3055500.0]), ('day23', [])]
#  原站点 0.4-0.6 [('hour0', []), ('hour1', []), ('hour2', []), ('hour3', []), ('hour4', []), ('hour5', []), ('hour6', []), ('hour7', []), ('hour8', [1005600.0, 1010300.0, 1010400.0, 1011203.0, 1011500.0]), ('hour9', [1003200.0, 1003400.0, 1004500.0, 1005502.0, 1006000.0, 1006200.0, 1008200.0, 1009200.0, 1010100.0, 1010300.0, 1011201.0, 1011500.0, 3003300.0, 3006300.0, 3018300.0, 3055100.0]), ('hour10', [1002800.0, 1005600.0, 1005800.0, 1010100.0, 1010200.0, 1010300.0, 3006300.0, 3018300.0, 3024500.0]), ('hour11', [1001300.0, 1002000.0, 1002800.0, 1003400.0, 1004100.0, 1005700.0, 1010100.0, 1010200.0, 1010400.0, 1011500.0, 3006300.0, 3026500.0]), ('hour12', [1001300.0, 1002000.0, 1002800.0, 1004100.0, 1005502.0, 1010100.0, 3024500.0, 3026500.0, 3027900.0]), ('hour13', [1003200.0, 3003300.0, 3021100.0, 3024500.0, 3027900.0, 3055100.0]), ('hour14', [1005800.0, 1010400.0, 3003300.0, 3024500.0, 3026500.0, 3055100.0]), ('hour15', [1006000.0, 3003300.0, 3018700.0, 3024500.0]), ('hour16', [1004800.0, 1010300.0, 3003300.0, 3006300.0]), ('hour17', [1010300.0, 3021100.0]), ('hour18', [1005600.0, 1013900.0, 3021100.0]), ('hour19', [1011202.0, 1019000.0]), ('hour20', [1007800.0, 1014900.0]), ('hour21', []), ('hour22', [1014900.0, 3000501.0]), ('hour23', [])]





#  加入新站点 0.5[('day0', []), ('day1', []), ('day2', []), ('day3', []), ('day4', []), ('day5', []), ('day6', []),
# ('day7', []), ('day8', []), ('day9', [1010300.0]), ('day10', []), ('day11', [1010100.0]),
# ('day12', [1005600.0, 1010100.0]), ('day13', []), ('day14', []), ('day15', []), ('day16', []), ('day17', [1010300.0]),
#  ('day18', []), ('day19', []), ('day20', []), ('day21', []), ('day22', []), ('day23', [])]
# 加入新站点 0.6[('day0', []), ('day1', []), ('day2', []), ('day3', []), ('day4', []), ('day5', []), ('day6', []),
# ('day7', []), ('day8', []), ('day9', [1005600.0]), ('day10', [1009200.0, 1010300.0]), ('day11', []), ('day12', []),
# ('day13', []), ('day14', []), ('day15', []), ('day16', [3003300.0]), ('day17', []), ('day18', [1010300.0]),
# ('day19', []), ('day20', []), ('day21', []), ('day22', []), ('day23', [])]
# #加入新站点 0.4-0.6 [('hour0', []), ('hour1', []), ('hour2', []), ('hour3', []), ('hour4', []), ('hour5', []), ('hour6', []),
# ('hour7', []), ('hour8', []), ('hour9', [1010300.0]), ('hour10', [1005600.0, 1010100.0]), ('hour11', [1010100.0]),
# ('hour12', [1010100.0]), ('hour13', []), ('hour14', []), ('hour15', []), ('hour16', []), ('hour17', [1010300.0]),
# ('hour18', []), ('hour19', []), ('hour20', []), ('hour21', []), ('hour22', []), ('hour23', [])]




# gap 0.5
# gap 0.6
# gap 0.4-0.6