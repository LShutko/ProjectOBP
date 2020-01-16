import PySimpleGUI as sg
import sys
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# from graphs import PlotChart

class Interface(object):

    def __init__(self, settings):

        sg.ChangeLookAndFeel('Material2')
        self.chart_type = 'pie'
        self.plant = 'all'
        self.graph_refresh = {
            'Tomato': self.update_plots(self.chart_type, 'Tomato'),
            'Potato': self.update_plots(self.chart_type, 'Potato'),
            'Pepperbell': self.update_plots(self.chart_type, 'Pepperbell'),
            'all': self.update_plots(self.chart_type, 'all'),
            'pie_chart': self.update_plots('pie', self.plant),
            'bar_chart': self.update_plots('bar', self.plant)
        }
        self.dispatch_dictionary = {
            'Load data': self.load,
            'Source code': self.source_code,
            'User manual': self.user_manual,
            'Export': self.export
        }
        self.settings = settings
        self.input_directory = ""
        self.startup_window = sg.Window('Starting up',
                                        self.define_layout('startup'),
                                        default_element_size=(30, 1),
                                        grab_anywhere=True)
        self.window = sg.Window('Bacterial spot prediction',
                                self.define_layout('home'),
                                default_element_size=(30, 1),
                                grab_anywhere=False)

    def open_gui(self):
        self.window = sg.Window('Bacterial spot prediction',
                                self.define_layout('home'),
                                default_element_size=(30, 1),
                                grab_anywhere=False)
        return

    def update_plots(self, chart_type, plant):
        return

    @staticmethod
    def define_layout(mode):
        if mode == 'home':

            home_tab_layout = [
                [sg.Text('Bacterial Spot Detection', size=(50, 2), justification='center', relief=sg.RELIEF_RIDGE)],
                [sg.Text('_' * 100, size=(100, 1), justification='center')],
                [sg.Text('Group 1: Tim, Paulo, Lena, Olga, Stephan', size=(20, 2), justification='center',
                         font=("Helvetica", 12))],
                [sg.Text('v1.0\tJanuary, 2020', size=(100, 5), justification='center', font=("Helvetica", 10))]
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
                               key='pie_chart')],
                     [sg.Radio('Bar Chart', group_id='chart_type', default=False, size=(10, 2), enable_events=True,
                               key='bar_chart')]
                 ]),
                 sg.Canvas(size=(100, 100), key='canvas')
                 ]
            ]

            model_tab_layout = [
                [sg.Text('Your folder', size=(23, 1), auto_size_text=False, justification='right'),
                 sg.Button('Load data', size=(30, 1))]
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
                [sg.Text('Welcome to the Bacterial Spot Detection', size=(20, 2), justification='center',
                         relief=sg.RELIEF_RIDGE)],
                [sg.Image(r'plots\leaf.png')],
                [sg.Button('Press Here To Start')],
                [sg.Text('Note: loading may take a few seconds.')]
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
