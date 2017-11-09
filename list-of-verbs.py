import processitem

file = open('./RELPRON/RELPRON/translation_basic.txt','r', encoding='latin-1')
items_raw = file.readlines()
file.close()

items_neat = []
for i in items_raw:
    neat = processitem.Item(i)
    items_neat.append(neat)
    
verbs = set()

for i in items_neat:
    verbs.add(i.V)

outfile = open('verb-stems-list.txt', 'w', encoding='utf-8')
for v in verbs:
    outfile.write(v+' ')
outfile.close()