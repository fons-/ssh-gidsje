corpus = './LassySmall/Treebank'

f = open('./training/RP_files.txt')
filelist_raw = f.read()
f.close()

files = filelist_raw.split('\n')

for file in files:
    fpath = corpus+'/'+file
    source = open(fpath, 'rb')
    content = source.read()
    source.close()
    
    title = file.split('/')[-1]
    output = open('./training/RP_trees/'+title, 'wb')
    output.write(content)
    output.close()