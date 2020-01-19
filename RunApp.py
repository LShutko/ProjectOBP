import yaml
from src.GUI import Interface

if __name__ == '__main__':
    print(f"Starting up")

    # Read in project settings
    with open('settings.yml', 'r') as f:
        SETTINGS = yaml.load(f, Loader=yaml.FullLoader)

    # Start up interface
    gui = Interface(SETTINGS)
    gui.startup_window()

    # After pressing start in startup_window load in whole program
    from src.Loader import Loader
    from src.Model import Model

    # Initialize reader loading new images
    reader = Loader(SETTINGS)

    # Define model and load in weights
    predictor = Model(SETTINGS)
    nn = predictor.load()

    gui.startup_window.close()
    gui.window()

    # Event loop. Read buttons, make callbacks
    while True:
        # Read the Window
        event, value = gui.window.read()
        print(' ')
        if event in ('Quit', None):
            break
        # Lookup event in function dictionary
        elif event in gui.dispatch_dictionary:
            if event == 'Browse':
                print(' ')
                func_to_call = gui.dispatch_dictionary[event]  # get function from dispatch dictionary
                input_directory = func_to_call()

                image_list, image_file_list  = reader.load_test_data(input_directory)
                y_probabilities = predictor.predict_batch(nn, image_list)
                y_predictions = y_probabilities.argmax(axis=1)

                path = input_directory+"/"+image_file_list[0]
                gui.update_test_image(gui.get_img_data(path))
                gui.update_model_controls(len(image_file_list), image_file_list[0], y_predictions[0] )



            if event == 'Slider':
                img = int(value['Slider'])
                print(img)
                path = input_directory + "/" + image_file_list[img-1]
                gui.update_test_image(gui.get_img_data(path))
                gui.refresh_image_info(img, image_file_list[img-1], y_predictions[img-1])



        elif event in gui.graph_refresh:
            print('')
            if event in ['all', 'Tomato', 'Potato', 'Pepperbell']:
                gui.plant = event
            else:
                gui.chart_type = event
            func_to_call = gui.graph_refresh[event]
            func_to_call()
        else:
            print('Event {} not in dispatch dictionary'.format(event))
