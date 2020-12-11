import psycopg2
import sys

def add_items(d, term, course, number):
    if term not in d:
        d[term] = {'code':[]}
        d[term]['code'].append((course,number))
    else:
        d[term]['code'].append((course,number))

dbname = 'a3'
conn = psycopg2.connect('dbname=a3')
cur = conn.cursor()
query = "select t.name, s.code, s1.Num from (select course_id, count(person_id) as Num from course_enrolments group by course_id) s1, subjects as s, courses as c, terms as t where c.subject_id=s.id and s1.course_id=c.id and c.term_id=t.id group by t.name, s.code, s1.Num  order by t.name, s.code;"
cur.execute(query)
argc = len(sys.argv)
dicTot = {}
if argc == 1:
    for tup in cur.fetchall():
        if str(tup[1]).startswith('ENGG'):
            add_items(dicTot, tup[0], tup[1], tup[2])
else:
    for tup in cur.fetchall():
        if str(tup[1]).startswith(sys.argv[1]):
            add_items(dicTot, tup[0], tup[1], tup[2])
            
for key, value in sorted(dicTot.items()):
        y = list(dicTot[key]['code'])
        if y:
            print('{}'.format(key))
            a,b = [list(i) for i in zip(*y)]
            for i in range(len(a)):
                print(' '+a[i]+'('+str(b[i])+')')
           
          

