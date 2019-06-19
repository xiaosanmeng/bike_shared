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
# 创建新站点
new_station = pd.DataFrame()
################################# 加入新站点
# new_station['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index,axis=0)['zone']
# new_station['id'] = new_station['zone'].apply(lambda x: int(str(x)[::]))
# capacity_i = new_station[['id']]
# capacity_i['capacity'] = 60
# stations = pd.concat([stations, capacity_i])  # 加入新站点
###################################
zone = pd.concat([new_station, zone])  # 加入新站点
zone_count_stations = zone.groupby(['zone'])['id'].count().reset_index()  # 统计每个区域的站点数量
demand = pd.merge(demand, zone_count_stations, how='left', on='zone').rename(columns={'id': 'count_stations'})
# stations['bikes'] = stations['capacity'].apply(lambda x: x * random.randint(4, 7)/10)  # 设置车子数量
stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
# stations['bikes'] = round(stations['capacity'] * 0.6)  # 设置车子数量

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


t = 1
stop_list_set = []
gap_sum = 0
start_demand_sum = 0
end_demands_sum = 0
for day in range(t):  # 按时间段依此读取数据
    stop_list = []
    day_demand = demand[demand['day'] == day+1].reset_index(drop=True)
    stop = 0
    len_day_demand = len(day_demand)
    for z in range(len_day_demand):
        zone_data = day_demand.loc[z]  # 依此读取每个区域的数据
        length_stations = int(zone_data['count_stations'])  # 获取该区域站点的数量
        stations_list = list(zone[zone['zone'] == zone_data['zone']]['id'])  # 获取该区域站点的id
        capacity = stations.loc[stations_list]['capacity']  # 获取区域内站点的容量
        bikes = stations.loc[stations_list]['bikes']  # 获取区域内站点的车子数量
        for time_1 in range(2000):
            print('day:', day, 'zone:', z, len_day_demand, time_1)
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
            start_demand = sum(start_demands)
            end_demands = sum(end_demands)
            gap = [abs(i) for i in gap]
            start_demand_sum += start_demand
            end_demands_sum += end_demands
            gap_sum += sum(gap)
    stop_list_set.append(('day%s' % day, stop_list))
print(stop_list_set)
print(gap_sum, start_demand_sum, end_demands_sum)

# 0.5 [1005502.0, 1010300.0, 1014900.0, 1019000.0, 3003300.0, 3055500.0]
# 0.6 [1005502.0, 1010300.0, 1011202.0, 1014500.0, 1014900.0, 3003300.0]


