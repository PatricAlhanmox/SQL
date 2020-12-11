import psycopg2
import sys

def add_items(dicTot, code, name, day, start_time, end_time, tag):
    if code not in dicTot:
        dicTot[code] = []
        dicTot[code].append((name, day, start_time, end_time, tag))
    else:
        dicTot[code].append((name, day, start_time, end_time, tag))


def sum_up(start, end):
    time = end - start
    if time % 100 == 0:
        sums = time*1.0 / 100
    else:
        x = time*1.0 / 100
        y = 1.0 * (time % 100) / 60
        sums = x + y
    return sums
    

def final_Hours(totalHours, subject, numDays, Daylist):
    n = 1
    for n in range(len(subject)):
        if 5*(n+1) <= len(subject):
            if subject[5*n - 3] not in Daylist:
                Daylist.append(subject[5*n - 3])
    numDays = len(Daylist)
    totalHours = totalHours + numDays*2
    return totalHours
    


dbname = 'a3'
conn = psycopg2.connect('dbname=a3')
cur = conn.cursor()
query = "select DISTINCT s.code, c.name, m.day, m.start_time, m.end_time, cl.tag from courses as co, terms as t, classes as cl, meetings as m, subjects as s, classtypes as c where co.term_id=t.id and s.id=co.subject_id and co.id=cl.course_id and c.id=cl.type_id  and m.class_id=cl.id and t.id = 5199 order by m.day, s.code, m.start_time;"
cur.execute(query)
argc = len(sys.argv)
dicTot = {}
numDays = 0
Daylist = []


