import yaml

from src.Reader import Reader
from src.Model import Model
from src.ModelPyTorch import ModelPytorch

if __name__ == '__main__':
    print(f"Starting up")

    # Read in project settings
    with open('settings.yml', 'r') as f:
        SETTINGS = yaml.load(f, Loader=yaml.FullLoader)

    # Initialize reader for  training_data and new images
    reader = Reader(SETTINGS)
    images, labels = reader.load_train_data()

    dataloader = reader.load_dataloader()

    # Train the CNN with preset settings
    #Model(SETTINGS, len(labels[0])).run(images, labels)
    ModelPytorch(SETTINGS).run_model(dataloader)
