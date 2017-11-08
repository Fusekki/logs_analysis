--Custom views for the news database

-- Drop the views if they exist.

DROP VIEW IF EXISTS toparticles;
DROP VIEW IF EXISTS authorsrank;
DROP VIEW IF EXISTS dailyerrors;

-- Create Top Articles View
--This view reports the top articles of all time based on hits.
CREATE VIEW toparticles AS
SELECT articles.title, hits.Hits
FROM (
SELECT COUNT(log.path) as Hits, SUBSTRING(log.path, 10) as Slug
FROM log
WHERE NOT path = '/'
GROUP BY Slug
ORDER BY Hits DESC
) AS hits
RIGHT JOIN articles ON
hits.Slug = articles.slug;

-- Create Top Authors View
--This view reports the top authors of all time based on hits
CREATE VIEW authorsrank AS
SELECT  authors.name, SUM(Standings.HitCount) AuthorHits
FROM (
SELECT articles.author, articles.title, Hits.HitCount
FROM (
SELECT COUNT(log.path) as HitCount, SUBSTRING(log.path, 10) as Slug
FROM log
WHERE NOT path = '/'
GROUP BY Slug
ORDER BY HitCount DESC
) as Hits
RIGHT JOIN articles ON
Hits.Slug = articles.slug
GROUP BY articles.author, articles.title, Hits.HitCount
ORDER BY Hits.HitCount DESC) as Standings
LEFT JOIN authors
on authors.id = Standings.author
GROUP BY authors.name
ORDER BY AuthorHits DESC;

--Create Daily Error Percentage View
--This view reports the error percentage, the error count, and request count of each date logged with activity.
CREATE VIEW dailyerrors AS
select HitsByDate.time as Date, CONCAT(cast(cast(cast(ErrorsByDate.count as decimal) / cast(HitsByDate.count as decimal) * 100 as decimal(10,2)) as varchar(5)), ' %') as ErrorPercent,
ErrorsByDate.count as ErrorCount, HitsByDate.count as HitCount
FROM (
select count(time), time::date
from log
group by time::date) as HitsByDate
left join (
select count(time), time::date
from log
WHERE
status <> '200 OK'
group by time::date) as ErrorsByDate
on HitsByDate.time = ErrorsByDate.time



