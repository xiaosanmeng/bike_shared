import pandas as pd
# 清洗数据，删去了4个站点不在出发集合的站点，38条出行记录
cb = pd.DataFrame(pd.read_csv('F:/bikedata/citi/201903-citibike-tripdata.csv', parse_dates=['starttime']))
cb['day'] = cb['starttime'].apply(lambda x: x.day)
cb_i = cb[['start station id', 'end station id', 'day']]\
    .rename(columns={'start station id': 'start', 'end station id': 'end'})
stations_i = pd.DataFrame()
stations_i['id'], stations_i['true'] = list(set(list(cb_i['start'])) & set(list(cb_i['end'])))
cb_i = pd.merge(cb_i, stations_i.rename(columns={'id': 'start'}), how='left', on='start')
cb_i = pd.merge(cb_i, stations_i.rename(columns={'id': 'end', 'true': 'true1'}), how='left', on='end')
cb_i = cb_i[(cb_i['true'] == 1) & (cb_i['true1'] == 1)][['start', 'end', 'day']].reset_index(drop=True)
# cb_i.to_csv('F:/bikedata/bike_datas/test/stations_day_demands.csv', index=None)

# 转换为区域间的出行数据
zone = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
    columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
zone_demands = pd.merge(cb_i, zone.rename(columns={'id': 'start'}), how='left', on='start')\
    .rename(columns={'zone': 'start zone'})
zone_demands = pd.merge(zone_demands, zone.rename(columns={'id': 'end'}), how='left', on='end')\
    .rename(columns={'zone': 'end zone'})
zone_demands = zone_demands[['start zone', 'end zone', 'day']]\
    .rename(columns={'start zone': 'start', 'end zone': 'end'})
# zone_demands.to_csv('E:/python/shared_bikes/main_code/datas/zone_demands_day.csv', index=None)

# 按天统计
zone_demands_i = pd.DataFrame()
for day in range(31):
    print(day)
    day_demands = zone_demands[zone_demands['day'] == day + 1]
    day_demands = day_demands.groupby(['start', 'end']).count().reset_index().rename(columns={'day': 'demands'})
    day_demands['day'] = day + 1
    zone_demands_i = pd.concat([zone_demands_i, day_demands])
zone_demands = zone_demands_i.reset_index(drop=True)
zone_demands['t'] = 0
zone_demands.t[zone_demands.start == zone_demands.end] = 1
zone_demands = zone_demands[zone_demands['t'] == 0]
del zone_demands['t']
zone_demands.to_csv('E:/python/shared_bikes/main_code/datas/zone_demands_day_new.csv', index=None)











# 统计站点每天的借还需求量
# start_count = cb.groupby(['start station id', 'day']) \
#     .count().reset_index().rename(columns={'start station id': 'id', 'starttime': 'start'})[['id', 'day', 'start']]
# end_count = cb.groupby(['end station id', 'day']) \
#     .count().reset_index().rename(columns={'end station id': 'id', 'stoptime': 'end'})[['id', 'day', 'end']]
# station_demands = pd.merge(start_count, end_count, how='outer', on=['id', 'day'])
# station_demands.to_csv('F:/bikedata/bike_datas/test/station_day.csv', index=None)

# 统计区域每天的借还需求量
# zone = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
#     columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
# station_demands = pd.merge(station_demands, zone, how='left', on='id')
# zone_demands = station_demands.groupby(['zone', 'day'])['start', 'end'].sum().reset_index()
# zone_stations = zone.groupby('zone').count().reset_index().rename(columns={'id': 'count_stations'})
# zone_demands = pd.merge(zone_demands, zone_stations, how='left', on='zone')
# zone_demands.to_csv('F:/bikedata/bike_datas/test/zone_day.csv', index=None)

# 创建站点进出空表
station_list = list(zone['id'])  # 新站点从此处append
stations_gap = pd.DataFrame()

# for i in range(31):
#     stations_i = pd.DataFrame()
#     stations_i['id'] = station_list
#     stations_i['day'] = i+1
#     stations_gap = pd.concat([stations_gap, stations_i])
# stations_gap = stations_gap.sort_values(by=['id', 'day'])
# stations_gap['start'] = 0
# stations_gap['end'] = 0
# stations_gap.to_csv('F:/bikedata/bike_datas/test/empty.csv', index=None)
#
#
# # 统计区域每小时的借还需求量
# cb = pd.DataFrame(pd.read_csv('F:/bikedata/citi/201903-citibike-tripdata.csv', parse_dates=['starttime']))
# cb['day'] = cb['starttime'].apply(lambda x: x.day)
# cb['hour'] = cb['starttime'].apply(lambda x: x.hour)
# start_count = cb.groupby(['start station id', 'day', 'hour']).count().reset_index().\
#     rename(columns={'start station id': 'id', 'starttime': 'start'})[['id', 'day', 'hour', 'start']]
# end_count = cb.groupby(['end station id', 'day', 'hour']).count().reset_index().\
#     rename(columns={'end station id': 'id', 'stoptime': 'end'})[['id', 'day', 'hour', 'end']]
# station_demands = pd.merge(start_count, end_count, how='outer', on=['id', 'day', 'hour']).fillna(0)
#
# zone = pd.read_csv('F:/bikedata/bike_datas/station_datas.csv').rename(
#     columns={'station_id': 'id', 'zone_id': 'zone'})[['id', 'zone']]
# station_demands = pd.merge(station_demands, zone, how='left', on='id')
# zone_demands = station_demands.groupby(['zone', 'day', 'hour'])['start', 'end'].sum().reset_index()
# zone_demands.to_csv('F:/bikedata/bike_datas/test/zone_hour.csv', index=None)
