vocabfile = open('vocab.txt', 'r')
vocab_raw = vocabfile.read()
vocabfile.close()

cols = vocab_raw.split(' ')

positions = dict()
cols_out = open('./cooccurrence/cols1.cols', 'w')
t = 0
for col in cols:
    positions[col] = t
    t += 1
    cols_out.write(col)
    cols_out.write('\n')
cols_out.close()

def getvocabindex(word):
    return(positions[word])

smfile = open('./cooccurrence/spm1.sm', 'r')
matrix_raw = smfile.read()
smfile.close()
matrix_rows = matrix_raw.split('\n')
matrix_tuples = list()
for row in matrix_rows:
    tup = row.split(' ')
    matrix_tuples.append(tup)
