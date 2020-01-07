import cv2
import numpy as np
import pickle
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import LabelBinarizer


class Processing(object):

    def __init__(self, settings):
        self.settings = settings
        self.image_size = tuple((settings['width'], settings['height']))

    def process_image(self, image_path):
        image = cv2.imread(image_path)
        if image is not None:
            image_resized = cv2.resize(image, self.image_size)
            array = img_to_array(image_resized) / 225.0
        else:
            array = np.array([])
        return array

    def transform(self, image_list, label_list):

        labelbinarizer = LabelBinarizer()
        image_labels = labelbinarizer.fit_transform(label_list)

        pickle.dump(labelbinarizer, open(self.settings['output_directory']+'label_transform.pkl', 'wb'))

        return np.asarray(image_list), image_labels
