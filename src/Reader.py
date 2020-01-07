import os
import numpy as np
from src.Processing import Processing


class Reader(object):

    def __init__(self, settings):
        self.settings = settings

    def load_train_data(self):
        print(f"Loading images")
        image_list = []
        label_list = []

        for plant_label in os.listdir(self.settings['input_directory']):
            print(f"    Loading {plant_label}...")
            image_list_single_label = os.listdir(self.settings['input_directory'] + plant_label)

            for image in image_list_single_label:
                image_list.append(Processing(self.settings).process_image(
                    self.settings['input_directory'] + plant_label + '/' + image))
                label_list.append(plant_label)

        print(f"loaded {len(label_list)} images")

        print(f"Return transformed images and labels")
        return Processing(self.settings).transform(image_list, label_list)
