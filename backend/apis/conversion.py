import tensorflow as tf
from keras.models import load_model

MODEL = "7hours"

def custom_loss(y_true, y_pred):
    weights = tf.where(tf.equal(y_true, 0), 0.1, 1.0)
    loss = tf.reduce_sum(tf.square(y_true - y_pred) * weights) / tf.reduce_sum(weights)
    return loss

model = tf.keras.models.load_model(f"./models/{MODEL}.keras", custom_objects={'custom_loss': custom_loss})
model.save('model.h5')
loadedModel = load_model('model.h5', custom_objects={'custom_loss': custom_loss})