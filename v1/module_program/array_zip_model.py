import tensorflow as tf



#矩陣壓縮檔
def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        # BytesList won't unpack a string from an EagerTensor.
        value = value.numpy()
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def comprassion(array,file_firstname,zip_path):
    feature = { "array": _bytes_feature(tf.io.serialize_tensor(array).numpy()) }
    tf_example = tf.train.Example(features=tf.train.Features(feature=feature))
    with tf.io.TFRecordWriter(zip_path + "/" + file_firstname +  ".tfrecords") as writer:
            writer.write(tf_example.SerializeToString())


# zip_path+"/"+file_firstname+"_"+str(time/1)+".tfrecords"
        

# array = np.float32(np.arange(100).reshape(10,10))
# comprassion(array)