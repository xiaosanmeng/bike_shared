import pandas as pd
import numpy as np
from random import randint
from re_32_object import object
import time
import matplotlib.pyplot as plt
import random

# 读取区域需求量
demand_i = pd.read_csv('F:/bikedata/bike_datas/test/zone_day.csv')
# 读取区域包含的站点信息
zone_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
    columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
# 读取站点信息
stations_i = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv')[['station_id', 'capacity']].\
    rename(columns={'station_id': 'id'})




def main(demand, zone, stations, day, re_times):


    # 构建新站点
    new_zone = pd.DataFrame()
    new_stations_i = pd.DataFrame()
    zone_count_stations = zone.groupby(['zone'])['id'].count().reset_index().rename(columns={'id': 'count_stations'}) # 统计每个区域的站点数量

    # 设置每个区域新站点的容量（取平均）
    zone_capacity = pd.merge(stations, zone, how='left', on='id')
    zone_capacity = zone_capacity.groupby('zone')['capacity'].sum().reset_index()
    zone_capacity = pd.merge(zone_capacity, zone_count_stations, how='left', on='zone')
    zone_capacity['capacity'] = round(zone_capacity['capacity'] / zone_capacity['count_stations'])

    # 新站点构建
    new_zone['zone'] = zone.drop(zone[zone[['zone']].duplicated()].index, axis=0)['zone']
    new_zone['id'] = new_zone['zone'].apply(lambda x: int(str(x)[::]))
    new_stations_i['id'] = new_zone['id']
    new_stations_i = pd.merge(new_stations_i, zone_capacity[['zone', 'capacity']],
                            how='left', left_on='id', right_on='zone')[['id', 'capacity']]
    demand['gap'] = demand['end'] - demand['start']
    # 选取新站点
    best_object_sum = 10000000
    object_list = []
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
        stations_i = stations_i.set_index('id')

        # y1 = []
        # y2 = []

        # best_object = 1000000
        # best_zone = pd.DataFrame()
        # for time_i in range(re_times):
        #     re_bikes = object(time_i, demand, zone_i, stations_i, zone_data_i, day)
        #     t = False
        #     if best_object >= re_bikes:
        #         best_object = re_bikes
        #         best_zone = zone_data_i.copy()
        #         t = True
        #     if t is False and np.random.rand() <= 0.1:
        #         zone_data_i['bikes'] = zone_data_i['capacity'].apply(lambda x: round(x * randint(0, 100) / 100))
        #     else:
        #         zone_data_i['bikes'] = best_zone['bikes'].apply(lambda x: round(x * randint(80, 120) / 100))
        #     print(time_i + 1, best_object)
        # return best_object
        re_bikes = object(1, demand, zone_i, stations_i, zone_data_i, day)
        return re_bikes

    def init(N):
        C = []
        for i in range(N):
            c = [random.randint(0, 1) for i in range(379)]
            C.append(c)
        return C

    def fitness(N):
        S = []  ##用于存储被选中的下标
        F = []  ## 用于存放当前该个体的最大价值
        for i in range(len(N)):
            f = 1 / GA_object(N[i])  # 价值
            S.append(i)
            F.append(f)
        return S, F

    def best_x(F):
        y = min(F)
        B = F.index(y)
        return B, y

    def rate(x):
        # 计算比率
        p = [0] * len(x)
        s = 0
        for i in x:
            s += i
        for i in range(len(x)):
            p[i] = x[i] / s
        return p

    ## 选择
    def chose(p, X, m, n):
        X1 = X
        r = np.random.rand(m)
        for i in range(m):
            k = 0
            for j in range(n):
                k = k + p[j]
                if r[i] <= k:
                    X1[i] = X[j]
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
            if k[u] and k[v]:
                # print(u,v)
                q = np.random.randint(n - 1)
                # print(q)
                for i in range(q + 1, n):
                    X[u][i], X[v][i] = X[v][i], X[u][i]
                k[u] = 0
                k[v] = 0
        return X

    ##变异
    def vari(X, m, n, p):
        for i in range(m):
            for j in range(n):
                q = np.random.rand()
                if q < p:
                    X[i][j] = np.random.randint(0, 2)

        return X
    m = 50  ##规模
    N = 800  ##迭代次数
    Pc = 0.8  ##交配概率
    Pm = 0.05  ##变异概率
    n = 379
    C = init(m)
    S, F = fitness(C)
    B, y = best_x(F)
    Y = [1/y]
    for i in range(N):
        p = rate(F)
        C = chose(p, C, m, n)
        C = match(C, m, n, Pc)
        C = vari(C, m, n, Pm)
        S, F = fitness(C)
        B1, y1 = best_x(F)
        B1 = sum(C[B1])
        if y1 > y:
            y = y1
        Y.append(1/y)
    # print("最大值为：", 1/y, '站点个数', B1)
    #
    # plt.plot(Y)
    # plt.show()


    return round(1/y), Y, B1



if __name__ == "__main__":
    start_time = time.time()
    re_bikes, object_list, stations_num = main(demand_i, zone_i, stations_i, 7, 1)
    end_time = time.time()
    print("最大值为：", re_bikes, '站点个数', stations_num)
    print('用时：%s s' % round(end_time - start_time))
    print('再平衡,7day,20-100')

    def DrawLinechart(y1,  title):
        x = range(len(y1))  # 生成0-10
        plt.plot(x, y1, c="R", label='common')
        # plt.plot(x, y2, c='B', label='best')
        plt.legend(loc='upper left')  # 图例的位置是左上
        plt.xlabel('round')  # X轴标签
        plt.ylabel('re_bikes')  # Y轴标签
        plt.title(title)  # 折线图标题
        plt.show()


    DrawLinechart(object_list,  're_bikes')
    # DrawLinechart(y1, bikes_best_list, 'bikes')

# 2151.0 [2273.0, 2236.0, 2211.0, 2151.0, 2162.0]

# 再平衡 原站点 10day
#  0.5 500轮  （50, 2190）
#  0.5 2000轮 （1200, 2175.0）

# 0.5 31day  100轮
# 新站点 20267.0
# 老站点 24828.0

# 0.5 7day  100轮
# 新站点 760
# 老站点 2212.0

# 0.5 14day 100轮
# 新站点   4671
# 老站点 7807
# 0.5 14day 2000轮
# 新站点   （170  4641.0）
# 老站点 （7507   503.0）

# 40  832.0  50 741.0  60 610.0