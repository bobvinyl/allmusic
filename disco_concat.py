import os

master_disco = open('master_disco/master_disco.csv','w')
master_disco.write('Artist,Year,Album,Label,AllMusic Rating,User Rating,User Count\n')
discos = os.listdir('discographies')

for disco_file in discos:
    print(disco_file)
    disco = open(f'discographies/{disco_file}','r')
    master_disco.writelines(disco.readlines()[1:])

master_disco.close()