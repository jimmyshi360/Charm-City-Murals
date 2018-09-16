from __init__ import *

import tensorflow as tf
import numpy as np
from tensorflow.contrib.layers import convolution2d, dropout, repeat
from tensorflow.contrib.learn.python.learn.estimators import model_fn

def create_labels():
    a = np.identity(BATCH_SIZE)
    b = np.zeros([BATCH_SIZE, BATCH_SIZE * 2])
    b[:BATCH_SIZE, :BATCH_SIZE] = a
    return b

def left_tower(inputs):
    # This is additional to the existing network.
    c1 = convolution2d(inputs=inputs, num_outputs=16, kernel_size=5, stride=5,
            padding='SAME', activation_fn=tf.nn.tanh, scope='lconv1')
    c2 = convolution2d(inputs=c1, num_outputs=32, kernel_size=5, stride=5,
            padding='SAME', activation_fn=tf.nn.tanh, scope='lconv2')
    c3 = convolution2d(inputs=c2, num_outputs=64, kernel_size=5, stride=5,
            padding='SAME', activation_fn=tf.nn.tanh, scope='lconv3')
    left_pooled = tf.reshape(c3, [-1, 8 * 8 * 64])
    d = tf.layers.dense(inputs=left_pooled, units=1024, activation=tf.nn.tanh)
    tf.identity(d, name="left")
    return d, [c1, c2, c3, d]

def right_tower(inputs):
    # Note that this scoping scheme must match the weights imported.
    trains = False
    c1 = convolution2d(inputs=inputs, num_outputs=16, kernel_size=5, stride=5,
            padding='SAME', activation_fn=tf.nn.tanh, scope='conv1', trainable=trains)
    c2 = convolution2d(inputs=c1, num_outputs=32, kernel_size=5, stride=5,
            padding='SAME', activation_fn=tf.nn.tanh, scope='conv2', trainable=trains)
    c3 = convolution2d(inputs=c2, num_outputs=64, kernel_size=5, stride=5,
            padding='SAME', activation_fn=tf.nn.tanh, scope='conv3', trainable=trains)

    right_pooled = tf.reshape(c3, [-1, 8 * 8 * 64])
    d = tf.layers.dense(inputs=right_pooled, units=1024,
            activation=tf.nn.tanh, trainable=trains)
    tf.identity(d, name="right")
    return d, [c1, c2, c3, d]

def train_op(g, noisy_inputs, inputs):
    # Construct the graph to train.

    labels = tf.identity(create_labels(), name="labels")

    left, var2 = left_tower(noisy_inputs)
    right, var = right_tower(inputs)
    logits = tf.matmul(right, tf.transpose(left))

    loss = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits_v2(
        logits=logits, labels=labels))

    tf.summary.scalar("loss", loss) 
    tf.summary.image("examples", noisy_inputs) 
    tf.summary.image("matching", tf.reshape(tf.nn.l2_normalize(logits), [1, BATCH_SIZE, BATCH_SIZE * 2, 1]))

    train_op = tf.train.AdamOptimizer(learning_rate=LEARN_RATE).minimize(loss=loss,
        global_step=tf.train.get_global_step())

    return train_op
