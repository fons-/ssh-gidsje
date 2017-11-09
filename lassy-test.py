import xml.etree.ElementTree as ET
from os import listdir
from os.path import isdir

#import verbs

verbfile = open('./verb-stems-list.txt', 'r')
verbs_raw = verbfile.read()    
verbfile.close()
stems = verbs_raw.split()

#queries

query = './/node[@pos="verb"]/..node[@rel="obj1"][@cat="np"]/..'
query_o = './node[@rel="obj1"]'
query_s = './node[@rel="su"]'
query_v = './node[@pos="verb"]'
query_head = './node[@rel="hd"]'
query_rp = './/node[@cat="rel"]/node[@rel="body"][@cat="ssub"]'

#some functions for searching through XML tree
            
def findhead (node):
    cat = node.get('cat')
    if cat == 'np':
        return node.findall(query_head)[0]
    if node.get('pt') == 'n' or node.get('pt') == 'vnw':
            return node
    return None

def findsbj (match, root):
    sbjs = match.findall(query_s)
    if sbjs:
        sbj = sbjs[0]
        head = findhead(sbj)
        if ET.iselement(head):
            return head
        index = sbj.get('index')
        if index:
            coindices = root.findall('.//node[@index="'+index+'"]')
            for node in coindices:
                result = findhead(node)
                if ET.iselement(result):
                    return result
    return None

#clear output files

rp_output = open('./training/RP_files.txt', 'w')
rp_output.write('')
rp_output.close()

for file in listdir('./training/VO'):
    f = open('./training/VO/'+file, 'w')
    f.write('')
    f.close()

for file in listdir('./training/VS'):
    f = open('./training/VS/'+file, 'w')
    f.write('')
    f.close()

#treebank = './LassySmall/Treebank/dpc-bal-001236-nl-sen/'
corpus = './LassySmall/Treebank'
treebanks_raw = listdir(corpus)
treebanks = []
for t in treebanks_raw:
    if not t.endswith('.dact'):
        treebanks.append(t)

#loop over directories

for treebank in treebanks:
    print(treebank)
    #clear temporary output
    rp_files = []
    VO_output = dict()
    VS_output = dict()
    #loop over files
    for file in listdir(corpus+'/'+treebank):
        try:
            tree = ET.parse(corpus+'/'+treebank+'/'+file)
            root = tree.getroot()
            text = root.find('sentence').text
            #find verbs
            for v in stems:
                matches = root.findall('.//node[@root="'+v+'"][@pos="verb"]/..')
                for match in matches:
                    obj = None
                    sbj = None
                    obj_cons = match.find(query_o)
                    verb = match.find(query_v)
                    verb_root = verb.get('root')
                    if ET.iselement(obj_cons):
                        obj = findhead(obj_cons)
                    sbj = findsbj(match, root)
                    if ET.iselement(obj):
                        if obj.get('root'):
                            prefix = verb.get('begin') +'|'+ obj.get('root')+'|'+obj.get('begin')
                            output = prefix + ' ' +  text
                            if verb_root in VO_output:
                                VO_output[verb_root].append(output)
                            else:
                                VO_output[verb_root] = [output]
                    if ET.iselement(sbj):
                        if sbj.get('root'):
                            prefix =verb.get('begin') +'|'+ sbj.get('root')+'|'+sbj.get('begin')
                            output = prefix + ' ' +  text
                            if verb_root in VS_output:
                                VS_output[verb_root].append(output)
                            else:
                                VS_output[verb_root] = [output]
            #find RP
            rps = root.findall(query_rp)
            for rp in rps:
                #print(rp.get("id"))
                #print(text)
                #print(file)
                #print()
                rp_files.append(file)
        except:
            print(file)
            
    rp_output = open('./training/RP_files.txt', 'a')
    for filename in rp_files:
        rp_output.write(treebank+'/'+filename+'\n')
    rp_output.close()
    
    for verb in VO_output.keys():
        outfile = open('./training/VO/'+verb+'.txt', 'a')
        for i in VO_output[verb]:
            outfile.write(i+'\n')
        outfile.close()
        
    for verb in VS_output.keys():
        outfile = open('./training/VS/'+verb+'.txt', 'a')
        for i in VS_output[verb]:
            outfile.write(i)
        outfile.close()

#end loop
        
        