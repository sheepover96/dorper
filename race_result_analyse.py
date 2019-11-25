# %%

from sqlalchemy.sql import text

from models import RaceResult, RacerInfo, RaceInfo, RaceOdds
from utils.setting import session

year = 2014

race_result_list17 = session.query(RaceResult).filter(RaceResult.year==year)
race_info_list17 = session.query(RaceInfo).filter(RaceInfo.year==year)
race_odds_list17 = session.query(RaceOdds).filter(RaceOdds.year==year)
racer_info_list16 = session.query(RacerInfo).filter(RacerInfo.year==2016)

#race_result_with_info = session.execute('select * from race_result inner join race_info on\
#                race_result.race_num = race_info.race_num and race_result.year=race_info.year\
#                where race_result. year={} and is_race_no_flying=1 and is_race_times_record_valid=1 order by race_num, pitout_lane;'.format(year))

# %%
race_result_with_info = session.query(RaceResult, RaceInfo)\
                                .filter(RaceResult.race_num==RaceInfo.race_num,\
                                        RaceResult.year==RaceInfo.year, RaceResult.year==year,\
                                        RaceInfo.is_race_no_flying==1, RaceInfo.is_race_times_record_valid==1)\
                                        .order_by(RaceResult.race_num, RaceResult.pitout_lane)

#%%
import matplotlib.pyplot as plt
#race result analysis
# pitout_lane to rank
pitout_lane_axis = []
rank_counts = []
rank_set = set([i for i in range(1,7)])
for pl in range(1,7):
    pl_race_result = race_result_list17.filter(RaceResult.pitout_lane==pl).all()
    rank_count = [0 for i in range(7)]
    for data in pl_race_result:
        result_rank = data.rank
        if not result_rank in rank_set:
            result_rank = 7
        rank_count[result_rank-1] += 1
    count_num = sum(rank_count)
    rank_count_norm = list(map(lambda x: x/count_num, rank_count))
    pitout_lane_axis.extend([pl for i in range(7)])
    rank_counts.extend(rank_count_norm)

colorlist = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#f070f0', '#007f00'] * (6)
plt.bar(range(len(rank_counts)), rank_counts, tick_label=pitout_lane_axis, color=colorlist)
plt.savefig('imgs/pitoutlane_to_rank.png')

#%%

# when racer in except 1st lane win?

wind_direction_dic = {}
wind_strength_dic = {}
weather_dic = {}
wave_height_dic = {}
lane_length_dic = {}

wind_direction_count = 0
wind_strength_count = 0
weather_count = 0
wave_height_count = 0
lane_length_count = 0

race_result_second_lane_rank1 = race_result_with_info.filter(RaceResult.pitout_lane==2, RaceResult.rank==1)
for race_result, race_info in race_result_second_lane_rank1.all():
    if not race_info.wind_direction in wind_direction_dic:
        wind_direction_dic[race_info.wind_direction] = wind_direction_count
        wind_direction_count += 1

    if not race_info.wind_strength in wind_strength_dic:
        wind_strength_dic[race_info.wind_strength] = wind_strength_count
        wind_strength_count += 1

    if not race_info.weather in weather_dic:
        weather_dic[race_info.weather] = weather_count
        weather_count += 1

    if not race_info.wave_height in wave_height_dic:
        wave_height_dic[race_info.wave_height] = wave_height_count
        wave_height_count += 1

    if not race_info.lane_length in lane_length_dic:
        lane_length_dic[race_info.lane_length] = lane_length_count
        lane_length_count += 1

#%%
# 複勝率の調査
import matplotlib.pyplot as plt
from sqlalchemy import or_, and_
nrace = race_result_with_info.filter(RaceResult.pitout_lane==1).count()
count = 0
race_num_list = []
race_result_double_win = race_result_with_info.filter(or_(and_(RaceResult.pitout_lane==1, RaceResult.rank==2), and_(RaceResult.pitout_lane==1, RaceResult.rank==1))).all()
for race_result, race_info in race_result_double_win:
    if not race_result.race_num in race_num_list:
        race_num_list.append(race_result.race_num)
        count += 1
