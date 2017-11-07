#!/usr/bin/env python3
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
    # Convert value to string.  Add a leading 0 if less than 10
    if x < 10:
        Perc = "0" + str(x)
    else:
        Perc = str(x)

    query = "SELECT * from dailyerrors " \
            "WHERE (errorcount / requestcount >= .{0})" \
            .format(Perc)
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
