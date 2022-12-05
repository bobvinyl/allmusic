from allmusic_disco_scraper import allmusic_disco_scraper

# Set this to your won instance of the Chrome driver (download from https://chromedriver.chromium.org/downloads)
driver_path = '../chrome/chromedriver.exe'

# Add artists to this list (Note: The file output will be named for the artist name in allmusic and may be different than the name in the list)
artists = [
    'Beat'
]

am = allmusic_disco_scraper(driver_path)

for artist in artists:
    # Get the artist name and url
    artist, url = am.get_artist_url(artist)
    # Get the discography as a DataFrame using the artist and url above
    df = am.disco_to_dataframe(artist,url)
    # Write the dicography to a file
    df.to_csv(f'discographies/{artist}.csv', index=False)