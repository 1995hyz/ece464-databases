In this assignment, I created a web-scrapper that extracts data from rottentomatoes website.
The tomato_scrapper.py script can read movie names from movies_metadata.csv file, and query
HTML file from rottentomatoes website. If the movie is in the website and the query is
successful, the queried HTML file will be parsed and useful information will be extracted
and insert into a local mongoDB database.
sample_query.txt contains the outputs of some sample queries after the local database was
populated by data extracted from rottentomatoes website.