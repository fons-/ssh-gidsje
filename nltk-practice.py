import nltk
from nltk.corpus import alpino as alp
from nltk.tag import UnigramTagger, BigramTagger

alpino = alp.tagged_sents()
unitagger = UnigramTagger(alpino)
bitagger = BigramTagger(alpino, backoff=unitagger)
pos_tag = bitagger.tag
sent = 'Een telescoop is een instrument dat een astronoom gebruikt .'.split()
print(pos_tag(sent))

