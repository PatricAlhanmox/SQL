import psycopg2
import sys

def add_items(d, building, courseCode):
    if building not in d:
        d[building] = {'code':[]}
        d[building]['code'].append(courseCode)
    elif courseCode in d[building]['code']:
        pass
    else:
        d[building]['code'].append(courseCode)
    

dbname = 'a3'
conn = psycopg2.connect('dbname=a3')
cur = conn.cursor()
query = "select b.name, sub.code from courses as cou, subjects as sub, classes as cla, meetings as m, rooms as r, buildings as b where cou.term_id = 5196 and cou.subject_id=sub.id and cla.course_id=cou.id and m.class_id=cla.id and r.id=m.room_id and b.id=r.within order by b.name;"
cur.execute(query)
argc = len(sys.argv)
dicTot = {}
if argc == 1:
    for tup in cur.fetchall():
        if str(tup[1]).startswith('ENGG'):
            add_items(dicTot, tup[0], tup[1])
    for n in sorted(dicTot):
        print(n)
        for c in sorted(dicTot[n]['code']):
            print(" " + c) 
else:
    for tup in cur.fetchall():
        if str(tup[1]).startswith(sys.argv[1]):
            add_items(dicTot, tup[0], tup[1])
    for n in sorted(dicTot):
        print(n)
        for c in sorted(dicTot[n]['code']):
            print(" " + c) 
       