print(count/nrace)

#%%
# 二連単率の調査
from sqlalchemy import or_, and_
nrace = race_result_with_info.filter(RaceResult.pitout_lane==1).count()
count = 0
race_num_dic = {}
race_result_double_win = race_result_with_info.filter(or_(and_(RaceResult.pitout_lane==1, RaceResult.rank==1), and_(RaceResult.pitout_lane==2, RaceResult.rank==2))).all()
for race_result, race_info in race_result_double_win:
    if not race_result.race_num in race_num_dic:
        race_num_dic[race_result.race_num] = 1
    else:
        race_num_dic[race_result.race_num] += 1
        count += 1
print(count/nrace)

#%%
# 二連複の調査
import matplotlib.pyplot as plt
from sqlalchemy import or_
nrace = race_result_with_info.filter(RaceResult.pitout_lane==1).count()
count = 0
race_num_dic = {}
race_result_double_win = race_result_with_info.filter(or_(and_(RaceResult.pitout_lane==1, RaceResult.rank==2), and_(RaceResult.pitout_lane==1, RaceResult.rank==1), and_(RaceResult.pitout_lane==2, RaceResult.rank==1), and_(RaceResult.pitout_lane==2, RaceResult.rank==2))).all()
for race_result, race_info in race_result_double_win:
    if not race_result.race_num in race_num_dic:
        race_num_dic[race_result.race_num] = 1
    else:
        race_num_dic[race_result.race_num] += 1
        count += 1
print(count/nrace)

#%%
# 三連単の調査
import matplotlib.pyplot as plt
from sqlalchemy import or_
nrace = race_result_with_info.filter(RaceResult.pitout_lane==1).count()
count = 0
race_num_dic = {}
race_result_double_win = race_result_with_info.filter(or_(and_(RaceResult.pitout_lane==1, RaceResult.rank==1), and_(RaceResult.pitout_lane==2, RaceResult.rank==2), and_(RaceResult.pitout_lane==3, RaceResult.rank==3))).all()
for race_result, race_info in race_result_double_win:
    if not race_result.race_num in race_num_dic:
        race_num_dic[race_result.race_num] = 1
    elif race_num_dic[race_result.race_num] == 1:
        race_num_dic[race_result.race_num] += 1
    else:
        count += 1

print(count/nrace)

#%%
# 三連複の調査
import matplotlib.pyplot as plt
from sqlalchemy import or_
nrace = race_result_with_info.filter(RaceResult.pitout_lane==1).count()
count = 0
race_num_dic = {}
race_result_double_win = race_result_with_info.filter(or_(and_(RaceResult.pitout_lane==1, RaceResult.rank==1),\
    and_(RaceResult.pitout_lane==1, RaceResult.rank==2), and_(RaceResult.pitout_lane==1, RaceResult.rank==3),\
    and_(RaceResult.pitout_lane==2, RaceResult.rank==1), and_(RaceResult.pitout_lane==2, RaceResult.rank==2),\
    and_(RaceResult.pitout_lane==2, RaceResult.rank==3),and_(RaceResult.pitout_lane==3, RaceResult.rank==1),\
    and_(RaceResult.pitout_lane==3, RaceResult.rank==2),and_(RaceResult.pitout_lane==3, RaceResult.rank==3))).all()
for race_result, race_info in race_result_double_win:
    if not race_result.race_num in race_num_dic:
        race_num_dic[race_result.race_num] = 1
    elif race_num_dic[race_result.race_num] == 1:
        race_num_dic[race_result.race_num] += 1
    else:
        count += 1

print(count/nrace)

#%%
# wind strength affects
import matplotlib.pyplot as plt
race_result_part = race_result_with_info.filter(RaceResult.pitout_lane==1, RaceResult.rank!=1)
wscounts = []
for key in sorted(wind_strength_dic.keys()):
    count = race_info_list17.filter(RaceInfo.wind_strength==key).count()
    wscounts.append(len(race_result_part.filter(RaceInfo.wind_strength==key).all())/count)
    print(key, count)
