import cv2
import numpy as np
import pickle

from sklearn.preprocessing import LabelBinarizer


class Processing(object):

    def __init__(self, settings):
        self.settings = settings
        self.image_size = tuple((settings['width'], settings['height']))

    def process_image(self, image_path):
        image = cv2.imread(image_path)
        if image is not None:
            image_resized = cv2.resize(image, self.image_size) / 225.0
        else:
            image_resized = np.array([])
        return image_resized

    @staticmethod
    def transform(image_list, label_list):

        if label_list:
            labelbinarizer = LabelBinarizer()
            image_labels = labelbinarizer.fit_transform(label_list)
        else:
            image_labels = None

        return np.asarray(image_list), image_labels
