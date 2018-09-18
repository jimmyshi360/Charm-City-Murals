# TODO: Build metadata table, and return dictionary column on eval.

from __init__ import *
import tensorflow as tf
import cv2
import numpy as np
from model import train_op
import Augmentor
from tensorflow.contrib.framework.python.framework import load_checkpoint

import json


def build_eval_fn():
    with open('/home/bltar/HopHacksDreamTeam/model/data.json') as json_file:  
        data = json.load(json_file)

    data = [x for x in data if x["image"] != ""]
    images = []
    for d in data:
        img = cv2.imread('/home/bltar/HopHacksDreamTeam/model/evals/' + d['image'], 3)
        img = cv2.resize(img, (1000, 1000))
        images.append(img)
    images = np.array(images)
    g = tf.Graph()
    with g.as_default():
        noisy_inputs = tf.placeholder(tf.float32 ,[None, WIDTH, HEIGHT, CHANNELS])
        inputs = tf.placeholder(tf.float32, [None, WIDTH, HEIGHT, CHANNELS])
        train = train_op(g, noisy_inputs, inputs)
        
        saver = tf.train.Saver()
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, "{}/model.ckpt-{}".format(CHECKPOINTS_DIR, 692))
        
        right_normed = tf.nn.l2_normalize(g.get_tensor_by_name("right:0"))
        [vectors] = sess.run([right_normed], feed_dict={inputs: images})
        
        def eval_fn(query):
            if type(query) == None:
                return {"has_mural": False}

            left_normed = tf.nn.l2_normalize(tf.transpose(g.get_tensor_by_name("left:0")))
            [current] = sess.run([left_normed], feed_dict={noisy_inputs: query})

            ## TODO: Review math. something might be fishy.
            result = np.matmul(vectors, current)
            index = np.argmax(result)
            print("Neural net results: ", result[index], index)      
            # Empirically determined threshhold.
            if result[index] > THRESHOLD:
                ## TODO: Return metadata associated with this index.
                meta = data[index]
                meta["has_mural"] = True
                return meta
            else:
                return {"has_mural": False}

        return eval_fn

eval_fn = build_eval_fn()

# example
eval_fn(np.random.rand(1, 1000, 1000, 3))
