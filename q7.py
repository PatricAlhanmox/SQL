import psycopg2
import sys
from collections import defaultdict
import collections


def convert_time(time):
    if time % 100 == 0:
        sums = time / 100
    else:
        x = (time // 100)*1.0
        y = (time % 100) / 60
        sums = x + y
    return sums
    
   
def add_count(weeks_binary):
    A = list(weeks_binary)
    del A[-1]
    x = A.count('1')
    return x

'''
def common_member(a, b):
    count = 0 
    for i in range(len(a)):
        if a[i] == b[i] and a[i] == '1':
            count += 1
    return count
'''    

def add_dic(weekDic, room, day, stime, etime, wbinary):
    A = list(wbinary)
    del A[-1]
    if room not in weekDic:
        weekDic[room] = {day:[]}
        if day not in weekDic[room]:
            weekDic[room][day] = []
            weekDic[room][day].append((stime, etime, A))
        else:
            if (stime, etime, A) not in weekDic[room][day]:
                weekDic[room][day].append((stime, etime, A))
    else:
        if day not in weekDic[room]:
            weekDic[room][day] = []
            weekDic[room][day].append((stime, etime, A))
        else:
            if (stime, etime, A) not in weekDic[room][day]:
                weekDic[room][day].append((stime, etime, A))
        # Superkey must be in cadidate key

dbname = 'a3'
conn = psycopg2.connect('dbname=a3')
cur = conn.cursor()
cur1 = conn.cursor()
query1 = "select r.code, t.name, m.day, m.start_time, m.end_time, m.weeks_binary from courses as c, classes as cl, rooms as r, terms as t, meetings as m where c.term_id=t.id and cl.course_id=c.id and cl.id=m.class_id and m.room_id=r.id and r.code ILIKE 'K-%' order by r.code, m.start_time, m.end_time;"
query2 = "select count(DISTINCT code) as counter from rooms where code ILIKE 'K-%'"
cur.execute(query1)
cur1.execute(query2)



totalRooms = cur1.fetchone()

valid_room = 0
timeDic = defaultdict(float)
weekDic = {}
argc = len(sys.argv)

for tup in cur.fetchall():
    if argc == 1:
        if tup[1] == '19T1':
            add_dic(weekDic, tup[0], tup[2], tup[3], tup[4], tup[5])
            K = list(tup[5])
            del K[-1]
            if (tup[3], tup[4], K) in weekDic[tup[0]][tup[2]]:
                timeDic[tup[0]] = timeDic[tup[0]] + (convert_time(tup[4]) - convert_time(tup[3])) * add_count(tup[5])
                
    else:
        if sys.argv[1] == tup[1]:
            add_dic(weekDic, tup[0], tup[2], tup[3], tup[4], tup[5])
            K = list(tup[5])
            del K[-1]
            if (tup[3], tup[4], K) in weekDic[tup[0]][tup[2]]:
                timeDic[tup[0]] = timeDic[tup[0]] + (convert_time(tup[4]) - convert_time(tup[3])) * add_count(tup[5])
            
for i in timeDic.values():
    if i >= 200:
        valid_room += 1

  
'''
value_occurrences = collections.Counter(a)
print(value_occurrences)

            add_dic(weekDic, tup[0], tup[2], tup[3], tup[4], tup[5])
            y = weekDic[tup[0]]
            a, b, c, d = [list(i) for i in zip(*y)]
            

            if value_occurrences > 1:
                check_weekBinary(t[i][5])
                subtract_time()
        print(value_occurrences)
            

print(valid_room)
print(weekDic)
print('=========================================================================')
print(timeDic)   
print('=========================================================================') 
'''   
P = str(round((1 - valid_room / totalRooms[0]) * 100, 1)) + "%"
print(P) 
