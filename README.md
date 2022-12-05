# allmusic
Screen scrape and stats for allmusic.com in Python/Pandas

## allmusic_disco_scraper.py
Import the allmusic_disco_scraper class into your script.  Call the disco_to_dataframe method, passing the artist name and the URL of the artist's page at allmusic.com.  A Pandas DataFrame with one row per allbum including the following columns is returned.
### Methods:
| Method | Arguments | Returns |
| --- | --- | --- |
| disco_to_dataframe | <ul><li>artist (string)</li><li>url (string)</li></ul> | DataFrame <ul><li>Artist</li><li>Year</li><li>Album</li><li>Label</li><li>AllMusic Rating</li><li>User Rating</li><li>User Count</li></ul> |
| get_artist_url | <ul><li>artist (string)</li></ul> | <ul><li>artist<br/>(pulled form allmusic rather than the artist <br/>name as passed as an arg)</li><li>url</li></ul> |

## disco_driver.py
This script is an example using the allmusic_disco_scraper class's disco_to_dataframe method.  Create a dictionary of artists and their urls and the code loops through, screen scraping the data from allmusic.com and storing it in .csv files (one per artist).

## artist_driver.py
This script is an example using the allmsuic_disco_scraper class's get_artist_url method. Create a list of artists and the code loops through, screen scraping the data from allmusic.com and storing it in .csv files (one per artist).
