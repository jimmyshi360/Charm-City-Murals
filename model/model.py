# Note, unstable. Just pushing upto server before finishing off.
from tensorflow.contrib.layers import convolution2d, dropout, repeat
from tensorflow.contrib.learn.python.learn.estimators import model_fn
g = tf.Graph()

BATCH_SIZE = 32
WIDTH = 1000
HEIGHT = 1000
CHANNELS = 3

def add_noise(images):
    p = Augmentor.DataPipeline(images)
    p.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=8)
    p.flip_left_right(probability=0.5)
    p.flip_top_bottom(probability=0.5)

    augmented_images, _ = p.sample(100)
    return augmented_images

def left_tower(inputs):
    # This is built on top of the existing network.
    composites = inputs, counter_examples
    left_conv = convolution2d(inputs=composites, num_outputs=16, kernel_size=5, stride=5,
            padding='SAME', activation_fn=tf.nn.tanh, scope='left_conv')
    left_pooled = tf.reshape(c3, [-1, 8 * 8 * 64])
    return tf.layers.dense(inputs=left_conv, units=1024, activation=tf.nn.tanh)

def right_tower(inputs, weights):
    # Note that this scoping scheme must match the weights imported.
    c1 = convolution2d(inputs=inputs, num_outputs=16, kernel_size=5, stride=5,
            padding='SAME', activation_fn=tf.nn.tanh, scope='conv1')
    c2 = convolution2d(inputs=c1, num_outputs=32, kernel_size=5, stride=5,
            padding='SAME', activation_fn=tf.nn.tanh, scope='conv2')
    c3 = convolution2d(inputs=c2, num_outputs=64, kernel_size=5, stride=5,
            padding='SAME', activation_fn=tf.nn.tanh, scope='conv3')

    right_pooled = tf.reshape(c3, [-1, 8 * 8 * 64])
    return tf.layers.dense(inputs=right_pooled, units=1024,
            activation=tf.nn.tanh)

def model_fn(g, inputs, counter_examples, weights):
  with g.as_default():
    [noisy_inputs] = add_noise([inputs])
    composites = counter_examples

    labels = tf.identity(
            np.range(BATCH_SIZE, dtype=np.int32), name="labels")

    left = left_tower(noisy_inputs)
    right = right_tower(composites)
    logits = tf.matmul(left, right)

    tf.losses.softmax_cross_entropy(logits=logits, labels=labels)
    train_op = tf.contrib.layers.optimize_loss(loss=loss,
            global_step=tf.contrib.framework.get_global_step(),
            optimizer="Adam", learning_rate=LEARN_RATE)

    return train_op
