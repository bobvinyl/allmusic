from allmusic_disco_scraper import allmusic_disco_scraper
# Either include the artists dict with the import or use the dict here
#from artists import artists

# Set this to your won instance of the Chrome driver (download from https://chromedriver.chromium.org/downloads)
driver_path = '../chrome/chromedriver.exe'

artists = {
    "": ""
}

am = allmusic_disco_scraper(driver_path)

for artist, url in artists.items():
    df = am.disco_to_dataframe(artist, url)
    print(df.head())
    df.to_csv(f'discographies/{artist}.csv', index=False)
    
am = None