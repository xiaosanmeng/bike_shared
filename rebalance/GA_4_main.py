import pandas as pd
import numpy as np
from random import randint
from re_4_object import object, set_bikes
import time
import matplotlib.pyplot as plt
import random


def main(demand, zone, stations, distance, day, re_times, stations_type, new_stations_num):
    # 构建新站点
    new_zone = pd.DataFrame()
    new_stations_i = pd.DataFrame()
    new_stations = pd.DataFrame()
    zone_count_stations = zone.groupby(['zone'])['id'].count().reset_index().rename(columns={'id': 'count_stations'}) # 统计每个区域的站点数量

    # 设置每个区域新站点的容量（取平均）
    zone_capacity = pd.merge(stations, zone, how='left', on='id')
    zone_capacity = zone_capacity.groupby('zone')['capacity'].sum().reset_index()
    zone_capacity = pd.merge(zone_capacity, zone_count_stations, how='left', on='zone')
    # zone_capacity['capacity'] = 60
    zone_capacity['capacity'] = round(zone_capacity['capacity'] / zone_capacity['count_stations'])
    demand['gap'] = demand['end'] - demand['start']

    # 新站点构建
    new_zone['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index, axis=0)['zone']
    new_zone['id'] = new_zone['zone'].apply(lambda x: int(str(x)[::]))
    new_stations_i['id'] = new_zone['id']
    new_stations_i = pd.merge(new_stations_i, zone_capacity[['zone', 'capacity']],
                            how='left', left_on='id', right_on='zone')[['id', 'capacity']]
    # 选取新站点
    best_object = 1000000
    object_list = []
    #

    y1 = []
    y2 = []
    def GA_object(c):
        new_stations_i['t'] = c
        new_stations = new_stations_i[new_stations_i['t'] == 1][['id', 'capacity']]
        stations_i = pd.concat([stations, new_stations])  # 加入新站点
        zone_i = pd.concat([new_zone, zone], sort=True)  # 加入新站点
        zone_data_i = pd.merge(stations_i, zone_i, how='left', on='id')
        zone_data_i = zone_data_i.groupby('zone')['capacity'].sum().reset_index()
        zone_data_i['bikes'] = round(zone_data_i['capacity'] * 0.5)
        zone_data_i = set_bikes(demand, zone_data_i)
        stations_i = stations_i.set_index('id')

        # 确定车子数量分割线
        re_bikes = object(1, demand, zone_i, stations_i, zone_data_i, distance, day)
        return re_bikes

        # y1 = []
        # y2 = []
        #
        #
        # best_object = 1000000
        # best_zone = pd.DataFrame()
        # for time_i in range(100):
        #     re_bikes = object(time_i, demand, zone_i, stations_i, zone_data_i, distance, day)
        #     t = False
        #     if best_object >= re_bikes:
        #         best_object = re_bikes
        #         best_zone = zone_data_i.copy()
        #         t = True
        #     if t is False and np.random.rand() <= 0.1:
        #         zone_data_i['bikes'] = zone_data_i['capacity'].apply(lambda x: round(x * randint(0, 100) / 100))
        #     else:
        #         zone_data_i['bikes'] = best_zone['bikes'].apply(lambda x: round(x * randint(80, 120) / 100))
        #     print(j+1, time_i + 1, best_object)
        #
        #     # y1.append(re_bikes)
        #     # y2.append(best_object)
        # if best_object_sum > best_object:
        #     best_object_sum = best_object
        # y1.append(best_object)
        # y2.append(best_object_sum)

    def init(N, new_stations_num):
        C = []
        for i in range(N):
            c = [1] * new_stations_num + [0] * (379 - new_stations_num)
            random.shuffle(c)
            # c = [random.randint(0, 1) for i in range(379)]
            C.append(c)
        return C

    def fitness(N):
        S = []  ##用于存储被选中的下标
        F = []  ## 用于存放当前该个体的最大价值
        for i in range(len(N)):
            f = GA_object(N[i])  # 价值
            S.append(i)
            F.append(f)
        return S, F

    def best_x(F, m):
        y = min(F)
        B = F.index(y)
        y1 = sum(F)/m
        return B, y, y1

    def rate(x):
        # 计算比率
        p = [0] * len(x)
        s = 0
        normal = max(x) - min(x)
        t = [(max(x)-i)/normal for i in x]
        s = sum(t)
        for i in range(len(t)):
            p[i] = t[i] / s
        return p

    ## 选择
    def chose(p, X, m, n):
        X1 = X.copy()
        r = np.random.rand(m)
        for i in range(m):
            k = 0
            for j in range(m):
                k = k + p[j]
                if r[i] <= k:
                    X1[i] = X[j].copy()
                    break
        return X1

    ##交叉
    def match(X, m, n, p):
        r = np.random.rand(m)
        k = [0] * m
        for i in range(m):
            if r[i] < p:
                k[i] = 1
        u = v = 0
        k[0] = k[0] = 0
        for i in range(m):
            if k[i]:
                if k[u] == 0:
                    u = i
                elif k[v] == 0:
                    v = i
            # if k[u] and k[v]:
            #     # print(u,v)
            #     q = np.random.randint(n - 1)
            #     # print(q)
            #     for i in range(q + 1, n):
            #         X[u][i], X[v][i] = X[v][i], X[u][i]
            #     k[u] = 0
            #     k[v] = 0
            if k[u] and k[v]:  # 选择好两个基因，分别找到已建的站点索引位置，然后相互求差集，得到自己已建而对方未建的站点，继续交换
                u_index = [index for index, i in enumerate(X[u]) if i == 1]  # 找到为1的基因索引
                v_index = [index for index, i in enumerate(X[v]) if i == 1]
                u_i = list(set(u_index).difference(set(v_index)))  # 两个基因的索引组，相互求差集
                v_i = list(set(v_index).difference(set(u_index)))
                min_length = round(min(len(u_i), len(v_i))/2)  # 得到差集长度最少的索引组长度
                random.shuffle(u_i)
                random.shuffle(v_i)
                u_i = u_i[:min_length]
                v_i = v_i[:min_length]
                for i in u_i:  # 交换基因
                    X[u][i], X[v][i] = 0, 1
                for j in v_i:
                    X[u][j], X[v][j] = 1, 0
                # print(u,v)
        #         q = np.random.randint(n - 1)
        #         # print(q)
        #         for i in range(q + 1, n):
        #             X[u][i], X[v][i] = X[v][i], X[u][i]
        #         k[u] = 0
        #         k[v] = 0
        return X

    ##变异
    def vari(X, m, n, p):
        for i in range(m):
            build_index = [index for index, i in enumerate(X[i]) if i == 1]  # 找到为1的基因索引
            un_index = [index for index, i in enumerate(X[i]) if i == 0]
            for j in un_index:
                q = np.random.rand()
                if q < p:
                    z = random.choice(build_index)
                    X[i][j], X[i][z] = 1, 0
                    build_index.pop(build_index.index(z))

        return X
    m = 20  #规模
    N = 120  #迭代次数
    Pc = 0.8  #交配概率
    Pm = 0.02  #变异概率
    n = 379
    C = init(m, new_stations_num)
    S, F = fitness(C)
    B, y, y_mean = best_x(F, m)
    Y = [y]
    Y1 = [y_mean]
    for i in range(N):
        print('第%s代' % (i+1), '总共%s代' % N)
        p = rate(F)
        C = chose(p, C, m, n)
        C = match(C, m, n, Pc)
        C = vari(C, m, n, Pm)
        S, F = fitness(C)
        B1, y1, y1_mean = best_x(F, m)
        B1 = sum(C[B1])
        if y1 < y:
            y = y1
        Y.append(y)
        Y1.append(y1_mean)
        print([sum(i) for i in C])

    # print("最大值为：", 1/y, '站点个数', B1)
    #
    # plt.plot(Y)
    # plt.show()



    return y, Y, Y1, B1


def DrawLinechart(y1, y2, title):
    x = range(len(y1))  # 生成0-10
    plt.plot(x, y1, c="R", label='best')
    plt.plot(x, y2, c='B', label='average')
    plt.legend(loc='upper left')  # 图例的位置是左上
    plt.xlabel('round')  # X轴标签
    plt.ylabel('re_bikes')  # Y轴标签
    plt.title(title)  # 折线图标题
    plt.show()




if __name__ == "__main__":
    # 读取区域需求量
    re_bikes_list = []
    for i in range(10):
        demand_i = pd.read_csv('F:/bikedata/bike_datas/test/zone_day.csv')
        # 读取区域包含的站点信息
        zone_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
            columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
        # 读取站点信息
        stations_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv')[['station_id', 'capacity']]. \
            rename(columns={'station_id': 'id'})
        distance = pd.read_csv('F:/bikedata/bike_datas/zones_distance_matrix.csv')
        distance = distance.set_index('Unnamed: 0')

        start_time = time.time()
        stations_type = 1  # 0-原站点  1-加入新站点
        new_stations = 120  # 构建的新站点个数
        days = 7
        re_bikes, object_list, object_average_list, stations_num = main(demand_i, zone_i, stations_i, distance, days, 3000, stations_type, new_stations)
        end_time = time.time()
        print(re_bikes)
        print('用时：%s s' % round(end_time - start_time))
        if stations_type == 0:
            print('原站点')
        else:
            print('构建%s个新站点' % new_stations)
        re_bikes_list.append(re_bikes)
    print('20/60', re_bikes_list)

    # DrawLinechart(object_list, object_average_list, 're_bikes')
    # DrawLinechart(y1, bikes_best_list, 'bikes')

