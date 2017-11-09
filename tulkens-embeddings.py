import processitem
from reach import Reach

r = Reach.load('./tulkens-embeddings/160/sonar-160.txt', header=True)

file = open('./RELPRON/RELPRON/translation_basic.txt','r', encoding='latin-1')
items_raw = file.readlines()
file.close()

items_neat = []
for i in items_raw:
    neat = processitem.Item(i)
    items_neat.append(neat)

NN_dist = []
NV_dist = []
for i in items_neat:
    t = i.termN
    h = i.headN
    v = i.V
    vt = r.vector(t)
    if vt.any():
        vh = r.vector(h)
        if vh.any():
            simh = r.similarity(t, h)
            NN_dist.append(simh)
        vv = r.vector(v)
        if vv.any():
            simv = r.similarity(t, v)
            NV_dist.append(simv)

totaln = 0
for n in NN_dist:
    totaln += n
    
totalv = 0
for n in NV_dist:
    totalv += n

    
mean_n = totaln / len(NN_dist)
mean_v = totalv / len(NV_dist)

