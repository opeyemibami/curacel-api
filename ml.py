import numpy as np
from skimage.transform import resize
from keras.preprocessing.image import load_img
from keras.models import load_model


model = load_model('model.h5')


def get_prediction(filename):
    image = load_img(filename, target_size=(224, 224))
    image = image.resize((224, 224))
    im_resized = resize(np.asarray(image), (224, 224, 3))
    grayy = resize(np.asarray(im_resized), (224, 224, 1))
    

    pred = model.predict_classes(np.expand_dims(grayy, 0))[0][0]
    if pred == 1: 
        confidence_level = (model.predict(np.expand_dims(grayy, 0))[0][0]*100).round(2)
    else:
        confidence_level = 100 - (model.predict(np.expand_dims(grayy, 0))[0][0]*100).round(2)

    return pred,confidence_level
