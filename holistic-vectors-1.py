import tensorflow as tf

#import input dimensions (v-arg combos, rows1.rows)
vargfile = open('./cooccurrence/rows1.rows', 'r')
varg_raw = vargfile.read()
vargfile.close()
vargs = varg_raw.split('\n')[:-1]
varg_dict = dict()
t = 0
for varg in vargs:
    varg_dict[varg] = t
    t += 1
del varg_raw
del vargs
input_dimension = len(varg_dict)

def input_vector(varg):
    """returns one-hot vector based on input"""
    index = varg_dict[varg]
    vector = tf.one_hot(index, input_dimension)
    return vector
    
#import output dimension (vocab, cols.cols)
vocabfile = open('./cooccurrence/cols1.cols', 'r')
vocab_raw = vocabfile.read()
vocabfile.close()
vocablist = vocab_raw.split('\n')[:-1]
vocab_dict = dict()
t = 0
for word in vocablist:
    vocab_dict[word] = t
    t += 1
del vocab_raw
del vocablist
output_dimension = len(vocab_dict)

def context_vector(word):
    """returns one-hot vector based on context"""
    index = vocab_dict[word]
    vector = tf.one_hot(index, output_dimension)
    return vector

#import cooccurence matrix

batch_size = 100
embedding_size = 128


#for each batch: obtain a series of input-output vectors
#can include negative samples

sess = tf.Session()
print(sess.run(input_vector('zing|O|zoiets')))
print(sess.run(context_vector('<S>')))

v_in = tf.placeholder(tf.float32, [None, input_dimension])
embeddings = tf.Variable(tf.random_uniform([input_dimension, embedding_size], -1.0, 1.0))
v_features = tf.matmul(v_in, embeddings)

feattooutput = tf.Variable(tf.random_uniform([embedding_size, output_dimension], -1.0, 1.0))
out_biases = tf.Variable(tf.zeros([output_dimension]))
v_output = tf.nn.softmax(tf.matmul(v_features, feattooutput))

v_context = tf.placeholder(tf.float32, [None, output_dimension])

#calculate loss
loss = tf.reduce_mean(tf.nn.nce_loss())

#optimizer
train_step = tf.train.GradientDescentOptimizer(1.0).minimize(loss)


#begin training
num_steps = 100001
init = tf.global_variables_initializer()
init.run()
print('Initialized')

average_loss = 0

