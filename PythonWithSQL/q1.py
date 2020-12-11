import psycopg2

dbname = "a3"
conn = psycopg2.connect("dbname=a3")  
cur = conn.cursor()
query = "create or replace view step2 as select count(ce.person_id) as nEnrol, c.id from course_enrolments ce join courses c on ce.course_id=c.id group by c.id; select DISTINCT s.code, cast(s2.nEnrol*1./c.quota*100 as int) from Subjects s join Courses c on c.subject_id=s.id join terms t on t.id=c.term_id join step2 s2 on s2.id=c.id where c.quota > 50 and s2.nEnrol > c.quota and t.id=5199 order by s.code; "
cur.execute(query)
for tup in cur.fetchall():
    x = tup[0]
    y = str(tup[1])
    print(x+ ' '+ y + '%')  
cur.close()     
conn.close() 
