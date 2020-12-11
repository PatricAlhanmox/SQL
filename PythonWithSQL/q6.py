import psycopg2
import sys
    
   
dbname = 'a3'
conn = psycopg2.connect('dbname=a3')
cur = conn.cursor()
cur1 = conn.cursor()
query = 'select id, weeks from meetings'
cur.execute(query)

for tup in cur.fetchall():
    temp = str(tup[1]).split(',')
    
    lisTot = []
    for i in range (11):
        lisTot.append('0')
        
    for m in temp:
        if 'N' in m or '<' in m:
            lisTot = '00000000000'
        else:
            if '-' in m:
                y = m.split('-')
                for j in range(int(y[0]), int(y[1])+1):
                    lisTot[int(j)-1] = '1'
            elif '-' not in m:
                lisTot[int(m)-1] = '1'
    Final = "update meetings set weeks_binary=\'" + ''.join(lisTot) + "\'"+" where id = " + str(tup[0]) + ";"
    cur1.execute(Final)
    
conn.commit()
cur.close()
cur1.close()
conn.close()
