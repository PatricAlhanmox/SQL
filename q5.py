import psycopg2
import sys

def add_items(dicTot, classes, classType, classTag, nEnrol):
    if classes not in dicTot:
        dicTot[classes] = []
        dicTot[classes].append((classType, classTag, nEnrol))
    else:
        dicTot[classes].append((classType, classTag, nEnrol))

dbname = 'a3'
conn = psycopg2.connect('dbname=a3')
cur = conn.cursor()
query = "select s.code, ct.name, cl.tag, cast(s1.nEnrol*1./cl.quota*100 as int) from ( select DISTINCT class_id, count(person_id) as nEnrol from class_enrolments group by class_id order by nEnrol ) as s1, courses as c, classes as cl, classtypes as ct, subjects as s where s1.class_id=cl.id and cl.course_id=c.id and cl.type_id=ct.id and c.term_id=5199 and c.subject_id=s.id and cl.quota>0 group by s.code, ct.name, cl.tag, cast(s1.nEnrol*1./cl.quota*100 as int) having cast(s1.nEnrol*1./cl.quota*100 as int) < 50;"
cur.execute(query)
argc = len(sys.argv)
dicTot = {}
if argc == 1:
    for tup in cur.fetchall():
        if tup[0] == 'COMP1521':
            add_items(dicTot, tup[0], tup[1], tup[2], tup[3])
            y = dicTot[tup[0]]
            if y:
                a,b,c = [list(i) for i in zip(*y)]   
else:
    for tup in cur.fetchall():
        if tup[0] == sys.argv[1]:
            add_items(dicTot, tup[0], tup[1], tup[2], tup[3])
            y = dicTot[tup[0]]
            if y:
                a,b,c = [list(i) for i in zip(*y)]

for i in range(len(a)):
    print(a[i]+' '+b[i]+' is '+str(c[i])+'% full')  


cur.close()
conn.close()
