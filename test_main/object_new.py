from random import randint


def object(time_i, demand, zone, stations, time):
    # def random_start(length, demands_i):
    #     points = [randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
    #     points = [0] + sorted(points) + [100]  # 排个队
    #     points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
    #     start_demand = demands_i['start'][0]
    #     start = [round(points[i] * start_demand) for i in range(length - 1)]
    #     start.append(start_demand - sum(start))
    #     return start
    #
    # def random_end(length, demands_i):
    #     points = [randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
    #     points = [0] + sorted(points) + [100]  # 排个队
    #     points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
    #     end_demand = demands_i['end'][0]
    #     end = [round(points[i] * end_demand) for i in range(length - 1)]
    #     end.append(end_demand - sum(end))
    #     return end
    def random_start(length, demands_i, rate, len_rate):
        points = [randint(0, 100) for i in range(length - 1)]  # 生成几个随机点
        points = [0] + sorted(points) + [100]  # 排个队
        points = [(points[i + 1] - points[i]) / 100 for i in range(length - 1)]
        start_demand = demands_i['start'][0] * (1 - rate/len_rate)
        end_demand = demands_i['end'][0] * (1 - rate/len_rate)
        start = [round(points[i] * start_demand) for i in range(length - 1)]
        end = [round(points[i] * end_demand) for i in range(length - 1)]
        start.append(start_demand - sum(start))
        end.append(end_demand - sum(end))
        return start, end

    def station_init_bikes(reset_bikes, data, list, capacity_i):
        # data.loc[list, 'bikes'] = round(capacity_i * ((reset_bikes+1) / 20))  # 所有站点比例一致
        data.loc[list, 'bikes'] = round(capacity_i * randint(0, 100) / 100)  # 所有站点比例一致
        # data.loc[list, 'bikes'] = capacity_i.apply(lambda x: round(x * randint(0, 100) / 100))  # 站点比例不一致
        return data

    # stations['bikes'] = round(stations['capacity'] * 0.5)  # 设置车子数量
    zone_list = demand.drop(demand[demand[['zone']].duplicated()].index, axis=0)['zone']  # 区域列
    gap_sum, start_demand_sum, end_demands_sum = 0, 0, 0  # 统计缺口总量, 满足的借车需求量, 满足的还车需求量
    stop_list = []
    for index, z in enumerate(zone_list):
        zone_data = demand[demand['zone'] == z]  # 依此读取每个区域的数据
        stations_list = list(zone[zone['zone'] == z]['id'])  # 获取该区域站点的id
        length_stations = len(stations_list)  # 获取该区域站点的数量
        stations_copy = stations.copy()
        round2 = 20
        for reset_demands in range(round2):  # 寻找可行初始解的次数
            stop = 0
            start_demands_copy, end_demands_copy, gap_sum_copy = 0, 0, 0
            for day in range(time):
                if (day+1) not in list(zone_data['day']):
                    continue
                day_demand = zone_data[zone_data['day'] == (day+1)].reset_index(drop=True)
                capacity = stations_copy.loc[stations_list]['capacity']  # 获取区域内站点的容量
                bikes = stations_copy.loc[stations_list]['bikes']  # 获取区域内站点的车子数量
                for time_1 in range(100):
                    # day_demand = pd.Series(day_demand)
                    print('round1:', time_i, 'zone:', z, "%:", (index, len(zone_list)),  'round2', reset_demands, 'day:', day + 1, time_1,)
                    start_demands, end_demands = random_start(length_stations, day_demand, reset_demands, round2)
                    # start_demands = random_start(length_stations, day_demand)  # 分配区域借车量
                    # end_demands = random_end(length_stations, day_demand)  # 分配区域借车量
                    judge = start_demands <= bikes + end_demands
                    judge_i = end_demands <= capacity - bikes + start_demands
                    if judge[judge == True].sum() == length_stations and \
                            judge_i[judge_i == True].sum() == length_stations:
                        break
                    elif time_1 == 99:
                        stop = 1
                if stop == 1:
                    stations_copy = stations.copy()
                    # stations_copy = station_init_bikes(reset_bikes, stations_copy, stations_list, capacity)
                    break
                else:
                    gap = [end_demands[i] - start_demands[i] for i in range(length_stations)]
                    stations_copy.loc[stations_list, 'bikes'] = bikes + gap
                    start_demands = sum(start_demands)
                    end_demands = sum(end_demands)
                    gap = [abs(i) for i in gap]
                    start_demands_copy += start_demands
                    end_demands_copy += end_demands
                    gap_sum_copy += sum(gap)
                    stop = 2
            if reset_demands == (round2 - 1) :
                stop_list.append([index, stations_list, day])
            if stop == 2:
                start_demand_sum += start_demands_copy
                end_demands_sum += end_demands_copy
                gap_sum += gap_sum_copy
                stations = stations_copy
                break
    # print(stop_list)
    # print(gap_sum, start_demand_sum, end_demands_sum)
    return gap_sum, start_demand_sum, end_demands_sum










