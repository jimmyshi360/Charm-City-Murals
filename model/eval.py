# TODO: Build metadata table, and return dictionary column on eval.

from __init__ import *
import tensorflow as tf
import numpy as np
from model import train_op
import Augmentor
from tensorflow.contrib.framework.python.framework import load_checkpoint

def build_eval_fn():
    g = tf.Graph()
    with g.as_default():
        noisy_inputs = tf.placeholder(tf.float32 ,[None, WIDTH, HEIGHT, CHANNELS])
        inputs = tf.placeholder(tf.float32, [None, WIDTH, HEIGHT, CHANNELS])
        train = train_op(g, noisy_inputs, inputs)
        
        images  = np.random.rand(15, 1000, 1000, 3)

        saver = tf.train.Saver()
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, "{}/model.ckpt-{}".format(CHECKPOINTS_DIR, 29))
        
        [vectors] = sess.run([g.get_tensor_by_name("right:0")], feed_dict={inputs: images})
        vectors /= np.linalg.norm(vectors, axis=0)
        
        def eval_fn(query):
            [current] = sess.run([g.get_tensor_by_name("left:0")], feed_dict={noisy_inputs: query})
            current /= np.linalg.norm(current, axis=1)
            print(current.shape)

            ## TODO: Review math. something might be fishy.
            result = np.matmul(vectors, current.T) / 2
            index = np.argmax(result)
                  
            if result[index] > THRESHOLD:
                print("Result is likely this.", index, result)
                ## TODO: Return metadata associated with this index.
            else:
                print("probably not this", index, result)
                ## TODO: Return a negative result
        return eval_fn

eval_fn = build_eval_fn()

# example
eval_fn(np.random.rand(1, 1000, 1000, 3))
