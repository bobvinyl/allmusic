import pandas as pd
import numpy as np
import os

#####################################################
### BEGIN SETTINGS
all_discos = True

#Files
write_files = True

#Quantile settings
buckets = 10
core_cutoff = 4

#Standard Deviation settings
stds_to_go_down = 0.75

#percent_from_mean = 0.75
### END SETTINGS
#####################################################

discos = [
    'ZZ Top.csv',
    'Yes.csv',
    'U2.csv',
    'Joy Division.csv',
    'Beatles.csv',
    'Led Zeppelin.csv',
    'Bob Marley.csv',
    # 'Prince.csv',
    # 'Madness.csv',
    # 'Supertramp.csv',
    'Rolling Stones.csv',
    'The Clash.csv',
    # 'Def Leppard.csv',
    'Iron Maiden.csv',
    # 'The Monkees.csv',
    'The Guess Who.csv',
    # 'All.csv',
    'Prince.csv',
    'Beach Boys.csv',
    'The Who.csv',
]

if all_discos:
    discos = os.listdir('discographies')
    
stats = []
skips = []

for disco in discos:
    print(disco)
    full_disco = pd.read_csv(f'discographies/{disco}').dropna()
    
    if len(full_disco) > 0:

        full_disco['Q'] = pd.qcut(full_disco['User Count'],q=buckets,labels=False,duplicates='drop')
        
        q_core_disco = full_disco.loc[full_disco['Q']>core_cutoff,:]
        q_excess_disco = full_disco.loc[full_disco['Q']<=core_cutoff,:]
            
        std_user_count_low = full_disco['User Count'].mean() - (full_disco['User Count'].std() * stds_to_go_down)      
        std_core_disco = full_disco.loc[full_disco['User Count']>std_user_count_low,:]
        std_excess_disco = full_disco.loc[full_disco['User Count']<=std_user_count_low,:]
        
        # Maybe think this one through later
        #perc_user_count_low = (full_disco['User Count'].max() - full_disco['User Count'].min()) / full_disco['User Count'].max()
        
        # disco_stat_data = [
        #     ['Variance',full_disco['User Count'].var()],
        #     ['Standard Deviation',full_disco['User Count'].std()],
        #     ['Min',full_disco['User Count'].min()],
        #     ['Max',full_disco['User Count'].max()],
        #     ['Mean',full_disco['User Count'].mean()],
        #     ['(Max-Min)/Max',(full_disco['User Count'].max() - full_disco['User Count'].min()) / full_disco['User Count'].max()],
        #     ['Qcut Buckets',buckets],
        #     ['Qcut Max Excess',core_cutoff],
        #     ['Standard Deviations Below Mean to Include in Core', stds_to_go_down],
        # ]
        stats.append([disco[:-4],
                    full_disco['User Count'].var(),
                    full_disco['User Count'].std(),
                    full_disco['User Count'].min(),
                    full_disco['User Count'].max(),
                    full_disco['User Count'].mean(),
                    (full_disco['User Count'].max() - full_disco['User Count'].min()) / full_disco['User Count'].max(),
                    len(full_disco),
                    full_disco['User Count'].sum(),
                    full_disco['AllMusic Rating'].mean(),
                    full_disco['User Rating'].mean(),                    
                    buckets,
                    core_cutoff,
                    len(q_core_disco),
                    len(q_excess_disco),
                    len(q_core_disco)/len(full_disco),
                    q_core_disco['AllMusic Rating'].mean(),
                    q_core_disco['User Rating'].mean(),
                    q_core_disco['AllMusic Rating'].mean() - full_disco['AllMusic Rating'].mean(),
                    q_core_disco['User Rating'].mean() - full_disco['User Rating'].mean(),
                    q_excess_disco['AllMusic Rating'].mean(),
                    q_excess_disco['User Rating'].mean(),
                    stds_to_go_down,
                    len(std_core_disco),
                    len(std_excess_disco),
                    len(std_core_disco)/len(full_disco),
                    std_core_disco['AllMusic Rating'].mean(),
                    std_core_disco['User Rating'].mean(),
                    std_core_disco['AllMusic Rating'].mean() - full_disco['AllMusic Rating'].mean(),
                    std_core_disco['User Rating'].mean() - full_disco['User Rating'].mean(),
                    std_excess_disco['AllMusic Rating'].mean(),
                    std_excess_disco['User Rating'].mean(),
                    ])
    else:
        skips.append(disco)
         
cols = ['Artist','Variance','Standard Deviation','Min','Max','Mean','(Max-Min)/Max','Total Albums',
        'Total User Ratings','Total AllMusic Mean Rating','Total User Mean Rating','Qcut Buckets',
        'Qcut Max Excess','Qcut Core Size','Qcut Excess Size','Qcut Percent Kept',
        'Qcut Core AllMusic Mean Rating','Qcut Core User Mean Rating',
        'Qcut AllMusic Rating Diff','Qcut User Rating Diff','Qcut Excess AllMusic Mean Rating',
        'Qcut Excess User Mean Rating','Standard Deviations Below Mean to Include in Core','Std Core Size',
        'Std Excess Size','Std Percent Kept','Std Core AllMusic Mean Rating','Std Core User Mean Rating',
        'Std AllMusic Rating Diff','Std User Rating Diff','Std Excess AllMusic Mean Rating','Std Excess User Mean Rating']
        
stats_df = pd.DataFrame(columns=cols, data=stats)

calc_version = f'_qcut_{str(buckets)}_{str(core_cutoff)}_std_{str(stds_to_go_down)}'

stats_df.to_csv(f'stats/{"all_" if all_discos else ""}core_disco_calc_stats_{calc_version}.csv',index=False)

print(skips)
