import yaml
from src.Reader import Reader
from src.Model import Model

if __name__ == '__main__':
    print(f"[INFO] Starting up")

    # Read in project settings
    with open('settings.yml', 'r') as f:
        SETTINGS = yaml.load(f, Loader=yaml.FullLoader)

    # Initialize reader for params, training_data, new images
    reader = Reader(SETTINGS)
    params = reader.read_params()

    images, labels = reader.load_train_data()
    print(f"[INFO] loaded {len(images)} images")

    Model(SETTINGS).run(images, labels)
