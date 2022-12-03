import pandas as pd
import numpy as np

# Quantile settings
buckets = 3
drop_threshold = 1

# STD settings
stds_below_mean = 0.6

# Artists to output
all_artists = True
artists_output = ['Beatles','Rolling Stones','Beach Boys','Led Zeppelin','Prince','Bad Company','Sault','Black Sabbath','Kiss','Elton John']

# Files
write_files = False

artists_output_str = ''
if all_artists == False:
    for artist in artists_output:
        artists_output_str += artist[:1]

disco = pd.read_csv('master_disco\master_disco.csv')

if all_artists == False:
    disco = disco.loc[disco['Artist'].isin(artists_output),:]

disco['Q'] = disco.groupby(['Artist'])['User Count'].transform(lambda x: pd.qcut(x,q=buckets,labels=False,duplicates='drop'))
disco['Core by Quantile'] = disco.apply(lambda x: 'Yes' if x['Q'] >= drop_threshold else 'No', axis=1 )

disco['STD'] = disco.groupby(['Artist'])['User Count'].transform('std')
disco['Mean'] = disco.groupby(['Artist'])['User Count'].transform('mean')
disco['Core by STD'] = disco.apply(lambda x: 'Yes' if x['Mean'] - (x['STD']*stds_below_mean) < x['User Count'] else 'No', axis=1)

disco['Mismatch'] = disco['Core by Quantile'] != disco['Core by STD']

#disco['AllMusic Rating Sum Core by STD'] = disco.groupby(['Artist','Core by STD'])

#print(disco.groupby(['Artist'])['AllMusic Rating','Core by STD'].apply(lambda x: sum(x['AllMusic Rating'] if x['Core by STD']=='Yes' else 0), axis=1))

disco_out = disco if all_artists else disco.loc[disco['Artist'].isin(artists_output),:]

print(disco_out.loc[:,['Artist','Album','Year','AllMusic Rating','User Rating','Core by STD','Core by Quantile','Mismatch']].sort_values(['Artist','Core by STD','Core by Quantile']))

calc_version = f'_qcut_{str(buckets)}_{str(drop_threshold)}_std_{str(stds_below_mean)}'

if write_files:
    disco_out.loc[:,['Artist','Year','Album','Label','AllMusic Rating','User Rating','User Count','Q','STD','Mean','Core by STD','Core by Quantile','Mismatch']].to_csv(f'master_disco/{artists_output_str}_master_disco_with_core_{calc_version}.csv',index=False)

# Stats by artist

#df.groupby('A').agg({'B': ['min', 'max'], 'C': 'sum'})

disco['Core by STD'] = disco['Core by STD']=='Yes'
disco['Core by Quantile'] = disco['Core by Quantile']=='Yes'
disco_stats = disco.groupby('Artist').agg({'Album': 'count', 'Core by STD': 'sum', 'Core by Quantile': 'sum', 'AllMusic Rating': 'mean'})
disco_stats['Core Diff (Q-Std)'] = disco_stats.apply(lambda x: int(x['Core by Quantile']) - int(x['Core by STD']), axis=1)
disco_stats['Core Percent by STD'] = disco_stats['Core by STD'] / disco_stats['Album'] * 100
disco_stats['Core Percent by Quantile'] = disco_stats['Core by Quantile'] / disco_stats['Album'] * 100
disco_stats = disco_stats.round({'Core Percent by STD': 2, 'Core Percent by Quantile': 2})

disco_stats = disco_stats.merge(
    disco.loc[disco['Core by Quantile']==True,['Artist','AllMusic Rating']].groupby('Artist').agg('mean').rename(columns={'AllMusic Rating': 'AllMusic Mean by Quantile'}).merge(
        disco.loc[disco['Core by STD']==True,['Artist','AllMusic Rating']].groupby('Artist').agg('mean').rename(columns={'AllMusic Rating': 'AllMusic Mean by STD'}),
                left_index=True, right_index=True
    ), left_index=True, right_index=True
)

disco_stats['Quantile Diff from AllMusic'] = disco_stats['AllMusic Mean by Quantile'] - disco_stats['AllMusic Rating']
disco_stats['STD Diff from AllMusic'] = disco_stats['AllMusic Mean by STD'] - disco_stats['AllMusic Rating']

disco_stats['AllMusic Mean Diff (Q-Std)'] = disco_stats['AllMusic Mean by Quantile'] - disco_stats['AllMusic Mean by STD']

disco_stats = disco_stats.loc[:,['Album','Core by STD','Core by Quantile','Core Diff (Q-Std)','Core Percent by STD','Core Percent by Quantile',
                                 'AllMusic Rating','AllMusic Mean by Quantile','AllMusic Mean by STD','AllMusic Mean Diff (Q-Std)',
                                 'Quantile Diff from AllMusic','STD Diff from AllMusic']]

print(disco_stats)

if write_files:
    disco_stats.to_csv(f'stats/{artists_output_str}_master_disco_core_stats{calc_version}.csv')
