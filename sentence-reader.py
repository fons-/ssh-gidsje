#%%

import processitem
import numpy as np
from numpy import linalg as la
from reach import Reach

file = open('./RELPRON/RELPRON/translation_basic.txt','r', encoding='latin-1')
items_raw = file.readlines()
file.close()

r = Reach.load('./tulkens-embeddings/160/sonar-160.txt', header=True)

#%%

items_neat = []
for i in items_raw:
    neat = processitem.Item(i)
    items_neat.append(neat)
    
class SentenceReader:
    def __init__(self, sentence, r):
        self.sent = sentence
        self.termN_v = r.vector(self.sent.termN)
        self.headN_v = r.vector(self.sent.headN)
        self.argN_V = r.vector(self.sent.argN)
        self.V_v = r.vector(self.sent.V)
    
    def angle(self, v1, v2):
        """returns angle between two arrays"""
        c = np.dot(v1, v2) / la.norm(v1) / la.norm(v2)
        angle = np.arccos(np.clip(c, -1, 1))
        return angle
    
    def lex_base_headN(self):
        """lexical baseline based on
        similarity between term and head noun
        """
        return self.angle(self.termN_v, self.headN_v)
    
    def lex_base_verb(self):
        """lexical baseline based on
        similarity between term and verb
        """
        return self.angle(self.termN_v, self.V_v)
    
    def vector_addition(self):
        """simple vector addition of head noun,
        argument noun and verb
        """
        clause1 = np.add(self.headN_v, self.argN_V)
        clause2 = np.add(clause1, self.V_v)
        return self.angle(self.termN_v, clause2)
    
#%%

for i in items_neat[:1]:
    item_reader = SentenceReader(i, r)
    print(item_reader.lex_base_headN(), end=' ')
    print(item_reader.lex_base_verb(), end=' ')
    print(item_reader.vector_addition())