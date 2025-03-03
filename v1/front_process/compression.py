import tensorflow as tf

def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        # BytesList won't unpack a string from an EagerTensor.
        value = value.numpy()
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


image_string = open("./tensorflow/txt/jpg/class 1/song1_1.0.jpg", 'rb').read()

feature = { "image_raw": _bytes_feature(image_string) }
tf_example = tf.train.Example(features=tf.train.Features(feature=feature))


with tf.io.TFRecordWriter("./tensorflow/txt/example.tfrecords") as writer:
    writer.write(tf_example.SerializeToString())

