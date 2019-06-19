import pandas as pd
from numpy import random


#  加入新站点寻求可行解的目标函数

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

 # 计算每个区域分配给站点的需求量


def object(demand, zone, old_stations, time, new_capacity, new_station):
    def random_start(length, demands_i):
        points = [random.randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
        points = [0] + sorted(points) + [100]  # 排个队
        points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
        start = [round(points[i] * demands_i['start']) for i in range(length - 1)]
        end = [round(points[i] * demands_i['end']) for i in range(length - 1)]
        start.append(demands_i['start'] - sum(start))
        end.append(demands_i['end'] - sum(end))
        return start, end


    # def station_init_bikes(data, t_list, bikes_list, list, capacity_i):
    #     data['bikes'] = round(data['capacity'] * 0.5)
    #     data.loc[t_list, 'bikes'] = bikes_list
    #     data.loc[list, 'bikes'] = round(capacity_i * random.randint(0, 100) / 100)
    #     return data

    def new_station_init_bikes(old_data, new_data, t_list, bikes_list, list, capacity_i):
        # data['bikes'] = round(data['capacity'] * 0.5)

        new_data.loc[t_list, 'bikes'] = bikes_list
        new_data.loc[list, 'bikes'] = round(capacity_i * random.randint(0, 100) / 100)
        data = pd.concat([old_data, new_data])  # 往原站点数据加入新站点
        return data

    stations = pd.concat([old_stations, new_capacity])  # 往原站点数据加入新站点
    zone = pd.concat([new_station, zone])  # 往区域数据中加入新站点
    zone_count_stations = zone.groupby(['zone'])['id'].count().reset_index()  # 统计每个区域的站点数量
    demand = pd.merge(demand, zone_count_stations, how='left', on='zone').rename(columns={'id': 'count_stations'})
    # stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
    # stations['bikes'] = round(stations['capacity'] * 0.6)  # 设置车子数量
    # stations['bikes'] = stations['capacity'].apply(lambda x: x * random.randint(4, 7)/10)  # 设置车子数量
    # stations = stations.set_index('id')
    # stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
    t = time
    stop_list_set = []  # 统计问题区域（需求量无法分配）
    question_list = []  # 用于记录问题区域的站点
    bikes_i = 0
    for t2 in range(500):
        stop = 0
        gap_sum, start_demand_sum, end_demands_sum = 0, 0, 0  # 统计缺口总量, 满足的借车需求量, 满足的还车需求量
        for day in range(t):  # 按时间段依此读取数据
            stop_list = []
            day_demand = demand[demand['day'] == day + 1].reset_index(drop=True)  # 一次读取每天需求量数据
            stop = 0
            len_day_demand = len(day_demand)
            for z in range(len_day_demand):  # 对区域进行循环
                zone_data = day_demand.loc[z]  # 依此读取每个区域的数据
                length_stations = int(zone_data['count_stations'])  # 获取该区域站点的数量
                stations_list = list(zone[zone['zone'] == zone_data['zone']]['id'])  # 获取该区域站点的id
                new_stations_list = list(zone[(zone['zone'] == zone_data['zone']) & (zone['label'] == 1)]['id'])  # 获取该区域新站点的id
                capacity = stations.loc[stations_list]['capacity']  # 获取区域内站点的容量
                bikes = stations.loc[stations_list]['bikes']  # 获取区域内站点的车子数量
                for time_1 in range(100):
                    print('round', t2, 'day:', day+1, 'zone:', z, len_day_demand, time_1)
                    start_demands, end_demands = random_start(length_stations, zone_data)  # 分配区域借车量
                    judge = start_demands <= bikes + end_demands
                    judge_i = end_demands <= capacity - bikes + start_demands
                    if judge[judge == True].sum() == length_stations and judge_i[
                        judge_i == True].sum() == length_stations:
                        break
                    elif time_1 == 99:
                        stop = 1
                if stop == 1:
                    stop_list.append(new_stations_list)
                    [question_list.append(i) for i in new_stations_list if i not in question_list]
                    # t1 = [z for i in t1 for z in i]
                    # bikes_i = stations.loc[t1]['bikes']
                    # print('区域：', zone_data['zone'])
                    # stop_list.append(zone_data['zone'])

                    stations = new_station_init_bikes(old_stations, new_capacity, question_list, bikes_i, new_stations_list, capacity)
                    bikes_i = stations.loc[question_list]['bikes']
                    break
                    # stop = 0
                else:
                    gap = [end_demands[i] - start_demands[i] for i in range(length_stations)]
                    stations.loc[stations_list, 'bikes'] = bikes + gap
                    start_demand = sum(start_demands)
                    end_demands = sum(end_demands)
                    gap = [abs(i) for i in gap]
                    start_demand_sum += start_demand
                    end_demands_sum += end_demands
                    gap_sum += sum(gap)
            if stop == 1:
                break
            else:
                stop = 2
            stop_list_set.append(('day%s' % (day+1), stop_list))
        if stop == 2:
            break

    print(stop_list_set)
    print(gap_sum, start_demand_sum, end_demands_sum)


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