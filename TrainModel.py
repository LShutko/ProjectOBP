import yaml

from src.Loader import Loader
from src.Model import Model
from src.ModelPyTorch import ModelPytorch

if __name__ == '__main__':
    print(f"Starting up")

    # Read in project settings
    with open('settings.yml', 'r') as f:
        SETTINGS = yaml.load(f, Loader=yaml.FullLoader)

    # Initialize reader for  training_data
    reader = Loader(SETTINGS)
    images, labels = reader.load_train_data()

    train_loader, validation_loader, data_loaders, data_lengths = reader.load_dataloader()

    # Train the CNN with preset settings
    Model(SETTINGS).run(images, labels)
    #ModelPytorch(SETTINGS, data_loaders, data_lengths).run_model(train_loader, validation_loader)
