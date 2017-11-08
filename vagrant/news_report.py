#!/usr/bin/env python2
import psycopg2


def connect():
    """Connect to the PostgreSQL database news.  Returns a database
    connection."""
    return psycopg2.connect("dbname=news")


def reportTopArticles(amount):
    """Reports the top articles by visitors from the logs table.

    Args:
          amount: the number of rankings to return
    """
    query = "SELECT * FROM toparticles " \
            "ORDER BY hits DESC " \
            "LIMIT {0}".format(amount)
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows


def reportTopAuthors():
    """Reports the top authors by visitors added for each of their articles.
    """
    query = "SELECT * FROM authorsrank"
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows


def reportDailyErrors(x):
    """Reports the dates in which the logged errors exceed x percent that day
    out of all logged visits.

    Args:
          x: the percentage of errors reported
    """

    query = "SELECT * from dailyerrors " \
            "WHERE " \
            "cast(errorcount as decimal) / cast(hitcount as decimal) * 100 >= {0}" \
            .format(x)
    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows

    c.execute(query)
    rows = c.fetchall()
    print rows
    return rows


# And here we go...
# Connect to the database
DB = connect()
c = DB.cursor()

# Method queries
reportTopArticles(3)
reportTopAuthors()
reportDailyErrors(1)
