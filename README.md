# Log Analysis db

The *log analysis db* is an internal reporting tool,
to analyze a newspaper website and give a statistics about kind of articles
the site's readers like, using information from the website database.

This tool will connect automatically to a fixed database called `news`,
reading data mainly from 2 views (`views_log`, `errors_log`) then print in
plain text the following statistics:
  1- The 3 most reading articles
  2- The most popular article authors
  3- The days did more than 1% of website requests lead to errors


*The Views creation syntax as follows:*
  1- Firstly for more details about the current used database, please see the
    `How To run this tool/ the database section` at the end of file.

  2- Connect to the database from the database console by using `\c` followed
    by the database name, for ex., `\c news`, or from the shell prompt by
    using the command `psql news`.

  3- Run the following two queries to create the needed Views by copy/ paste
    each one inside the database console then press Enter:

      create view views_log as
        select articles.id as article_l, articles.author as author_l
              , log.path as path_l, log.ip as ip_l, log.method as method_l
              , log.status as status_l, log.time as time_l, log.id as id_l
        from log join articles
        on log.path like '%' || articles.slug || '%'
      where log.method like 'GET%' and log.status like '2%';

      create view errors_log as
        select articles.id as article_l, articles.author as author_l
              , log.path as path_l, log.ip as ip_l, log.method as method_l
              , log.status as status_l, log.time as time_l, log.id as id_l
        from log left join articles
        on log.path like '%' || articles.slug || '%'
      where log.method like 'GET%'
              and (log.status like '4%' or log.status like '5%');


*How To run this tool:*
  1- Its a `python` program, needs the python standard libraries to be
    installed on the pc, try this site https://www.python.prg/

  2- The database connection to the  `news db` is required, its a postgresql
    database, created under a Linux VM, for more details:
    https://youtu.be/djnqoEO2rLc

  2- Finally the program can be run from the shell like (`terminal` on
    Mac or Linux) using the command `python3 loganalysisdb.py`, from
    `git bash` on Windows using `python loganalysisdb.py`, or just double
    clicked on the file.
