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
query_any_v = './/node[@pos="verb"]'
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

#%%

fileref = open('treebanks.txt', 'r')
files_raw = fileref.read()
fileref.close()

files = files_raw.split('\n')
files_to_do = files

def updatefileref():
    """after each file, call on this function to remove it from reference file"""
    global files_to_do
    files_to_do = files_to_do[1:]
    fileref = open('treebanks.txt', 'w')
    for f in files_to_do:
        fileref.write(f)
        fileref.write('\n')
    fileref.close()
            
for file in files:
    print(file[-10:], end='...')
    print ((100 -(100 * (len(files_to_do) / 3867))), '%...')
    #clear local output
    rp_files = []
    VO_output = dict()
    VS_output = dict()
    
    #open file
    f = open(file, 'r')
    raw = f.read()
    f.close()
    
    #loop trough sentences in data
    sentences = raw.split('<?xml version="1.0" encoding="UTF-8"?>')
    for sentence in sentences[1:]:
        try:
            root = ET.fromstring(sentence)
            text = root.find('sentence').text.split(' ')
            #find verbs
            if ET.iselement(root.find(query_any_v)):            
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
                                prefix = obj.get('root') + '|'
                                text[int(verb.get('begin'))] = '&&|' + verb.get('root') + '|' + obj.get('root')
                                joined = ' '.join(text)
                                output = prefix + ' ' + joined
                                if verb_root in VO_output:
                                    VO_output[verb_root].append(output)
                                else:
                                    VO_output[verb_root] = [output]
                        if ET.iselement(sbj):
                            if sbj.get('root'):
                                prefix = sbj.get('root')+'|'
                                text[int(verb.get('begin'))] = '&&|' + verb.get('root') + '|' + sbj.get('root')
                                joined = ' '.join(text)
                                output = prefix + ' ' +  joined
                                if verb_root in VS_output:
                                    VS_output[verb_root].append(output)
                                else:
                                    VS_output[verb_root] = [output]
            #find RP, not processed yet
            rps = root.findall(query_rp)
            for rp in rps:
                rp_files.append(sentence)
        except Exception as e:
            print(e)
            
    #save results to files
    rp_output = open('/media/luka/Seagate Expansion Drive/training/RP_files.txt', 'a')
    for structure in rp_files:
        rp_output.write(structure)
        rp_output.write('\n')
    rp_output.close()
    
    for verb in VO_output.keys():
        outfile = open('/media/luka/Seagate Expansion Drive/training/VO/'+verb+'.txt', 'a')
        for i in VO_output[verb]:
            outfile.write(i+'\n')
        outfile.close()
        
    for verb in VS_output.keys():
        outfile = open('/media/luka/Seagate Expansion Drive/training/VS/'+verb+'.txt', 'a')
        for i in VS_output[verb]:
            outfile.write(i)
        outfile.close()
    
    updatefileref()
