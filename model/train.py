from __init__ import *
import tensorflow as tf
import numpy as np
from model import train_op
import Augmentor
from tensorflow.contrib.framework.python.framework import load_checkpoint

def add_noise(images):
    p = Augmentor.DataPipeline(images)
    # p.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=8)
    p.flip_left_right(probability=0.5)
    p.flip_top_bottom(probability=0.5)

    augmented_images = p.sample(0)
    return augmented_images

def load(g):
    ckpt = load_checkpoint(FROZEN_CHECKPOINTS_DIR + "/model.ckpt")
    variables = {}
    vs = {
      "conv1/weights",
      "conv1/biases",
      "conv2/weights",
      "conv2/biases",
      "conv3/weights",
      "conv3/biases",
      "dense/kernel",
      "dense/bias",
    }
    for v in vs:
        print(v)
        variables[v + ":0"] = ckpt.get_tensor(v)
    return variables

def main():
    g = tf.Graph()
    with g.as_default():
        noisy_inputs = tf.placeholder(tf.float32 ,[None, WIDTH, HEIGHT, CHANNELS])
        inputs = tf.placeholder(tf.float32, [None, WIDTH, HEIGHT, CHANNELS])
        train = train_op(g, noisy_inputs, inputs)
        feed_dict = load(g) 

        inputs_gen = Augmentor.Pipeline(TRUE_DIR)
        inputs_gen.resize(probability=1.0, width=WIDTH, height=HEIGHT)
        inputs_gen = inputs_gen.keras_generator(batch_size=BATCH_SIZE)
        validation_gen = Augmentor.Pipeline(FALSE_DIR)
        validation_gen.random_distortion(probability=1., grid_width=4, grid_height=4, magnitude=8)
        validation_gen.resize(probability=1.0, width=WIDTH, height=HEIGHT)
        validation_gen = validation_gen.keras_generator(batch_size=BATCH_SIZE, scaled=True)
        saver = tf.train.Saver()
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            for i in range(TRAIN_STEP):
                feed_dict = {}
                feed_dict[inputs], _ = next(inputs_gen)
                validation, _ = next(validation_gen)
                saver.save(sess, "./checkpoints/baltar/model.ckpt-{}".format(i))
                feed_dict[noisy_inputs] = np.vstack([add_noise(feed_dict[inputs]), validation])
                sess.run([train], feed_dict=feed_dict)

main()
