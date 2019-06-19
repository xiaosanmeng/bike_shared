import pandas as pd
import numpy as np
from random import randint



#  老站点寻求可行解的目标函数

# # 读取区域需求量
# demand = pd.read_csv('F:/bikedata/bike_datas/test/zone_day.csv')
# # 读取区域包含的站点信息
# zone = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
#     columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
# # 读取站点信息
# stations = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv')[['station_id', 'capacity']].\
#     rename(columns={'station_id': 'id'})
# new_station = pd.DataFrame()
# ############################  加入新站点
# # new_station['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index,axis=0)['zone']
# # new_station['id'] = new_station['zone'].apply(lambda x: int(str(x)[::]))
# # capacity_i = new_station[['id']]
# # capacity_i['capacity'] = 60
# # stations = pd.concat([stations, capacity_i])  # 加入新站点
# ##############################
# zone = pd.concat([new_station, zone])  # 加入新站点
# zone_count_stations = zone.groupby(['zone'])['id'].count().reset_index()  # 统计每个区域的站点数量
# demand = pd.merge(demand, zone_count_stations, how='left', on='zone').rename(columns={'id': 'count_stations'})
# # stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
# stations['bikes'] = round(stations['capacity'] * 0.6)  # 设置车子数量
# # stations['bikes'] = stations['capacity'].apply(lambda x: x * random.randint(4, 7)/10)  # 设置车子数量
# stations = stations.set_index('id')
#
# # 读取站点空白表
# stations_demands = pd.read_csv('F:/bikedata/bike_datas/test/empty.csv')


# 读取区域需求量
demand_i = pd.read_csv('F:/bikedata/bike_datas/test/zone_day.csv')
# 读取区域包含的站点信息
zone_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
    columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
# 读取站点信息
stations_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv')[['station_id', 'capacity']].\
    rename(columns={'station_id': 'id'})
new_station_i = pd.DataFrame()




def object(demand, zone, stations, time):
    def random_start(length, demands_i):
        points = [randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
        points = [0] + sorted(points) + [100]  # 排个队
        points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
        start_demand = demands_i['start'][0]
        end_demand = demands_i['end'][0]
        start = [round(points[i] * start_demand) for i in range(length - 1)]
        end = [round(points[i] * end_demand) for i in range(length - 1)]
        start.append(demands_i['start'] - sum(start))
        end.append(demands_i['end'] - sum(end))
        return start, end

    def station_init_bikes(data, list, capacity_i):
        data.loc[list, 'bikes'] = round(capacity_i * randint(0, 100) / 100)
        return data

    # stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
    zone_list = demand.drop(demand[demand[['zone']].duplicated()].index, axis=0)['zone']  # 区域列
    gap_sum, start_demand_sum, end_demands_sum = 0, 0, 0  # 统计缺口总量, 满足的借车需求量, 满足的还车需求量
    stop_list = []
    for index, z in enumerate(zone_list):
        zone_data = demand[demand['zone'] == z]  # 依此读取每个区域的数据
        stations_list = list(zone[zone['zone'] == z]['id'])  # 获取该区域站点的id
        length_stations = len(stations_list)  # 获取该区域站点的数量
        for reset_bikes in range(500):  # 寻找可行初始解的次数
            stop = 0
            for day in range(time):
                if (day+1) not in list(zone_data['day']):
                    continue
                day_demand = zone_data[zone_data['day'] == (day+1)].reset_index(drop=True)
                capacity = stations.loc[stations_list]['capacity']  # 获取区域内站点的容量
                bikes = stations.loc[stations_list]['bikes']  # 获取区域内站点的车子数量
                for time_1 in range(100):
                    # day_demand = pd.Series(day_demand)
                    print('round', reset_bikes, 'day:', day + 1, 'zone:', z, "%:", index, len(zone_list), time_1)
                    start_demands, end_demands = random_start(length_stations, day_demand)  # 分配区域借车量
                    judge = start_demands <= bikes + end_demands
                    judge_i = end_demands <= capacity - bikes + start_demands
                    if judge[judge == True].sum() == length_stations and judge_i[
                        judge_i == True].sum() == length_stations:
                        break
                    elif time_1 == 99:
                        stop = 1
                if stop == 1:
                    stations = station_init_bikes(stations, stations_list, capacity)
                    break
                else:
                    gap = [end_demands[i] - start_demands[i] for i in range(length_stations)]
                    stations.loc[stations_list, 'bikes'] = bikes + gap
                    start_demand = sum(start_demands)
                    end_demands = sum(end_demands)
                    gap = [abs(i) for i in gap]
                    start_demand_sum += start_demand
                    end_demands_sum += end_demands
                    gap_sum += sum(gap)
                    stop = 2
            if reset_bikes == 499:
                stop_list.append([stations_list, day])
            if stop == 2:
                break
    print(stop_list)
    print(gap_sum, start_demand_sum, end_demands_sum)
# 主函数
def main(demand, zone, stations, new_station, day):
    # 构建新站点
    new_station['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index, axis=0)['zone']
    new_station['id'] = new_station['zone'].apply(lambda x: int(str(x)[::]))
    capacity_i = new_station[['id']]
    capacity_i['capacity'] = 60
    stations = pd.concat([stations, capacity_i])  # 加入新站点
    stations['bikes'] = stations['capacity'].apply(lambda x: round(x * randint(2, 9)/10))  # 设置车子数量
    # 加入新站点
    zone = pd.concat([new_station, zone], sort=True)  # 加入新站点
    zone_count_stations = zone.groupby(['zone'])['id'].count().reset_index()  # 统计每个区域的站点数量
    demand = pd.merge(demand, zone_count_stations, how='left', on='zone').rename(columns={'id': 'count_stations'})
    # stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
    # stations['bikes'] = round(stations['capacity'] * 0.6)  # 设置车子数量
    # stations['bikes'] = stations['capacity'].apply(lambda x: x * random.randint(4, 7)/10)  # 设置车子数量
    stations = stations.set_index('id')
    object(demand, zone, stations, day)
main(demand_i, zone_i, stations_i, new_station_i, 1)
