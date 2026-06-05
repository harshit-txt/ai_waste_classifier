import tensorflow as tf

IMAGE_SIZE = (224,224)
NUM_CLASSES = 4
BATCH_SIZE = 32

train_data = tf.keras.utils.image_dataset_from_directory(
    "data/train",
    image_size = IMAGE_SIZE,
    batch_size = BATCH_SIZE
)

val_data = tf.keras.utils.image_dataset_from_directory(
    "data/val",
    image_size = IMAGE_SIZE,
    batch_size = BATCH_SIZE
)

test_data = tf.keras.utils.image_dataset_from_directory(
    "data/test",
    image_size = IMAGE_SIZE,
    batch_size = BATCH_SIZE
)

normalisation = tf.keras.layers.Rescaling(1./255)

train_data = train_data.map(lambda x,y: (normalisation(x), y))
val_data = val_data.map(lambda x,y: (normalisation(x), y))
test_data =test_data.map(lambda x,y: (normalisation(x), y))

augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1)
])


train_data = train_data.map(lambda x,y: (augmentation (x, training = True) , y))

