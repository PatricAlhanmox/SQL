-- COMP3311 19T3 Assignment 2
-- Written by <<Zhifan Zhang>>

-- Q1 Which movies are more than 6 hours long? 

create or replace view Q1(title)
as
select t.main_title 
from titles t 
where runtime > 360 and t.format ILIKE 'movie';


-- Q2 What different formats are there in Titles, and how many of each?

create or replace view Q2(format, ntitles)
as
select  count(t.format), t.format 
from titles t 
group by t.format;


-- Q3 What are the top 10 movies that received more than 1000 votes?

create or replace view Q3(title, rating, nvotes)
as
select t.main_title, t.rating, t.nvotes 
from titles t 
where t.format ILIKE 'movie' and t.nvotes > 1000  
order by t.rating desc, t.main_title LIMIT 10;


-- Q4 What are the top-rating TV series and how many episodes did each have?

create or replace view Toprate 
as
select id, main_title
From titles
where rating = 10 AND format ILIKE '%TV%series%';

create or replace view Q4(title, nepisodes)
as
select top.main_title, count(top.main_title)
from Toprate as top
JOIN episodes as ep ON top.id=ep.parent_id
group by top.main_title
;


-- Q5 Which movie was released in the most languages?

create or replace view lan
as
select DISTINCT t.id, t.main_title, a.language
from titles t
join Aliases as a on t.id=a.title_id
where t.format='movie';

create or replace view most
as
select DISTINCT la.main_title, la.id, count(la.language) 
as nlanguages
from lan la
group by la.id, la.main_title;

create or replace view Q5(title, nlanguages)
as
select l.main_title, l.nlanguages
from most l
where l.nlanguages = (select MAX(nlanguages) from most)
;


-- Q6 Which actor has the highest average rating in movies that they're known for?
create or replace view actors
as
select w.name_id as id, n.name as name
from worked_as w
join names as n on w.name_id=n.id
where work_role ILIKE 'actor';

create or replace view ratemovie
as 
select avg(t.rating), a.id, a.name
from titles t
join known_for kf on t.id=kf.title_id
join actors a on a.id=kf.name_id
where t.format ILIKE 'movie'
group by a.id, a.name
having COUNT(t.rating) > 2;

create or replace view Q6(name)
as
select ratemovie.name
from ratemovie
where avg >= (select MAX(ratemovie.avg) from ratemovie)
;

-- Q7 For each movie with more than 3 genres, show the movie title and a comma-separated list of the genres
create or replace view step1
as
select DISTINCT t.main_title, m.genre, t.id
from titles t 
join title_genres m on t.id=m.title_id
where t.format ILIKE 'movie';

create or replace view step2
as 
select t.main_title, t.id, count(t.genre)
from step1 t
group by t.main_title, t.id;

create or replace view step3
as
select t.main_title, t.id
from step2 t
where t.count > 3;

create or replace view step4
as
select m.main_title, g.genre
from step3 m
join titles t on t.id=m.id
join title_genres g on g.title_id=t.id
order by m.main_title, g.genre;

create or replace view Q7(title,genres)
as
select DISTINCT m.main_title, string_agg(genre, ';')
from step4 m
group by m.main_title
;

-- Q8 Get the names of all people who had both actor and crew roles on the same movie

create or replace view stepFirst
as
select DISTINCT n.name, n.id as identity, t.id
from actor_roles ar
join titles t on ar.title_id=t.id
join names n on n.id=ar.name_id
where t.format ILIKE 'movie'
;

create or replace view stepSecond
as
select DISTINCT n.name, n.id as identity, t.id
from crew_roles as cr
join names n on n.id=cr.name_id
join titles t on t.id=cr.title_id
where t.format ILIKE 'movie'
;

create or replace view Q8(name)
as
select DISTINCT A.name
 from stepSecond A
inner join stepFirst B
on A.id=B.id AND A.identity=B.identity
;

-- Q9 Who was the youngest person to have an acting role in a movie, and how old were they when the movie started?
create or replace view steps1
as
select n.birth_year, t.start_year start_year, n.name
from actor_roles as ar
join titles t on t.id=ar.title_id
join names n on n.id=ar.name_id
where t.format ILIKE 'movie'
;

create or replace view steps2
as
select DISTINCT n.name, (n.start_year-n.birth_year) as age
from steps1 n
order by age
;

create or replace view Q9(name,age)
as
select n.name, age
from steps2 n
where age = (select MIN(age) from steps2)
;

-- Q10 Write a PLpgSQL function that, given part of a title, shows the full title and the total size of the cast and crew

create or replace function
	Q10(partial_title text) returns setof text
as $$
DECLARE
    succ integer;
    num_1 integer;
    num_2 integer;
    num_3 integer;
    sum_people integer;
    k RECORD;
BEGIN
    succ := 0;
    for k in (select t.main_title, t.id
              from titles t
              where t.main_title ILIKE '%' || partial_title || '%')
    LOOP
        SELECT count(DISTINCT(n.id)) into num_1
        from names n join principals pr on n.id=pr.name_id
        join titles t on t.id=pr.title_id
        where t.id=k.id;
        
        select count(DISTINCT(n.id)) into num_2
        from names n join crew_roles cr on cr.name_id=n.id
        join titles t on t.id=cr.title_id
        where t.id=k.id;
        
        select count(DISTINCT(n.id)) into num_3
        from names n join actor_roles ar on n.id=ar.name_id
        join titles t on t.id=ar.title_id
        where t.id=k.id;
        
        IF (num_1 >= num_2) and (num_1 >= num_3) then
            sum_people :=num_1;
        ELSIF (num_2 >= num_1) and (num_2 >= num_3) then
            sum_people :=num_2;
        ELSIF (num_3 >= num_1) and (num_3 >= num_2) then
            sum_people :=num_3;
        END IF;
                
        IF (sum_people != 0) then
            succ := 1;
            return NEXT k.main_title || ' has ' || sum_people || ' cast and crew';
        end IF;
    end LOOP;
    
    IF (succ = 0) then
        return NEXT 'No matching titles';
    end IF;

END;$$ language plpgsql;

