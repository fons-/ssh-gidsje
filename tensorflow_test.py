import sys
import os

folder = os.path.expandvars('/home/luka/anaconda3/envs/py35/lib/python3.5/site-packages/tensorflow/')
if folder not in sys.path:
    sys.path.append(folder)


import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))