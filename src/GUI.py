import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
import os
import webbrowser

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# from graphs import PlotChart

class Interface(object):

    def __init__(self, settings):

        sg.ChangeLookAndFeel('Material1')

        self.chart_type = 'pie'
        self.plant = 'all'
        self.image_element = sg.Image(r'plots\pie_all.png', key='canvas', size=(640,480))
        self.image_element_pred = sg.Image(r'plots\fantom.png',  key='canvas_pred')
        self.slider = sg.Slider((1, 1), key='Slider', orientation='h', enable_events=True, disable_number_display=True)
        self.file_num_left = sg.Text('0')
        self.file_num_right = sg.Text('0', size=(1,1))
        self.file_number = sg.Text('0', size=(1,1))
        self.image_file_name = sg.Text('', size=(1,1))
        self.image_number = sg.Text('', size=(1,1))
        self.image_predic_class = sg.Text('', size=(1,1))
        self.predict_certainty = sg.Text('', size=(1,1))
        self.file_listbox = sg.Listbox(values=[], enable_events=True, size=(40, 20), background_color='White', text_color='Black', key='listbox')
        self.pred_stat_listbox = sg.Listbox(values=[], enable_events=False, size=(45, 10), background_color='White',
                                            text_color='Black', select_mode = sg.LISTBOX_SELECT_MODE_MULTIPLE )
        self.graph_refresh = {
            'Tomato': self.update_plots,
            'Potato': self.update_plots,
            'Pepperbell': self.update_plots,
            'all': self.update_plots,
            'pie': self.update_plots,
            'bar': self.update_plots
        }
        self.dispatch_dictionary = {
            'Browse': self.load,
            'Source code': self.source_code,
            'User Manual': self.user_manual,
            'Documentation': self.docum_manual,
            'Save as': self.save_pred_details,
            'Filter': self.filter_results
             }
        self.predic_browsing = {            # mouse scrolling/slider/arrow, PgUp-PgDn keys/list events at Prediction page
            'Slider': self.update_predict_display,
            'Down:40':self.update_predict_display,
            'Next:34': self.update_predict_display,
            'Up:38': self.update_predict_display,
            'Prior:33': self.update_predict_display,
            'Next': self.update_predict_display,
            'Prev': self.update_predict_display,
            'MouseWheel:Down': self.update_predict_display,
            'MouseWheel:Up': self.update_predict_display,
            'listbox': self.update_predict_display

        }

        self.class_dictionary = {           #Model class labels
            0: 'Pepperbell_bacterial_spot',
            1: 'Pepperbell_healthy',
            2: 'Potato_early_blight',
            3: 'Potato_healthy',
            4: 'Potato_late_blight',
            5: 'Tomato_mosaic_virus',
            6: 'Tomato_spider_mites_2_spotted_spider_mite',
            7: 'Tomato_yellow_leaf_curl_virus',
            8: 'Tomato_bacterial_spot',
            9: 'Tomato_early_blight',
            10: 'Tomato_healthy',
            11: 'Tomato_late_blight',
            12: 'Tomato_leaf_mold',
            13: 'Tomato_septoria_leaf_spot',
            14: 'Tomato_target_spot'
        }

        self.settings = settings
        self.manual_file = self.settings['manual_file']
        self.document_file = self.settings['document_file']
        self.github_code=self.settings['github_code']
        self.startup_window = sg.Window('Starting up',
                                        self.define_layout('startup'),
                                        default_element_size=(30, 1),
                                        grab_anywhere=True)


        self.window = sg.Window('Bacterial spot prediction',
                                    self.define_layout('home'),
                                    return_keyboard_events=True,
                                    grab_anywhere=False,
                                    location=(0, 0))





    def get_img_data(self, f, maxsize=(256, 256)):  # PIL function to read one file and convert to PNG
        img = Image.open(f)
        img.thumbnail(maxsize)
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()

    def update_plots(self):
        img_path = 'plots/'+self.chart_type+'_'+self.plant+'.png'

        return self.image_element.update(data=self.get_img_data(img_path,(640,480)))

    def update_test_image(self, image):
        return self.image_element_pred.update(data=image)



    def update_predict_display(self, path_dir, number, pred_class, y_certainty): # refresh image and file info for scrolling/slider/key/list events

        list_b = self.file_listbox.get_list_values()
        fname = list_b[number]
        path = path_dir+"/"+fname
        self.update_test_image(self.get_img_data(path))

        self.image_file_name.set_size(size=(len(fname), 1))
        self.image_file_name.update(value=fname)

        self.image_number.set_size(size=(len(str(number+1)), 1))
        self.image_number.update(value=str(number+1))

        self.image_predic_class.set_size(size=(len(self.class_dictionary[pred_class]), 1))
        self.image_predic_class.update(value=self.class_dictionary[pred_class])

        certain = str(round(y_certainty,3)) + "%"
        self.predict_certainty.set_size(size=(len(certain), 1))
        self.predict_certainty.update(value=certain)


    def filter_results(self, image_file_list, pred_class_list, y_certainty):
        image_file_list_filter = []
        y_predictions_filter = []
        y_certainty_filter =[]
        list_selected_classes = []
        for i in self.pred_stat_listbox.get_indexes():
            s = self.pred_stat_listbox.get_list_values()[i]
            list_selected_classes.append(s.split(":")[0])

        if len(list_selected_classes) ==0:
            return image_file_list, pred_class_list

        for i in range(len(image_file_list)):
            for j in list_selected_classes:
                if j == self.class_dictionary[pred_class_list[i]]:
                    image_file_list_filter.append(image_file_list[i])
                    y_predictions_filter.append(pred_class_list[i])
                    y_certainty_filter.append(y_certainty[i])
        self.file_listbox.update(values=image_file_list_filter)
        return image_file_list_filter, y_predictions_filter, y_certainty_filter

    def reset_predict_display(self):
        self.update_test_image(self.get_img_data(r'plots\fantom.png'))
        self.file_listbox.update(values=[])
        self.pred_stat_listbox.update(values=[])
        self.slider.Update(range=(0, 0))
        self.file_num_left.update("")
        self.file_num_right.update("")
        self.file_number.update("")
        self.image_predic_class.update("")
        self.image_number.update('')
        self.image_file_name.update("")
        self.predict_certainty.update('')



    def init_model_controls(self, image_file_list):   # set up controls and image file info after test dataset upload
        image_set_size = len(image_file_list)
        self.file_listbox.update(values=image_file_list)
        self.slider.Update(range=(1,image_set_size))
        self.file_num_left.update("1")
        self.file_num_right.set_size(size=(len(str(image_set_size)),1))
        self.file_num_right.update(value=str(image_set_size))
        self.file_number.set_size(size=(len(str(image_set_size)), 1))
        self.file_number.update(value=len(image_file_list))

    def init_dataset_statistics (self, data_stat):
        classes_out = []  #string list to display in a listbox
        class_dict = {} # dictionary, will contain <class_name>:<percentage>
        for i in range (0, len(data_stat)):  #populating a dictionary
            if data_stat[i] > 0:
                class_dict[self.class_dictionary[i]]=data_stat[i]
        classes_sorted = sorted(class_dict.items(), key=lambda x: x[1], reverse=True) #sorting class_dict by value
        for i in  classes_sorted:
           classes_out.append(i[0]+': '+str(i[1])+"%") #composing the string list
        self.pred_stat_listbox.update(values=classes_out)
        self.pred_stat_listbox.update(set_to_index=None)
        return classes_out


    def define_layout(self, mode):
        if mode == 'home':

            home_tab_layout = [
                [sg.Text(' '*7, size=(37, 1), justification='center', font=("Helvetica", 35),
                         relief=sg.RELIEF_RIDGE)],
                [sg.Text('Welcome!', size=(37, 2), justification='center', font=("Helvetica", 35), text_color='Black',
                         relief=sg.RELIEF_RIDGE)],
                [sg.Text('Bacterial Spot Detection', size=(43, 1), justification='center',font=("Helvetica", 30), text_color='Darkblue',
                         relief=sg.RELIEF_RIDGE)],
                [sg.Text('_'*145, justification='center')],
                [sg.Text('Project: Optimization of Business Processes', size=(70, 2), justification='center',
                         font=("Helvetica", 17, 'bold'),
                         text_color='Black',
                         relief=sg.RELIEF_RIDGE)],
                [sg.Text('Yura Group 1:', size=(100, 1), justification='center',
                         font=("Helvetica", 12, 'underline bold'), relief=sg.RELIEF_RIDGE)],
                [sg.Text('Paulo Fijen', size=(110, 1), justification='center',
                         font=("Helvetica", 12), relief=sg.RELIEF_RIDGE)],
                [sg.Text('Tim Flikweert', size=(110, 1), justification='center',
                         font=("Helvetica", 12), relief=sg.RELIEF_RIDGE)],
                [sg.Text('Olga Konstantinova', size=(110, 1), justification='center',
                         font=("Helvetica", 12), relief=sg.RELIEF_RIDGE)],
                [sg.Text('Lena Shutko', size=(110, 1), justification='center',
                         font=("Helvetica", 12), relief=sg.RELIEF_RIDGE)],
                [sg.Text('Stephan van der Kolff', size=(110, 5), justification='center',
                         font=("Helvetica", 12), relief=sg.RELIEF_RIDGE)],
                [sg.Text(" "*73), sg.Button("User Manual", size=(15,1)), sg.Button("Documentation", size=(15,1)),
                 sg.Button("Source code", size=(15,1)), sg.Text('v3.6\tJanuary, 2020', size=(37, 1), justification='right', font=("Helvetica", 10))]
            ]

            visual_tab_layout = [
                [sg.Frame(" 1. Select Plants ", [
                    [sg.Radio('All', group_id='plant_type', default=True, size=(12, 1), enable_events=True, key='all')],
                    [sg.Radio('Tomato', group_id='plant_type', default=False, size=(12, 1), enable_events=True,
                              key='Tomato')],
                    [sg.Radio('Potato', group_id='plant_type', default=False, size=(12, 1), enable_events=True,
                              key='Potato')],
                    [sg.Radio('Pepperbell', group_id='plant_type', default=False, size=(12, 1), enable_events=True,
                              key='Pepperbell')],
                ]),
                 sg.Frame(" 2. Chart Type ", [
                     [sg.Radio('Pie Chart', group_id='chart_type', default=True, size=(10, 2), enable_events=True,
                               key='pie')],
                     [sg.Radio('Bar Chart', group_id='chart_type', default=False, size=(10, 2), enable_events=True,
                               key='bar')]
                 ]),
                 self.image_element
                 ]
            ]
            model_col_image = [[self.image_element_pred]]
            model_col_files = [[self.file_listbox ],
                         [sg.Button('Prev', size=(8, 2)), sg.Button('Next', size=(8, 2))]]
            model_col_image_file = [[sg.Text("File name: ")],
                                    [self.image_file_name],
                                    [sg.Text("File number "), self.image_number, sg.Text("of "), self.file_number],
                                    [sg.Text("Predicted class: ")],
                                    [self.image_predic_class],
                                    [sg.Text('Certainty: '), self.predict_certainty],
                                    [sg.Text("Dataset prediction details", font=("Helvetica", 15, 'bold'), size=(25, 1), justification='left')],
                                    [self.pred_stat_listbox],
                                    [sg.Button('Export details', size=(10, 2), key='Save as'),
                                     sg.Button('Filter selection', size=(10, 2), key='Filter')]]
            model_tab_layout = [
                [sg.Text(' ')],
                [sg.Text('Select Your Folder', size=(25, 1), auto_size_text=False, justification='left')],
                [sg.Button('Browse', size=(20, 1))],
                [sg.Text('_'*50)],
                [sg.Text('Leaf Demonstration'), sg.Text('', key='_OUTPUT_')],
                [self.file_num_left, self.slider, self.file_num_right],
                [sg.Column(model_col_files ), sg.Column(model_col_image),  sg.Column(model_col_image_file)],

                #, sg.Column(model_col_image_file)
            ]

            layout = [
                [sg.TabGroup([[sg.Tab('Home', home_tab_layout),
                               sg.Tab('Visualisation', visual_tab_layout),
                               sg.Tab('Prediction', model_tab_layout)]])],
                [sg.Quit(tooltip='Click to quit')]
            ]
            return layout

        elif mode == 'startup':
            startup_layout = [
                [sg.Text(' ')],
                [sg.Text('Bacterial Spot Detector', size=(22, 2), justification='center', font=("Helvetica", 14))],
                [sg.Image(r'plots\leaf.png')],
                [sg.Text(' ')],
                [sg.Button('Press Here To Start', size=(32, 2))],
                [sg.Text('Note: loading may take a few seconds.', size=(32, 2), justification='center')]
            ]
            return startup_layout

    def load(self):
        self.input_directory = sg.popup_get_folder('Select folder')
        if self.input_directory == "":
            sg.popup("No valid dataset directory provided!")
        else:
            return self.input_directory

    def save_pred_details(self,path, image_file_list, y_predictions, y_certainty):
        file_name = sg.PopupGetFile('Enter Filename', save_as=True, default_path="results.txt",default_extension='txt')
        if not file_name:
            sg.popup("Please enter the file name")
        else:
            file = open(file_name, "w")
            file.write("Prediction details of the dataset "+path+'\n')
            file.write("Number of files: ")
            file.write(str(len(os.listdir(path))) + '\n')

            for line in self.pred_stat_listbox.GetListValues():
                file.write(line + '\n')
            class_sel =  self.pred_stat_listbox.get_indexes()

            file.write("\n")
            file.write("Selected classes: ")
            if len(class_sel) > 0:
                j=0
                for i in class_sel:
                    j+=1
                    s = self.pred_stat_listbox.get_list_values()[i]
                    file.write(s.split(":")[0])

                    if j < len(class_sel):
                        file.write(', ')

            else:
                file.write("all \n")
            file.write("\n")
            file.write("\n")
            for i in range(len(image_file_list)):
                certain = str(round(y_certainty[i], 3)) + "%"
                file.write(image_file_list[i] + ": "+ self.class_dictionary[y_predictions[i]] + " " + certain )
                file.write("\n")

            file.close()



    def popup_note(self, text):
        sg.popup(text)

    def user_manual(self):
        os.startfile(self.manual_file)

    def docum_manual(self):
        os.startfile(self.document_file)

    def source_code(self):
        webbrowser.open(self.github_code)

    # Matplotlib helper code for embedded canvas
    @staticmethod
    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg


    def export():
        sg.SetOptions(text_justification='right')
        layout = [[sg.Text('Here files will be exported', font=('Helvetica', 10))]]

        window = sg.Window('Source code', layout, font=("Helvetica", 12))

        event, values = window.read()