for tup in cur.fetchall():
    if argc == 1:
        if tup[0] == 'COMP1511' or tup[0] == 'MATH1131':
            add_items(dicTot, tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
            if tup[0] == 'COMP1511' :
                fir_code = 'COMP1511'
                y = dicTot[tup[0]]
                a1,b1,c1,d1,e1 = [list(i) for i in zip(*y)]
            if tup[0] == 'MATH1131':
                z = dicTot[tup[0]]
                sec_code = tup[0]
                a2,b2,c2,d2,e2 = [list(i) for i in zip(*z)]


            
    elif argc == 2:
        if tup[0] == sys.argv[1]:
            fir_code = tup[0]
            add_items(dicTot, tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
            y = dicTot[tup[0]]
            a1,b1,c1,d1,e1 = [list(i) for i in zip(*y)] 
            
    elif argc == 3:
        if tup[0] == sys.argv[1] or tup[0] == sys.argv[2]:
            add_items(dicTot, tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
            if tup[0] == sys.argv[1] :
                fir_code = sys.argv[1]
                y = dicTot[tup[0]]
                a1,b1,c1,d1,e1 = [list(i) for i in zip(*y)] 
                fir_code = tup[0]
            if tup[0] == sys.argv[2]:
                z = dicTot[tup[0]]
                sec_code = sys.argv[2]
                a2,b2,c2,d2,e2 = [list(i) for i in zip(*z)]
                sec_code = tup[0]
    
    elif argc == 4:
        if tup[0] == sys.argv[1] or tup[0] == sys.argv[2] or tup[0] == sys.argv[3]:
            add_items(dicTot, tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
            if tup[0] == sys.argv[1] :
                fir_code = sys.argv[1]
                y = dicTot[tup[0]]
                a1,b1,c1,d1,e1 = [list(i) for i in zip(*y)] 
                fir_code = tup[0]
            if tup[0] == sys.argv[2]:
                z = dicTot[tup[0]]
                sec_code = sys.argv[2]
                a2,b2,c2,d2,e2 = [list(i) for i in zip(*z)]
                sec_code = tup[0]            
            if tup[0] == sys.argv[3]:
                v = dicTot[tup[0]]
                thr_code = sys.argv[3]
                a3,b3,c3,d3,e3 = [list(i) for i in zip(*v)]
                sec_code = tup[0]
 
subject = []
totalHours = 0
finalHours = 0

if argc == 1:
    k = 0
    flagL = False
    flagT = False
    flagTL = False
    falgO = False
    for i in range(len(a1)):
        if a1[i] == 'Lecture':
            subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]])
            totalHours = totalHours + sum_up(c1[i], d1[i]) 
            k = k+1
        elif a1[i] in forb_list and flagL == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]])
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagL = True  
                    k = k+1  
        elif a1[i] == 'Tutorial' and flagT == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]]) 
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagT = True 
                    k = k+1
        elif a1[i] == 'Tute/Lab' and flagTL == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]]) 
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagTL = True 
                    k = k+1
        elif a1[i] == 'Tute/Lab' and flagO == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]]) 
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagO = True 
                    k = k+1
    
    m = 0
    flagL = False
    flagT = False
    flagTL = False
    for i in range(len(a2)):
        if a2[i] == 'Lecture':
            subject.extend([sec_code, a2[i], b2[i], c2[i], d2[i]])
            totalHours = totalHours + sum_up(c2[i], d2[i]) 
            m = m+1

        elif a2[i] in forb_list and flagL == False:
            j = 1
            for j in range (m):
                if subject[5*j-2] < c2[i] and c2[i] < subject[5*j-1]:
                    if subject[5*j-2] < d2[i] and d2[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([sec_code, a2[i], b2[i], c2[i], d2[i]])
                    totalHours = totalHours + sum_up(c2[i], d2[i]) 
                    flagL = True  
                    m = m+1  
        elif a2[i] == 'Tutorial' and flagT == False:
            j = 1
            for j in range (m):
                if subject[5*j-2] < c2[i] and c2[i] < subject[5*j-1]:
                    if subject[5*j-2] < d2[i] and d2[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([sec_code, a2[i], b2[i], c2[i], d2[i]]) 
                    totalHours = totalHours + sum_up(c2[i], d2[i]) 
                    flagT = True 
                    m = m+1
        elif a2[i] == 'Tute/Lab' and flagTL == False:
            j = 1
            if j in range (m):
                if subject[5*m-2] < c2[i] and c2[i] < subject[5*m-1]:
                    if subject[5*m-2] < d2[i] and d2[i] < subject[5*m-1]:
                        pass
                else:
                    subject.extend([sec_code, a2[i], b2[i], c2[i], d2[i]]) 
                    totalHours = totalHours + sum_up(c2[i], d2[i]) 
                    flagTL = True 
                    m = m+1
        elif a2[i] == 'Other' and flagO == False:
            j = 1
            for j in range (m):
                if subject[5*j-2] < c2[i] and c2[i] < subject[5*j-1]:
                    if subject[5*j-2] < d2[i] and d2[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a2[i], b2[i], c2[i], d2[i]]) 
                    totalHours = totalHours + sum_up(c2[i], d2[i]) 
                    flagO = True 
                    m = m+1
    finalHours = final_Hours(totalHours, subject, numDays, Daylist)


if argc == 2:
    k = 0
    flagL = False
    flagT = False
    flagTL = False
    falgO = False
    for i in range(len(a1)):
        if a1[i] == 'Lecture':
            subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]])
            totalHours = totalHours + sum_up(c1[i], d1[i]) 
            k = k+1
        elif a1[i] == 'Lab class' and flagL == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]])
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagL = True  
                    k = k+1  
        elif a1[i] == 'Tutorial' and flagT == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]]) 
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagT = True 
                    k = k+1
        elif a1[i] == 'Tute/Lab' and flagTL == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]]) 
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagTL = True 
                    k = k+1
        elif a1[i] == 'Tute/Lab' and flagO == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]]) 
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagO = True 
                    k = k+1

 
