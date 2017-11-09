import os

path_o = '/media/luka/Seagate Expansion Drive/training2/VO'
path_s = '/media/luka/Seagate Expansion Drive/training2/VS'
files_o = os.listdir(path_o)
files_s = os.listdir(path_s)

outfile_o = open('verbs_vo.txt', 'w')
for file in files_o:
    verb = file[:-4]
    outfile_o.write(verb)
    outfile_o.write('\n')
outfile_o.close()

outfile_s = open('verbs_vs.txt', 'w')
for file in files_s:
    verb = file[:-4]
    outfile_s.write(verb)
    outfile_s.write('\n')
outfile_s.close()