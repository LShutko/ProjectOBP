import os
from src.Processing import Processing


class Reader(object):

    def __init__(self, settings):
        self.settings = settings

    def read_params(self):
        return

    def load_train_data(self):
        print(f"[INFO] Loading images")
        image_list = []
        label_list = []

        for plant_label in os.listdir(self.settings['input_directory']):
            print(f"    [INFO] Loading {plant_label}...")
            image_list_single_label = os.listdir(self.settings['input_directory'] + plant_label)

            for image in image_list_single_label:
                image_list.append(Processing(self.settings).process_image(
                    self.settings['input_directory'] + plant_label + '/' + image))
                label_list.append(plant_label)

        print(f"[INFO] loaded {len(label_list)} images")

        print(f"[INFO] Transforming labels")
        label_list = Processing(self.settings).transform_labels(label_list)

        return image_list, label_list
