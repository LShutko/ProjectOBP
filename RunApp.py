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
    layout = gui.define_layout()
    gui.create_window(layout)

    # Event loop. Read buttons, make callbacks
    while True:
        # Read the Window
        event, value = gui.window.read()
        if event in ('Quit', None):
            break
        # Lookup event in function dictionary
        if event in gui.dispatch_dictionary:
            func_to_call = gui.dispatch_dictionary[event]  # get function from dispatch dictionary
            func_to_call()
        elif event == "Load the training set data":
            tkfig = gui.LoadTraining()
        elif event in gui.graph_refresh:
            gui.RefreshPlots(tkfig)
        else:
            print('Event {} not in dispatch dictionary'.format(event))
    gui.window.read()

