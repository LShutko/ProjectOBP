import yaml

from src.Loader import Loader
from src.Model import Model
from src.GUI import Interface

if __name__ == '__main__':
    print(f"Starting up")

    # Read in project settings
    with open('settings.yml', 'r') as f:
        SETTINGS = yaml.load(f, Loader=yaml.FullLoader)

    # Initialize reader loading new images
    reader = Loader(SETTINGS)

    # Define model and load in weights
    predictor = Model(SETTINGS)
    nn = predictor.load()

    # Start up interface
    gui = Interface(SETTINGS)

    # Event loop. Read buttons, make callbacks
    while True:
        # Read the Window
        event, value = gui.window.read()

        if event in ('Quit', None):
            break
        # Lookup event in function dictionary
        elif event in gui.dispatch_dictionary:
            if event == 'Load data':
                func_to_call = gui.dispatch_dictionary[event]  # get function from dispatch dictionary
                input_directory = func_to_call()
                image_list = reader.load_test_data(input_directory)

                y_probabilities = predictor.predict_batch(nn, image_list)
                y_predictions = y_probabilities.argmax(axis=1)
                #TODO: Continue here...

            else:
                gui.dispatch_dictionary[event]
                func_to_call()
        else:
            print('Event {} not in dispatch dictionary'.format(event))
    gui.window.read()

