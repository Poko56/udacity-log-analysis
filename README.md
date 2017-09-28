## About

This code is for the project of logs analysis of newspaper site. The data is from 2016-07-01 to 2016-07-31, and is consists of three tables(articles, authors, log table). You can [download the sql data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

This program will analyze the following.

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Set up

### The virtual machine

You can download the virtual machine: [https://github.com/udacity/fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm).

This virtual machine will give you the PostgreSQL database and support software like Python2.7 needed for running this program.

### Database

If you don't have news database in the psql, run this code to create news database in your terminal. And be sure to place the newsdata.sql file in the same directory and logged in with SSH.

```
psql -d news -f newsdata.sql
```

### Views in the database

For running the log analysis code, you need to create views in the database. So go to the psql and run the following code.

- View for the problem 1 and 2.

```sql
create view pages
as select log.path
from log
where (log.status = '200 OK') and (not log.path = '/');
```

- Views for the problem 3.

```sql
create view error_per_day
as select log.time::timestamp::date as date, count(*) as error
from log
where not log.status = '200 OK' group by date;
```

```sql
create view access_per_day
as select log.time::timestamp::date as date, count(*) as access
from log group by date;
```

```sql
create view error_percent_per_day
as select
	to_char(access_per_day.date, 'FMMonth dd, YYYY') as date,
	round(100.0 * error_per_day.error / access_per_day.access, 1) as error_percent
from access_per_day, error_per_day
where access_per_day.date = error_per_day.date;
```

## Usage

After loggin in to the virtual machine ssh, go to the directory where this program is placed. And run the following code.

You can run the code to display the Log Analysis.

```sh
python report.py
```

This code will display the report. To see the output, take a look at _output.txt_.



## License

This program is under [MIT licence](https://github.com/nishanths/license/blob/master/LICENSE).
