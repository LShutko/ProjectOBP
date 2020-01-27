import yaml
import os
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
    test_data_loaded = False   #indication of the loaded dataset

    gui.startup_window.close()
    window = gui.window

    # Event loop. Read buttons, make callbacks
    while True:
        # Read the Window
        event, value = window.read()
        if event in ('Quit', None):
            break

        # Lookup event in function dictionary
        elif event in gui.dispatch_dictionary:
            if event == 'Browse':
                func_to_call = gui.dispatch_dictionary[event]  # get function from dispatch dictionary
                directory = func_to_call()

                if (directory is not None) and os.path.isdir(directory):
                    input_directory = directory
                    gui.update_test_image(gui.get_img_data(r'plots\data_loading.png'))
                    window.refresh()
                    image_list, image_file_list_orig  = reader.load_test_data(input_directory)
                    image_file_list = image_file_list_orig.copy()
                    if len(image_list)>0:
                        y_probabilities = predictor.predict_batch(nn, image_list)
                        y_predictions_orig = y_probabilities.argmax(axis=1)
                        y_predictions = y_predictions_orig.copy()

                        m = [0]*15  #calculating the percentage for each predicted class in the dataset
                        for i in y_predictions:
                            m[i]+=1
                        for i in range (0, len(m)):
                            m[i] = round(100*m[i]/len(y_predictions),2)

                        print(gui.init_dataset_statistics(m))
                        im_index = 0
                        test_data_loaded = True
                        path = input_directory+"/"+image_file_list[0]
                        gui.init_model_controls(image_file_list)  #set the slider, file name list
                        gui.update_predict_display(input_directory, im_index,y_predictions[im_index]) #load first image and update file info display

                    else:
                        gui.popup_note("No valid dataset directory provided! try again")
                        test_data_loaded = False
                        gui.reset_predict_display()



            if event == 'User Manual':
                func_to_call = gui.dispatch_dictionary[event]
                func_to_call()

            if event == 'Documentation':
                func_to_call = gui.dispatch_dictionary[event]
                func_to_call()

            if event == 'Source code':
                func_to_call = gui.dispatch_dictionary[event]
                func_to_call()

            if event == 'Save as':
                if test_data_loaded:
                    func_to_call = gui.dispatch_dictionary[event]  # get function from dispatch dictionary
                    func_to_call(input_directory, image_file_list, y_predictions)
                else:
                    gui.popup_note("Upload the data first!")

            if event == 'Filter':

                if test_data_loaded:
                    image_file_list = []
                    y_predictions = []
                    image_file_list, y_predictions = gui.filter_results(image_file_list_orig, y_predictions_orig)
                    im_index = 0
                    path = input_directory + "/" + image_file_list[0]
                    gui.init_model_controls(image_file_list)  # set the slider, file name list
                    gui.update_predict_display(input_directory, im_index, y_predictions[im_index])
                else:
                    gui.popup_note("Upload the data first!")




        elif ((event in gui.predic_browsing) and test_data_loaded):  #events on the Prediction tab
            if event == 'Slider':
                im_index = int(value['Slider'])-1
                gui.file_listbox.update(scroll_to_index=im_index, set_to_index=im_index)
                print(im_index)
            elif event == 'listbox':
                fname = value['listbox'][0]
                im_index = image_file_list.index(fname)
                gui.slider.update(value=im_index + 1)
            elif event in ('Prev', 'MouseWheel:Up', 'Up:38', 'Prior:33'):
                im_index -=1
                if im_index <0 :
                    im_index = 0
                gui.file_listbox.update(scroll_to_index=im_index, set_to_index=im_index)
                gui.slider.update(value=im_index + 1)
            elif event in ('Next', 'MouseWheel:Down', 'Down:40', 'Next:34'):
                im_index +=1
                if im_index >len(image_file_list)-1 :
                    im_index = len(image_file_list)-1
                gui.file_listbox.update(scroll_to_index=im_index,set_to_index=im_index)
                gui.slider.update(value=im_index + 1)

            func_to_call = gui.predic_browsing[event]  # get function from dispatch dictionary
            func_to_call(input_directory, im_index, y_predictions[im_index]) #call gui.update_predict_display function


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
