import pandas as pd
import numpy as np
import os

#####################################################
### BEGIN SETTINGS
#Choose only one and set the appropriate values below
use_quantile = True
use_std = False

all_discos = False

#Files
write_files = True

#Display
display_discos = False
display_stats = False

#Quantile settings
buckets = 10
core_cutoff = 4

#Standard Deviation settings
stds_to_go_down = 0.75
### END SETTINGS
#####################################################

if use_quantile & use_std:
    print('Choose only one method')
    exit()

process_type = 'quantile' if use_quantile else 'std' if use_std else ''

discos = [
    # 'ZZ Top.csv',
    # 'Yes.csv',
    # 'U2.csv',
    # 'Joy Division.csv',
    # 'Beatles.csv',
    # 'Led Zeppelin.csv',
    # 'Bob Marley.csv',
    # 'Prince.csv',
    # 'Madness.csv',
    # 'Supertramp.csv',
    # 'Rolling Stones.csv',
    # 'The Clash.csv',
    # 'Def Leppard.csv',
    # 'Iron Maiden.csv',
    # 'The Monkees.csv',
    # 'The Guess Who.csv',
    'All.csv'
]

if all_discos:
    discos = os.listdir('discographies')

error_discos = []

for disco in discos:
    print(disco)
    full_disco = pd.read_csv(f'discographies/{disco}').dropna()

    #labels = range(1,buckets+1)
    try:
        # qc = pd.qcut(full_disco['User Count'],q=buckets,labels=False,duplicates='drop')
        # print(qc)
        # print(len(qc))
        full_disco['Q'] = pd.qcut(full_disco['User Count'],q=buckets,labels=False,duplicates='drop')
        print(full_disco)  
    except ValueError as ve:
        print(f'{disco}: {str(ve)}')
        error_discos.append((disco,str(ve)))
    except IndexError as ie:
        print(f'{disco}: {str(ie)}')
        error_discos.append((disco,str(ie)))
    if use_quantile:        
        core_disco = full_disco.loc[full_disco['Q']>core_cutoff,:]
        excess_disco = full_disco.loc[full_disco['Q']<=core_cutoff,:]
        
    if use_std:
        user_count_low = full_disco['User Count'].mean() - full_disco['User Count'].std()        
        core_disco = full_disco.loc[full_disco['User Count']>user_count_low,:]
        excess_disco = full_disco.loc[full_disco['User Count']<=user_count_low,:]
    
    if display_discos:
        print('Full')
        print(full_disco)
        print('Core')
        print(core_disco)
        print('Excess')
        print(excess_disco)
    
    disco_stat_data = [
        ['Process Type', process_type],
        ['Variance',full_disco['User Count'].var()],
        ['Standard Deviation',full_disco['User Count'].std()],
        ['Min',full_disco['User Count'].min()],
        ['Max',full_disco['User Count'].max()],
        ['Mean',full_disco['User Count'].mean()],
        ['(Max-Min)/Max',(full_disco['User Count'].max() - full_disco['User Count'].min()) / full_disco['User Count'].max()],
    ]
    
    if process_type == 'quantile':
        disco_stat_data.append(['Buckets',buckets])
        disco_stat_data.append(['Max Excess',core_cutoff])
        
    if process_type == 'std':
        disco_stat_data.append(['Standard Deviations Belwo Mean to Include in Core', stds_to_go_down])
    
    disco_stats = pd.DataFrame(columns=['Stat','Value'],data=disco_stat_data)
    
    if display_stats:
        print(disco)
        print('Variance: ', str(full_disco['User Count'].var()))
        print('Satndard Deviation: ', str(full_disco['User Count'].std()))
        print('Min: ', str(full_disco['User Count'].min()))
        print('Max: ', str(full_disco['User Count'].max()))
        print('Mean: ', str(full_disco['User Count'].mean()))
        print('Variance / Max: ', str(full_disco['User Count'].var() / full_disco['User Count'].max()))
        print('(Max - Min) / Max: ', str((full_disco['User Count'].max() - full_disco['User Count'].min()) / full_disco['User Count'].max()))
        print('***********************')
    
    if write_files:
        calc_version = ''
        if use_quantile:
            calc_version = f'_{str(buckets)}_{str(core_cutoff)}'
        if use_std:
            calc_version = f'_{str(stds_to_go_down)}'
        with pd.ExcelWriter(f"core_disco/{disco}_{process_type}{calc_version}.xlsx") as writer:
            full_disco.to_excel(writer, sheet_name="Full Discography", index=False)
            core_disco.to_excel(writer, sheet_name="Core Discography", index=False)
            excess_disco.to_excel(writer, sheet_name="Excess Discography", index=False)
            disco_stats.to_excel(writer, sheet_name='Stats', index=False)
    
print(error_discos)