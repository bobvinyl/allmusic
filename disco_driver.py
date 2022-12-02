from allmusic_disco_scraper import allmusic_disco_scraper
# Either include the artists doct with the import or use the dict here
#from artists import artists

artists = {
    "": ""
}

am = allmusic_disco_scraper()

for artist, url in artists.items():
    df = am.disco_to_dataframe(artist, url)
    print(df.head())
    df.to_csv(f'discographies/{artist}.csv', index=False)
    
am = None