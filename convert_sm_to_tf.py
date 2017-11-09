import re


sm = '/home/luka/ThLi/cooccurrence/weighted_sm.sm'

rowsfile = '/home/luka/ThLi/cooccurrence/weighted_sm.rows'
colsfile = '/home/luka/ThLi/cooccurrence/weighted_sm.cols'

cols_in = open(colsfile, 'r')
cols = cols_in.readlines()
cols_in.close()

colsdict = dict()
t = 0
for col in cols:
    colsdict[col[:-1]] = t
    t += 1

indices = []
values = []

sm_in = open(sm, 'r')

row = -1
current_row = ''
attriberrrors = 0

for line in sm_in.readlines():
    row_entry = re.search(r'^(\S+)(?=\s)', line).group(0)
    if row_entry != current_row:
        row += 1
        current_row = row_entry
        if row % 10000 == 0:
            print(row, '...')
    col_entry = re.search(r'\S+(?=\s+([0-9]+\.)?[0-9]+$)', line).group(0)
    col = colsdict[col_entry]
    value_str = re.search(r'([0-9]+\.)?[0-9]+$', line).group(0)
    value = float(value_str)
    indices.append([row, col])
    values.append(value)

sm_in.close()

dense_shape = [row + 1, len(cols)]

#%%

import tensorflow as tf
tensor = tf.SparseTensor(indices=indices, values=values, dense_shape=dense_shape)

#%%

dense = tf.sparse_tensor_to_dense(tensor)
s, u, v = tf.svd(dense)
reduced_tensor = tf.Variable(tf.matmul(dense, v[:, :300]))

#%%

init = tf.global_variables_initializer()
saver = tf.train.Saver()

with tf.Session() as sess:
    print('starting session')
    sess.run(init)
    save_path = saver.save(sess, '/home/luka/ThLi/cooccurrence/session.ckpt')
    
