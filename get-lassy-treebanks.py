from os import listdir

output = open('treebanks.txt', 'w')

corpus = '/media/luka/Seagate Expansion Drive/LassyLarge/'
treebanks = []
for subdir in listdir(corpus):
    if subdir.startswith('WR'):
        treebanks.append(corpus+subdir+'/COMPACT/')
for treebank in treebanks:
    files = []
    for filename in listdir(treebank):
        if filename.endswith('.data'):
            files.append(filename)
            
    for file in files:
        output.write(treebank+ file)
        output.write('\n')

output.close()