if argc == 3: 
    k = 0
    flagL = False
    flagT = False
    flagTL = False
    falgO = False
    for i in range(len(a1)):
        if a1[i] == 'Lecture':
            subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]])
            totalHours = totalHours + sum_up(c1[i], d1[i]) 
            k = k+1
        elif a1[i] == 'Lab class' and flagL == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]])
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagL = True  
                    k = k+1  
        elif a1[i] == 'Tutorial' and flagT == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]]) 
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagT = True 
                    k = k+1
        elif a1[i] == 'Tute/Lab' and flagTL == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]]) 
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagTL = True 
                    k = k+1
        elif a1[i] == 'Tute/Lab' and flagO == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]]) 
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagO = True 
                    k = k+1

    m = 0
    flagL = False
    flagT = False
    flagTL = False
    for i in range(len(a2)):
        if a2[i] == 'Lecture':
            subject.extend([sec_code, a2[i], b2[i], c2[i], d2[i]])
            totalHours = totalHours + sum_up(c2[i], d2[i]) 
            m = m+1

        elif a2[i] == 'Lab class' and flagL == False:
            j = 1
            for j in range (m):
                if subject[5*j-2] < c2[i] and c2[i] < subject[5*j-1]:
                    if subject[5*j-2] < d2[i] and d2[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([sec_code, a2[i], b2[i], c2[i], d2[i]])
                    totalHours = totalHours + sum_up(c2[i], d2[i]) 
                    flagL = True  
                    m = m+1  
        elif a2[i] == 'Tutorial' and flagT == False:
            j = 1
            for j in range (m):
                if subject[5*j-2] < c2[i] and c2[i] < subject[5*j-1]:
                    if subject[5*j-2] < d2[i] and d2[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([sec_code, a2[i], b2[i], c2[i], d2[i]]) 
                    totalHours = totalHours + sum_up(c2[i], d2[i]) 
                    flagT = True 
                    m = m+1
        elif a2[i] == 'Tute/Lab' and flagTL == False:
            j = 1
            if j in range (m):
                if subject[5*m-2] < c2[i] and c2[i] < subject[5*m-1]:
                    if subject[5*m-2] < d2[i] and d2[i] < subject[5*m-1]:
                        pass
                else:
                    subject.extend([sec_code, a2[i], b2[i], c2[i], d2[i]]) 
                    totalHours = totalHours + sum_up(c2[i], d2[i]) 
                    flagTL = True 
                    m = m+1
        elif a2[i] == 'Other' and flagO == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c2[i] and c2[i] < subject[5*j-1]:
                    if subject[5*j-2] < d2[i] and d2[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a2[i], b2[i], c2[i], d2[i]]) 
                    totalHours = totalHours + sum_up(c2[i], d2[i]) 
                    flagO = True 
                    m = m+1
    finalHours = final_Hours(totalHours, subject, numDays, Daylist)


if argc == 4:
    k = 0
    flagL = False
    flagT = False
    flagTL = False
    falgO = False
    for i in range(len(a1)):
        if a1[i] == 'Lecture':
            subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]])
            totalHours = totalHours + sum_up(c1[i], d1[i]) 
            k = k+1
        elif a1[i] == 'Lab class' and flagL == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]])
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagL = True  
                    k = k+1  
        elif a1[i] == 'Tutorial' and flagT == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]]) 
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagT = True 
                    k = k+1
        elif a1[i] == 'Tute/Lab' and flagTL == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]]) 
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagTL = True 
                    k = k+1
        elif a1[i] == 'Tute/Lab' and flagO == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c1[i] and c1[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a1[i], b1[i], c1[i], d1[i]]) 
                    totalHours = totalHours + sum_up(c1[i], d1[i]) 
                    flagO = True 
                    k = k+1

    m = 0
    flagL = False
    flagT = False
    flagTL = False
    for i in range(len(a2)):
        if a2[i] == 'Lecture':
            subject.extend([sec_code, a2[i], b2[i], c2[i], d2[i]])
            totalHours = totalHours + sum_up(c2[i], d2[i]) 
            m = m+1

        elif a2[i] == 'Lab class' and flagL == False:
            j = 1
            for j in range (m):
                if subject[5*j-2] < c2[i] and c2[i] < subject[5*j-1]:
                    if subject[5*j-2] < d2[i] and d2[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([sec_code, a2[i], b2[i], c2[i], d2[i]])
                    totalHours = totalHours + sum_up(c2[i], d2[i]) 
                    flagL = True  
                    m = m+1  
        elif a2[i] == 'Tutorial' and flagT == False:
            j = 1
            for j in range (m):
                if subject[5*j-2] < c2[i] and c2[i] < subject[5*j-1]:
                    if subject[5*j-2] < d2[i] and d2[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([sec_code, a2[i], b2[i], c2[i], d2[i]]) 
                    totalHours = totalHours + sum_up(c2[i], d2[i]) 
                    flagT = True 
                    m = m+1
        elif a2[i] == 'Tute/Lab' and flagTL == False:
            j = 1
            if j in range (m):
                if subject[5*m-2] < c2[i] and c2[i] < subject[5*m-1]:
                    if subject[5*m-2] < d2[i] and d2[i] < subject[5*m-1]:
                        pass
                else:
                    subject.extend([sec_code, a2[i], b2[i], c2[i], d2[i]]) 
                    totalHours = totalHours + sum_up(c2[i], d2[i]) 
                    flagTL = True 
                    m = m+1
        elif a2[i] == 'Other' and flagO == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c2[i] and c2[i] < subject[5*j-1]:
                    if subject[5*j-2] < d2[i] and d2[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a2[i], b2[i], c2[i], d2[i]]) 
                    totalHours = totalHours + sum_up(c2[i], d2[i]) 
                    flagO = True 
                    m = m+1
                        
    xp = 0
    flagL = False
    flagT = False
    flagTL = False    
    for i in range(len(a3)):
        if a3[i] == 'Lecture':
            subject.extend([sec_code, a3[i], b3[i], c3[i], d3[i]])
            totalHours = totalHours + sum_up(c3[i], d3[i]) 
            xp = xp+1

        elif a3[i] == 'Lab class' and flagL == False:
            j = 1
            for j in range (m):
                if subject[5*j-2] < c3[i] and c3[i] < subject[5*j-1]:
                    if subject[5*j-2] < d3[i] and d3[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([thr_code, a3[i], b3[i], c3[i], d3[i]])
                    totalHours = totalHours + sum_up(c3[i], d3[i]) 
                    flagL = True  
                    xp = xp+1  
        elif a3[i] == 'Tutorial' and flagT == False:
            j = 1
            for j in range (m):
                if subject[5*j-2] < c3[i] and c3[i] < subject[5*j-1]:
                    if subject[5*j-2] < d3[i] and d3[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([thr_code, a3[i], b3[i], c3[i], d3[i]]) 
                    totalHours = totalHours + sum_up(c3[i], d3[i]) 
                    flagT = True 
                    xp = xp+1
        elif a3[i] == 'Tute/Lab' and flagTL == False:
            j = 1
            if j in range (m):
                if subject[5*m-2] < c3[i] and c3[i] < subject[5*m-1]:
                    if subject[5*m-2] < d3[i] and d3[i] < subject[5*m-1]:
                        pass
                else:
                    subject.extend([thr_code, a3[i], b3[i], c3[i], d3[i]]) 
                    totalHours = totalHours + sum_up(c3[i], d3[i]) 
                    flagTL = True 
                    xp = xp+1
        elif a3[i] == 'Other' and flagO == False:
            j = 1
            for j in range (k):
                if subject[5*j-2] < c3[i] and c3[i] < subject[5*j-1]:
                    if subject[5*j-2] < d1[i] and d1[i] < subject[5*j-1]:
                        pass
                else:
                    subject.extend([fir_code, a3[i], b3[i], c3[i], d3[i]]) 
                    totalHours = totalHours + sum_up(c3[i], d3[i]) 
                    flagO = True 
                    xp = xp+1
    
    finalHours = final_Hours(totalHours, subject, numDays, Daylist)
    
dicPrint = {} 
ordered = {"Mon":0, "Tue":1, "Wed":2, "Thu":3, "Fri":4}  
x = ' '
print("Total hours: {}".format(finalHours))
n = 1
dicPrint[subject[n*5-3]] = []
for n in range(len(subject)):
    if 5*n < len(subject):
        if subject[n*5-3] in dicPrint.keys():
            dicPrint[subject[n*5-3]].append(subject[n*5-4])
            dicPrint[subject[n*5-3]].append(subject[n*5-5])
            dicPrint[subject[n*5-3]].append(subject[n*5-2])
            dicPrint[subject[n*5-3]].append(subject[n*5-1])
        else:
            dicPrint[subject[n*5-3]] = []
            dicPrint[subject[n*5-3]].append(subject[n*5-4])
            dicPrint[subject[n*5-3]].append(subject[n*5-5])
            dicPrint[subject[n*5-3]].append(subject[n*5-2])
            dicPrint[subject[n*5-3]].append(subject[n*5-1])

for i in dicPrint.keys():
    for j in range(len(dicPrint[i])//4):
        print(x*2 + i)
        print(x*4 + dicPrint[i][4*j-4] + x + dicPrint[i][4*j-3] + ': ' + str(dicPrint[i][4*j-2]) + '-' + str(dicPrint[i][4*j-1]))

