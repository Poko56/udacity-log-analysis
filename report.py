#! /usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

DBNAME = 'news'


def get_query_results(query):
    """Connect to the database with taking the SELECT statement as a parameter
    If working well, returns the SQL result, otherwise raise error.

    Args:
        query: A sequense of strings representing SQL SELECT statement.

    Returns:
        A list of SQL result that is fetched to the correcponding data.

    Raises:
        IOError: An Error occured if raised database error.
    """
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(query)
        result = c.fetchall()
        db.close()
        return result
    except Exception as e:
        print(type(e))
        print("Database error: " + str(e))
        exit(1)


# Query the article title and page views ordered by page views
page_views_query = """
        SELECT articles.title, COUNT(*) AS page_views
        FROM pages, articles
        WHERE CONCAT('/article/', articles.slug) = pages.path
        GROUP BY articles.slug, articles.title
        ORDER BY page_views DESC
        LIMIT 3;"""


# Query the article author and page viewsordered by page views
popular_article_author_query = """
        SELECT authors.name, COUNT(*) AS page_views
        FROM pages, articles, authors
        WHERE CONCAT('/article/', articles.slug) = pages.path
        AND authors.id = articles.author
        GROUP BY authors.name
        ORDER BY page_views DESC;"""


# Query day and error percent
# whose requests error is more than 1% per day
error_percent_query = """
        SELECT date, error_percent
        FROM error_percent_per_day
        WHERE error_percent > 1.0
        ORDER BY error_percent DESC;"""


# Main code to display the console
if __name__ == '__main__':
    # Display the most popular top 3 articles
    print('The most popular three articles of all time:')
    for i, v in enumerate(get_query_results(page_views_query)):
        print('[{rank}] "{title}" - {page_views} views').format(
            rank=str(i + 1),
            title=v[0],
            page_views=str(v[1]))

    print('+++++++++++++++++++++++++++++++++++++')

    # Display the most popular article authros of all times
    print('The most popular article authors of all time:')
    for i, v in enumerate(get_query_results(popular_article_author_query)):
        print('[{rank}] "{author}" - {page_views} views').format(
            rank=str(i + 1),
            author=v[0],
            page_views=str(v[1]))

    print('+++++++++++++++++++++++++++++++++++++')

    # Display the error rate(%) more than 1% per day.
    print('Day(s) which is more than 1% of requests errors:')
    for i, v in enumerate(get_query_results(error_percent_query)):
        print('[{rank}] {date} - {error_percent}% errors').format(
            rank=str(i + 1),
            date=v[0],
            error_percent=v[1])