plt.bar(range(len(wscounts)), wscounts, tick_label=sorted(wind_strength_dic.keys()))
plt.savefig('imgs/wind_strength_1lane_1st15.png')


#%%
import matplotlib.pyplot as plt
race_result_part = race_result_with_info.filter(RaceResult.pitout_lane==1, RaceResult.rank!=1)
wscounts = []
for key in weather_dic.keys():
    count = race_info_list17.filter(RaceInfo.weather==key).count()
    wscounts.append(len(race_result_part.filter(RaceInfo.weather==key).all())/count)
plt.bar(range(len(wscounts)), wscounts, tick_label=['sunny', 'cloudy', 'rain', 'snow'])
plt.savefig('imgs/weather_affects_1lane_not1st.png')
print(weather_dic.keys())



#%%
import matplotlib.pyplot as plt
race_result_part = race_result_with_info.filter(RaceResult.pitout_lane==1, RaceResult.rank!=1)
wscounts = []
for key in lane_length_dic.keys():
    count = race_info_list17.filter(RaceInfo.lane_length==key).count()
    wscounts.append(len(race_result_part.filter(RaceInfo.lane_length==key).all())/count)
plt.bar(range(len(wscounts)), wscounts, tick_label=lane_length_dic.keys())
plt.savefig('imgs/lane_length_affects_1lane_not1st.png')


#%%
import matplotlib.pyplot as plt
race_result_part = race_result_with_info.filter(RaceResult.pitout_lane==1, RaceResult.rank!=1)
wscounts = []
for key in sorted(wave_height_dic.keys()):
    count = race_info_list17.filter(RaceInfo.wave_height==key).count()
    wscounts.append(len(race_result_part.filter(RaceInfo.wave_height==key).all())/count)
    print(key, count)
plt.bar(range(len(wscounts)), wscounts, tick_label=sorted(wave_height_dic.keys()))
plt.savefig('imgs/wave_height_1lane_not1st14.png')

#%%
race_result_with_info_and_racer = session.query(RaceResult, RaceInfo, RacerInfo)\
                                .filter(RaceResult.race_num==RaceInfo.race_num,\
                                        RaceResult.year==RaceInfo.year, RaceResult.year==year,RacerInfo.year==(year-1),\
                                        RaceResult.racer_id==RacerInfo.racer_id, RacerInfo.period==2,
                                        RaceInfo.is_race_no_flying==1, RaceInfo.is_race_times_record_valid==1)\
                                        .order_by(RaceResult.race_num, RaceResult.pitout_lane)

#race_result_with_info_and_racer = session.query(RaceResult, RaceInfo, RacerInfo)\
#                                .filter(RaceResult.race_num==RaceInfo.race_num,\
#                                        RaceResult.year==RaceInfo.year, RaceResult.year==year,\
#                                        RaceInfo.is_race_no_flying==1, RaceInfo.is_race_times_record_valid==1)\
#                                        .order_by(RaceResult.race_num, RaceResult.pitout_lane)

#%%

import matplotlib.pyplot as plt
#１位をとるracerのランクの分布とかを調べてみる

## 1位になる人の前年のスタートタイミング,複勝率
race_result_part2 = race_result_with_info_and_racer.filter(RaceResult.pitout_lane==5,RaceResult.rank==1)
rank_list = []
win_rate_list = []
double_win_rate_list = []
for race_result, race_info, racer_info in race_result_part2.all():
    win_rate_list.append(racer_info.racer_win_rate)
    double_win_rate_list.append(racer_info.racer_double_win_rate)


fig = plt.figure()
ax = fig.add_subplot(211)
ax.hist(win_rate_list, range=(0,1))
#ax.title('1lane_win_rate')

bx = fig.add_subplot(212)
bx.hist(double_win_rate_list, range=(0,1))
#bx.title('1lane_double_win_rate')

fig.savefig('imgs/5lane_rank1_winrate_and_double_winrate.png')
#%%
