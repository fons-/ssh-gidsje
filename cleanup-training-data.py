import os

path_o = '/media/luka/Seagate Expansion Drive/training2/VO'
path_s = '/media/luka/Seagate Expansion Drive/training2/VS'
files_o = os.listdir(path_o)
files_s = os.listdir(path_s)

def filter_dir(path, files):
    """delete any files not in the stems list"""
    verbfile = open('./verb-stems-list.txt', 'r')
    verbs_raw = verbfile.read()    
    verbfile.close()
    stems = verbs_raw.split()
    
    for stem in stems:
        if not stem+'.txt' in files:
            print(stem)
    print()
    
    for file in files:
        if not file[:-4] in stems:
            print(file)
            #os.remove(path+'/'+file)


def getsize(path, files):
    for file in files:
        conn = open(path+'/'+file, 'r')
        text = conn.read()
        conn.close()
        size = len(text.split('\n'))
        spacing = (25 - len(file) - len(str(size)))*' '
        print(file[:-4], spacing, size)

getsize(path_s, files_s)