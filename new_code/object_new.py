from random import randint
from time import time


def object(time_i, demand, zone, stations, time1):
    # def choose_start_station(start, end, stations_data):
    #     judge = 0
    #     i, j = None, None
    #     for i in start['id']:
    #         if stations_data.loc[i]['bikes'] > 0:
    #             judge += 1
    #             break
    #     for j in end['id']:
    #         if stations_data.loc[j]['bikes'] < stations_data.loc[i]['capacity']:
    #             judge += 1
    #             break
    #
    #     return judge, i, j
    #
    # def choose_end_station(end, stations_data):
    #     judge = 0
    #     i = None
    #     for i in end['id']:
    #         if stations_data.loc[i]['bikes'] < stations_data.loc[i]['capacity']:
    #             judge = 1
    #             break
    #     return judge, i

    def random_distribution(stations, demand):
        length = len(stations)
        points = [randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
        points = [0] + sorted(points) + [100]  # 排个队
        points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
        demand_distribution = [round(points[i] * demand) for i in range(length - 1)]
        demand_distribution.append(demand - sum(demand_distribution))
        return demand_distribution

    def demands_distribution_rate(start, end, demand, stations, rate, day, zone_index, sum_index, sum_demands, time1):  # stations 稍后试一下精简代码，速度是否有提升
        judge = 0
        end_empty = stations.loc[end['id']]['capacity'] - stations.loc[end['id']]['bikes'] # 获取区域内站点的容量
        start_bikes = stations.loc[start['id']]['bikes']  # 获取区域内站点的车子数量
        for i in range(rate):
            demand_i = demand * (1 - i/rate)
            if demand_i < start_bikes.sum() and demand_i < end_empty.sum():
                for j in range(100):
                    print(time1, day, zone_index, sum_index, i, j)
                    start_demand = random_distribution(start['id'], demand_i)
                    end_demand = random_distribution(end['id'], demand_i)
                    if (start_demand <= start_bikes).all() and (end_demand <= end_empty).all():
                        stations.loc[start['id'], 'bikes'] -= start_demand
                        stations.loc[end['id'], 'bikes'] += end_demand
                        sum_demands += demand_i
                        judge = 1
                        break
            if judge == 1:
                break
        return judge, stations, sum_demands

    def demands_distribution(start, end, demand, stations, rate, day, zone_index, sum_index, sum_demands, time1):  # stations 稍后试一下精简代码，速度是否有提升
        judge = 0
        end_empty = stations.loc[end['id']]['capacity'] - stations.loc[end['id']]['bikes'] # 获取区域内站点的容量
        start_bikes = stations.loc[start['id']]['bikes']  # 获取区域内站点的车子数量
        demand_i = demand
        if demand_i < start_bikes.sum() and demand_i < end_empty.sum():
            for j in range(100):
                print(time1, day, zone_index, sum_index, j)
                start_demand = random_distribution(start['id'], demand_i)
                end_demand = random_distribution(end['id'], demand_i)
                if (start_demand <= start_bikes).all() and (end_demand <= end_empty).all():
                    stations.loc[start['id'], 'bikes'] -= start_demand
                    stations.loc[end['id'], 'bikes'] += end_demand
                    sum_demands += demand_i
                    judge = 1
                    break
        return judge, stations, sum_demands


    demand_sum = 0
    t1, t2, t3, t4, t5, t6 = 0, 0, 0, 0, 0, 0
    t11 = time()
    demand['T'] = 0
    for day in range(time1):
        day = day + 1
        day_demand = demand[demand['day'] == day].reset_index()
        # day_demand = day_demand.groupby(['start', 'end']).count().reset_index().rename(columns={'day': 'count'})
        len_data = len(day_demand)
        z = 5
        for time1 in range(z):
            for data_index in range(len_data):
                demand_i = day_demand.loc[data_index]
                if demand_i['T'] == 1:
                    continue
                start_zone, end_zone = zone[zone['zone'] == demand_i['start']], zone[zone['zone'] == demand_i['end']]
                zone_demand = demand_i['demands']
                if time1 < z - 1:
                    judge, stations, demand_sum = demands_distribution(start_zone, end_zone, zone_demand, stations, 10,
                                                                       day, data_index, len_data, demand_sum, time1)
                else:
                    judge, stations, demand_sum = demands_distribution_rate(start_zone, end_zone, zone_demand, stations, 10,
                                                                       day, data_index, len_data, demand_sum, time1)
                if judge == 1:
                    day_demand.loc[data_index, 'T'] = 1
    t12 = time()
    t1 = t12-t11
    print('用时', t1, '需求量', demand_sum)

# 3轮 用时 591.881649017334 需求量 27167.4
# 用时 785.3199377059937 需求量 27252.89999999996






            # t11 = time()
            # t12 = time()
            # t1 += (t12-t11)
            # t21 = time()
            # start_zone, end_zone = zone[zone['zone'] == demand_i['start']], zone[zone['zone'] == demand_i['end']]
            # demand_zone = demand_i['demands']
            # t22 = time()
            # t2 += (t22 - t21)
            # t31 = time()
            # end_zone = zone[zone['zone'] == demand_i['end']]
            # t32 = time()
            # t3 += (t32 - t31)
            # t41 = time()
            # # judge, start_id, end_id = choose_start_station(start_zone, end_zone, stations)
            # t42 = time()
            # t4 += (t42 - t41)
            # t51 = time()
            # end_judge, = choose_end_station(end_zone, stations)
            # t52 = time()
            # t5 += (t52 - t51)
            # t61 = time()
            # if judge == 2:
            #     demand_sum += 1
            #     stations.loc[start_id, 'bikes'] += 1
            #     stations.loc[end_id, 'bikes'] -= 1
            # t62 = time()
            # t6 += (t62 - t61)
    # print(t1, t2, t3, t4, t5, t6) # 7.226779460906982 26.5844943523407 24.571924448013306 16.974573612213135 22.295313358306885 41.07453465461731

    # print(demand_sum)







    # stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
    # zone_list = demand.drop(demand[demand[['zone']].duplicated()].index, axis=0)['zone']  # 区域列
    # gap_sum, start_demand_sum, end_demands_sum = 0, 0, 0  # 统计缺口总量, 满足的借车需求量, 满足的还车需求量
    # stop_list = []
    # for index, z in enumerate(zone_list):
    #     zone_data = demand[demand['zone'] == z]  # 依此读取每个区域的数据
    #     stations_list = list(zone[zone['zone'] == z]['id'])  # 获取该区域站点的id
    #     length_stations = len(stations_list)  # 获取该区域站点的数量
    #     stations_copy = stations.copy()
    #     round2 = 20
    #     for reset_demands in range(round2):  # 寻找可行初始解的次数
    #         stop = 0
    #         start_demands_copy, end_demands_copy, gap_sum_copy = 0, 0, 0
    #         for day in range(time):
    #             if (day+1) not in list(zone_data['day']):
    #                 continue
    #             day_demand = zone_data[zone_data['day'] == (day+1)].reset_index(drop=True)
    #             capacity = stations_copy.loc[stations_list]['capacity']  # 获取区域内站点的容量
    #             bikes = stations_copy.loc[stations_list]['bikes']  # 获取区域内站点的车子数量
    #             for time_1 in range(100):
    #                 # day_demand = pd.Series(day_demand)
    #                 print('round1:', time_i, 'zone:', z, "%:", (index, len(zone_list)),  'round2', reset_demands, 'day:', day + 1, time_1,)
    #                 start_demands, end_demands = random_start(length_stations, day_demand, reset_demands, round2)
    #                 # start_demands = random_start(length_stations, day_demand)  # 分配区域借车量
    #                 # end_demands = random_end(length_stations, day_demand)  # 分配区域借车量
    #                 judge = start_demands <= bikes + end_demands
    #                 judge_i = end_demands <= capacity - bikes + start_demands
    #                 if judge[judge == True].sum() == length_stations and \
    #                         judge_i[judge_i == True].sum() == length_stations:
    #                     break
    #                 elif time_1 == 99:
    #                     stop = 1
    #             if stop == 1:
    #                 stations_copy = stations.copy()
    #                 # stations_copy = station_init_bikes(reset_bikes, stations_copy, stations_list, capacity)
    #                 break
    #             else:
    #                 gap = [end_demands[i] - start_demands[i] for i in range(length_stations)]
    #                 stations_copy.loc[stations_list, 'bikes'] = bikes + gap
    #                 start_demands = sum(start_demands)
    #                 end_demands = sum(end_demands)
    #                 gap = [abs(i) for i in gap]
    #                 start_demands_copy += start_demands
    #                 end_demands_copy += end_demands
    #                 gap_sum_copy += sum(gap)
    #                 stop = 2
    #         if reset_demands == (round2 - 1):
    #             stop_list.append([index, stations_list, day])
    #         if stop == 2:
    #             start_demand_sum += start_demands_copy
    #             end_demands_sum += end_demands_copy
    #             gap_sum += gap_sum_copy
    #             stations = stations_copy
    #             break
    # # print(stop_list)
    # # print(gap_sum, start_demand_sum, end_demands_sum)
    # return gap_sum, start_demand_sum, end_demands_sum
