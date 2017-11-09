import re

verbfile = open('verb-stems-list', 'r', encoding='utf-8')
verbs = verbfile.readlines()
verbfile.close()

queries = []

for v in verbs:
    vneat = re.match(r'([a-z]|ë)+(_([a-z]|ë)+)?', v).group(0)
    oquery = r'//node[node[@rel="hd" and @root="'+vneat+r'" and @pos="verb"] and node[@rel="obj1" and @cat="np" and node[@rel="hd" and @pos="noun"]]]'
    queries.append(oquery)
    squery = r'//node[node[@rel="su" and @cat="np" and node[@rel="hd" and @pos="noun"]] and node[@rel="hd" and @root="'+vneat+r'" and @pos="verb"]]'
    queries.append(squery)
    
outfile = open('queries.txt', 'w')
for q in queries:
    outfile.write(q+'\n')
outfile.close()