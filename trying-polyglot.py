from polyglot.mapping import Embedding
import processitem
import numpy as np

embeddings = Embedding.load('/home/luka/polyglot_data/embeddings2/nl/embeddings_pkl.tar.bz2')

words = []
vectors = []

for w, v in embeddings:
    words.append(w)
    vectors.append(v)

file = open('./RELPRON/RELPRON/translation_basic.txt','r', encoding='latin-1')
items_raw = file.readlines()
file.close()

items_neat = []
for i in items_raw:
    neat = processitem.Item(i)
    items_neat.append(neat)
    
#calculate lexical baselines: headN and V vectors
NN_dist = []
NV_dist = []
for i in items_neat:
    t = i.termN
    h = i.headN
    v = i.V
    if t in words:
        vt = embeddings.get(t)
        if h in words:
            vh = embeddings.get(h)
            NN_dist.append(np.linalg.norm(vt - vh))
        else: 
            NN_dist.append(None)
        if v in words:
            vv = embeddings.get(v)
            NV_dist.append(np.linalg.norm(vt - vv))
        else:
            NV_dist.append(None)

output = open('lexbaseline.txt', 'w')
for n in range(len(NN_dist)):
    output.write(str(NN_dist[n])+' '+str(NV_dist[n])+'\n')
output.close()

