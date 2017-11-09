import tensorflow as tf
import re
from reach import Reach
r = Reach.load('./tulkens-embeddings/160/sonar-160.txt', header=True)

objsize = 160
holisticsize = 10

#%%

#import list of verbs
verb = 'overleef'
print('Verb:', verb)

#create tensor for verb
verbtens = tf.Variable(tf.random_uniform([objsize, holisticsize], 0.0, 1.0))
inp = tf.placeholder(tf.float32, [objsize])
outp = tf.matmul(verbtens, inp)
sess = tf.Session()

#get VO-combinations list
combos = []
rowsfile = open('./cooccurrence/rows1.rows', 'r')
done = False
found = False
while done == False:
    line = rowsfile.readline()
    if line.startswith(verb):
        found = True
        combos.append(line)
    else:
        if found == True:
            done = True

print('Number of arguments:', len(combos))

#select VO-combo
combo = combos[38]

#import holistic vector for VO-combo
holistens = tf.random_uniform([holisticsize], 0.0, 1.0)

#get object
obj = re.search(r'(?<=\|(O|S)\|).*$', combo).group(0)

#import embedding of object
objvec = r.vector(obj)
if objvec.any():
    objtens = tf.convert_to_tensor(objvec)