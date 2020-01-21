import PySimpleGUI as sg
from PIL import Image, ImageTk
import io

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# from graphs import PlotChart

class Interface(object):

    def __init__(self, settings):

        sg.ChangeLookAndFeel('Material2')
        self.chart_type = 'pie'
        self.plant = 'all'
        self.image_element = sg.Image(r'plots\pie_all.png', key='canvas', size=(640,480))
        self.image_element_pred = sg.Image(r'plots\fantom.png',  key='canvas_pred')
        self.slider = sg.Slider((1, 1), key='Slider', orientation='h', enable_events=True, disable_number_display=True)
        self.file_num_left = sg.Text('0')
        self.file_num_right = sg.Text('0', size=(15,1))
        self.file_number = sg.Text('0', size=(15,1))
        self.image_file_name = sg.Text('', size=(10,1))
        self.image_number = sg.Text('', size=(1,1))
        self.image_predic_class = sg.Text('', size=(10,1))
        self.file_listbox = sg.Listbox(values=[], enable_events=True, size=(40, 20), background_color='White', text_color='Black', key='listbox')
        self.pred_stat_listbox = sg.Listbox(values=[], enable_events=False, size=(45, 15), background_color='White', text_color='Black')
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
            'User manual': self.user_manual,
            'Export': self.export
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
            5: 'Tomato_bacterial_spot',
            6: 'Tomato_early_blight',
            7: 'Tomato_healthy',
            8: 'Tomato_late_blight',
            9: 'Tomato_leaf_mold',
            10: 'Tomato_septoria_leaf_spot',
            11: 'Tomato_target_spot',
            12: 'Tomato-mosaic_virus',
            13: 'Tomato-spider_mites_2_spotted_spider_mite',
            14: 'Tomato-yellow_leaf_curl_virus'
        }

        self.settings = settings
        self.input_directory = ""
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

    def update_predict_display(self, path_dir, fname, number, pred_class): # refresh image and file info for scrolling/slider/key/list events

        path = path_dir+"/"+fname
        self.update_test_image(self.get_img_data(path))

        self.image_file_name.set_size(size=(len(fname), 1))
        self.image_file_name.update(value=fname)

        self.image_number.set_size(size=(len(str(number+1)), 1))
        self.image_number.update(value=str(number+1))

        self.image_predic_class.set_size(size=(len(self.class_dictionary[pred_class]), 1))
        self.image_predic_class.update(value=self.class_dictionary[pred_class])


    def init_model_controls(self, image_file_list):   # set up controls and image file info after test dataset upload
        image_set_size = len(image_file_list)
        self.file_listbox.update(values=image_file_list)
        self.slider.Update(range=(1,image_set_size))
        self.file_num_left.update("1")
        self.file_num_right.set_size(size=(len(str(image_set_size)),1))
        self.file_num_right.update(value=str(image_set_size))
        self.file_number.set_size(size=(len(image_file_list), 1))
        self.file_number.update(value=len(image_file_list))

    def init_dataset_statistics (self, data_stat):
        classes_out = []
        for i in range (0, len(data_stat)):
            if data_stat[i] > 0:
                classes_out.append(self.class_dictionary[i]+': '+str(data_stat[i])+"%")

                self.pred_stat_listbox.update(values=classes_out)
        return classes_out


    def define_layout(self, mode):
        if mode == 'home':

            home_tab_layout = [
                [sg.Text('Bacterial Spot Detection', size=(50, 2), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.Text('_'*50, size=(50, 1), justification='center')],
                [sg.Text('Group 1: Tim, Paulo, Lena, Olga, Stephan', size=(20, 2), justification='center',
                         font=("Helvetica", 12))],
                [sg.Text('v1.0\tJanuary, 2020', size=(50, 5), justification='center', font=("Helvetica", 10))]
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
                         [sg.Button('Next', size=(8, 2)), sg.Button('Prev', size=(8, 2))]]
            model_col_image_file = [[sg.Text("File name: "), self.image_file_name],[sg.Text("File number "),
                                 self.image_number, sg.Text("of "), self.file_number],
                                    [sg.Text("Predicted class: "), self.image_predic_class],
                                    [self.pred_stat_listbox]]
            model_tab_layout = [
                [sg.Text(' ')],
                [sg.Text('Select Your Folder', size=(25, 1), auto_size_text=False, justification='left')],
                [sg.Button('Browse', size=(20, 1))],
                [sg.Text('_'*50)],
                [sg.Text('Leaf Demonstration'), sg.Text('', key='_OUTPUT_')],
                [self.file_num_left, self.slider, self.file_num_right],
                [sg.Column(model_col_files ), sg.Column(model_col_image),  sg.Column(model_col_image_file)]
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
            sg.popup("Cancel", "No filename supplied")
            raise SystemExit("Cancelling: no filename supplied")
        else:
            return self.input_directory



    # Matplotlib helper code for embedded canvas
    @staticmethod
    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    @staticmethod
    def source_code():
        sg.SetOptions(text_justification='right')
        layout = [[sg.Text('Link to the GitHub', font=('Helvetica', 10))]]

        window = sg.Window('Source code', layout, font=("Helvetica", 12))

        event, values = window.read()

    @staticmethod
    def user_manual():
        sg.SetOptions(text_justification='right')
        layout = [[sg.Text('Here will be some description of user manual (help)', font=('Helvetica', 10))]]

        window = sg.Window('Source code', layout, font=("Helvetica", 12))

        event, values = window.read()

    @staticmethod
    def export():
        sg.SetOptions(text_justification='right')
        layout = [[sg.Text('Here files will be exported', font=('Helvetica', 10))]]

        window = sg.Window('Source code', layout, font=("Helvetica", 12))

        event, values = window.read()