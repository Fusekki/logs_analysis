# Logs Analysis Project
## A Python report generation tool that performs three SQL queries on a complex Postgre SQL database with over a million rows
## This is part of the Udacity Full Stack Nanodegree program.  As such, it is my official submission for the project.
## 
Utilizes:
* [Python 3.6.3](https://www.python.org/)
* Python libraries: psycopg2


Prerequisites:
* [Python 3.6.3](https://www.python.org/)
* [VirtualBox](https://www.virtualbox.org/wiki/VirtualBox)
VirtualBox is the software that actually runs the VM. You can download it from virtualbox.org, here. Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.
Ubuntu 14.04 Note: If you are running Ubuntu 14.04, install VirtualBox using the [Ubuntu Software Center](https://apps.ubuntu.com/cat/applications/quantal/virtualbox-qt/), not the virtualbox.org web site. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.
* [Vagrant](https://www.vagrantup.com/)
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. You can download it from vagrantup.com. Install the version for your operating system.
Windows Note: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

To launch, follow these steps:
* Install the prerequisites listed above (Python, VirtualBox, Vagrant)
* Clone the repo
* From a command line, change to the directory of the repo and mount the vagrant VM with ```vagrant up```
* Connect to vagrant the VM by entering ```vagrant ssh```
* From the command line, type ```cd /vagrant```
* Create the database by entering ```psql -d news -f newsviews.sql```
* Launch the app by typing ```python news_report.py```

Note: 
* This reporting tool utilizes views specifically created for these queries.  The three views needed can be created by running ```psql -d news -f newsviews.sql``` from the virtual machine.
    * To create the views manually, from the vagrant command line, run ```psql -d news```
    * ```CREATE VIEW toparticles AS
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
    * ```CREATE VIEW authorsrank AS
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
    * ```CREATE VIEW dailyerrors AS
      SELECT ErrorPercent.date, concat(SUBSTRING(cast(ErrorPercent.ErrorDecimal as varchar(5)), 1, 3), ' %') as ErrorDecimal, ErrorPercent.errorcount, ErrorPercent.requestcount
      FROM (
      SELECT DailyErrors.dailyerrorcount as errorcount, DailyRequestCount.requests_count as requestcount, DailyErrors.time as date, ROUND((DailyErrors.DailyErrorCount / DailyRequestCount.requests_count), 2) * 100  as ErrorDecimal
      FROM  (
      SELECT SUM(ErrorByDay.count) DailyErrorCount, ErrorByDay.ErrorDate as time
      FROM (
      SELECT COUNT(status), DATE(time) as ErrorDate
      FROM (
      SELECT status, time
      FROM log
      WHERE status <> '200 OK'
      GROUP BY status, time) as ErrorTimes
      GROUP BY ErrorTimes.time, ErrorDate) as ErrorByDay
      GROUP BY ErrorByDay.ErrorDate, ErrorByDay.count) as DailyErrors
      LEFT JOIN (
      SELECT COUNT(DATE(time)) requests_count, date(time) as ShortDate
      FROM log
      GROUP BY ShortDate) as DailyRequestCount
      ON DailyErrors.time = DailyRequestCount.ShortDate) As ErrorPercent;

* Following the report, you will need to manually delete the custom views created. Enter the following at the vm command line.
    * ```psql -d news```
    * ```DROP VIEW IF EXISTS toparticles; ```
    * ```DROP VIEW IF EXISTS authorsrank;```
    * ```DROP VIEW IF EXISTS dailyerrors```
    

code by [Phillip Stafford](http://philliprstafford.com)