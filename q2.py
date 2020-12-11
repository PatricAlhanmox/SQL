import psycopg2
import sys

def step1(d, numPart, alpPart):
    if numPart not in d:
        d[numPart] = {'alpPart':[alpPart]}
    else: 
        d[numPart]['alpPart'].append(alpPart)        
    

dbname = "a3"
conn = psycopg2.connect('dbname = a3')

cur = conn.cursor()
query = "select DISTINCT s1.backend, left(s.code, 4), s1.counter from (select right(code, 4) as backend, count(code) as counter from subjects group by backend having count(code) > 1 and count(code) < 11 order by backend) s1 join subjects s on right(s.code, 4)=s1.backend group by left(s.code, 4), s1.backend, s1.counter order by s1.backend;"
cur.execute(query)
argc = len(sys.argv)
dicTot = {}

if argc == 1:
    for tup in cur.fetchall():
        if tup[2] == 2:
            step1(dicTot, tup[0], tup[1])
elif argc == 2:
    for tup in cur.fetchall():
        if tup[2] == int(sys.argv[1]):
            step1(dicTot, tup[0], tup[1])
for key,value in sorted(dicTot.items()):
    string = " ".join(value['alpPart'])
    print("{}: {}".format(key,string))
conn.close()                
