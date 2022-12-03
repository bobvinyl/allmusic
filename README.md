# allmusic
Screen scrape and stats for allmusic.com in Python/Pandas

## allmusic_disco_scraper.py
Import the allmusic_disco_scraper class into your script.  Call the disco_to_dataframe method, passing the artist name and the URL of the artist's page at allmusic.com.  A Pandas DataFrame with one row per allbum including the following columns is returned.
  * Artist
  * Year
  * Album
  * Label
  * AllMusic Rating
  * User Rating
  * User Count

## disco-driver.py
This script is an example using the allmusic_disco_scraper class.  Create a dictionary of artists and their urls and the code loops through, screen scraping the data from allmusic.com and storing it in .csv files (one per artist).
