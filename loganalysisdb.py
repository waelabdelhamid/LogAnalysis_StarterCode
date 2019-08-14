# !/usr/bin/env python3
#
# "Database code" for the Log Analysis db Reporting tool.

import psycopg2

REPORT = '\t%s\n'

# Store the count of all queries will be run till now
# please consider change if more queries added in main.
QUERYCOUNT = 3

# Track the number of queries that are running.
# This variable will get +1 every time a query run
currentquery = 0


def get_analysis(query):
    """takes query as string argument, run it in postgresql\\news database,
    and returns logs analysis rows"""

    global currentquery
    rows = []
    currentquery += 1
    print("Fetching [{}{}{}] ...".format(currentquery, '/', QUERYCOUNT))
    try:
        # Fetch query from the news database
        db = psycopg2.connect("dbname=news")
        c = db.cursor()
        c.execute(query)
        rows = c.fetchall()
        db.close()
    except psycopg2.Error as e:
        print(e)
    return rows

if __name__ == '__main__':
    reports = ""

    # Fetch most popular three articles from the database
    # as noted i am not use outer join to force show the top 3 , else
    # no show
    query = """
        select title || ' -- ' || count(*)::text || ' view(s)' as title_num
        from articles join views_log on articles.id = views_log.article_l
        group by title
        order by count(*) desc
        limit 3;
    """
    reports += "\nThe most popular three articles of all time:\n"
    reports += "".join(REPORT % (text) for text in get_analysis(query))

    # Fetch most popular article authors from the database
    # here i am using outer join to show all list even 0 views authors
    query = """
        select name || ' -- ' || count(author_l)::text
                    ||' view(s)' as name_num
        from authors left join views_log on authors.id = views_log.author_l
        group by name
        order by count(author_l) desc;
    """
    reports += "\nThe most popular article authors of all time:\n"
    reports += "".join(REPORT % (text) for text in get_analysis(query))

    # Fetch days has more that 1% of requests lead to Error from the database
    # here i am using outer join to count all requests, then error requests
    query = """
        select REGEXP_REPLACE(
                        to_char(DATE_TRUNC('day', time), 'MONTH'), '\s+',
                     '')
                    || ' ' || to_char(DATE_TRUNC('day', time), 'DD,YYYY')
                    || ' -- '
                    || round(
                        round(
                            count(method_l) * 1.000 / count(method) * 1.000
                        ,3)
                    * 100, 1)::text
                    || '% errors' as day_errperc
        from log left join errors_log on id = id_l
        group by DATE_TRUNC('day', time)
        having count(method_l) * 1.000 / count(method) * 1.000 > 0.01;
    """
    reports += "\nThe days did more than 1% of requests lead to errors:\n"
    reports += "".join(REPORT % (text) for text in get_analysis(query))

    print(reports)
