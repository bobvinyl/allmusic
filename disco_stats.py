import pandas as pd
import numpy as np
import os


#artists = ['Blind Melon','Stooges','Beach Boys','Beatles','Bob Dylan','Bruce Springsteen','Husker Du',
#           'Pixies','Prince','Rolling Stones','The Clash']

df_all = pd.DataFrame(columns=['Artist', 'Year', 'Album', 'Label', 'AllMusic Rating', 'User Rating',
       'User Count'])

discos = os.listdir('discographies')

#for artist in artists:
for disco in discos:
    df = pd.read_csv(f'discographies/{disco}')
    #df['User Rating'] = df['User Rating'].apply(lambda x: np.nan if x==0 else x)
    df = df.dropna()
    df_all = pd.concat([df_all,df],ignore_index=True)
    
df_all['Diff'] = df_all['AllMusic Rating'] - df_all['User Rating']

album_count = len(df_all['Diff'])
avg_chg = df_all['Diff'].sum() / album_count
avg_users = df_all['User Count'] / album_count

df_all['Diff from Average'] = df_all['Diff'] - avg_chg

print("Albums: ", album_count)
print('Avergae Change: ',avg_chg)
print('Average User Count: ', avg_users)

#df.agg({'A' : ['sum', 'min'], 'B' : ['min', 'max']})
#stats = df_all.loc[:,['Artist','Diff']].groupby('Artist').agg(['count', np.mean])
stats = df_all.loc[:,['Artist','Diff','Diff from Average']].groupby('Artist').agg({'Diff': ['count', np.mean], 'Diff from Average': np.mean})
print(stats.columns)
stats = stats.rename(columns={0: 'Album Count', 1: 'Raw Rating Diff', 2: 'Adjusted Rating Diff'})
stats.columns = stats.columns.droplevel()

print(stats)

stats.sort_values('Adjusted Rating Diff').to_csv('reports/mean_critic_to_fan_diff.csv')

print(df_all.loc[df_all['User Rating']==0,:])

# Find correlation between am/fan disparity and number of fan reviews

# Find average time between releases and check for albums released in at or below the time period
    
    