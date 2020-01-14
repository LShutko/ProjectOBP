import PySimpleGUI as sg
import sys
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# from graphs import PlotChart


class Interface(object):

    def __init__(self, settings):
        self.window = sg.Window('Bacterial spot prediction', self.define_layout(), default_element_size=(30, 1),
                                grab_anywhere=False)
        self.graph_refresh = {
            'Tomato': self.refresh_plots,
            'Potato': self.refresh_plots,
            'Pepperbell': self.refresh_plots,
            'all': self.refresh_plots,
            'pie_chart': self.refresh_plots,
            'bar_chart': self.refresh_plots
        }
        self.dispatch_dictionary = {
            'Load the data': self.load,
            'Source code': self.source_code,
            'User manual': self.user_manual,
            'Export': self.export
        }
        self.settings = settings
        self.input_directory = './input/'  # location of the training set data

    def create_window(self, layout):
        return

    # Matplotlib helper code for embedded canvas
    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    def load(self):
        fname = sys.argv[1] if len(sys.argv) > 1 else sg.popup_get_file('Document to open')
        if not fname:
            sg.popup("Cancel", "No filename supplied")
            raise SystemExit("Cancelling: no filename supplied")
        else:
            print(fname)

    def load_training(self):
        names, sizes = self.get_data(self.input_directory)
        fig = plt.gcf()  # if using Pyplot then get the figure from the plot

        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
        my_canvas = self.window.FindElement('canvas')
        #    my_canvas.set_size(figure_w, figure_h)
        fig_photo = self.draw_figure(my_canvas.TKCanvas, fig)
        return fig_photo

    def source_code(self):
        sg.SetOptions(text_justification='right')
        layout = [[sg.Text('Link to the GitHub', font=('Helvetica', 10))]]

        window = sg.Window('Source code', layout, font=("Helvetica", 12))

        event, values = window.read()

    def user_manual(self):
        sg.SetOptions(text_justification='right')
        layout = [[sg.Text('Here will be some description of user manual (help)', font=('Helvetica', 10))]]

        window = sg.Window('Source code', layout, font=("Helvetica", 12))

        event, values = window.read()

    def export(self):
        sg.SetOptions(text_justification='right')
        layout = [[sg.Text('Here files will be exported', font=('Helvetica', 10))]]

        window = sg.Window('Source code', layout, font=("Helvetica", 12))

        event, values = window.read()

    def refresh_plots(self, tkfig):
        ctr_plant = ['Tomato', 'Potato', 'Pepperbell', 'all']

        if self.window.FindElement('pie_chart').Get():
            chart_type = 'pie'
        else:
            chart_type = 'bar'
        fig = plt.gcf()  # if using Pyplot then get the figure from the plot
        fig.clf()
        names, sizes = self.get_data(self.input_directory)
        for plant in ctr_plant:
            if self.window.FindElement(plant).Get() > 0:
                print('TODO')
                # TODO: descriptive_text, plot = PlotChart(names, sizes, plant, chart_type)
        tkfig.draw()

    @staticmethod
    def define_layout():
        sg.ChangeLookAndFeel('Material1')

        home_tab_layout = [
            [sg.Text('Welcome!', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
            [sg.Text('Bacterial spot detection', size=(35, 1), justification='center', font=("Helvetica", 20),
                     relief=sg.RELIEF_RIDGE)],

            [sg.Text('_' * 80)],
            [sg.Text('For uploading the data, click the button below', size=(71, 1), justification='center')],
            [sg.Text('Your folder', size=(23, 1), auto_size_text=False, justification='right'),
             sg.Button('Load the data', size=(30, 1))],
            [sg.Text('Requirements for uploaded folder: not zip...', size=(73, 1), justification='center')],
            [sg.Text('_' * 80)],
            [sg.Text('Group 1', size=(50, 1), justification='center', font=("Helvetica", 15), relief=sg.RELIEF_RIDGE)],
            [sg.Text('Tim, Paulo, Lena, Olga, Stephan', size=(67, 1), justification='center', font=("Helvetica", 10),
                     relief=sg.RELIEF_RIDGE)],
            [sg.Text('January, 2020', size=(68, 1), justification='center', font=("Helvetica", 10),
                     relief=sg.RELIEF_RIDGE)]]

        visual_tab_layout = [
            [sg.Text('For uploading the data, click the button below', size=(71, 1), justification='center')],
            [sg.Text('Your folder', size=(23, 1), auto_size_text=False, justification='right'),
             sg.Button('Load the training set data', size=(30, 1))],
            [sg.Text('Requirements for uploaded folder: not zip...', size=(73, 1), justification='center')],
            [sg.Text('_' * 90)],
            [sg.Frame("Select Plants", [
                [sg.Checkbox('Tomato', size=(12, 1), enable_events=True, key='Tomato')],
                [sg.Checkbox('Potato', size=(12, 1), enable_events=True, key='Potato')],
                [sg.Checkbox('Pepperbell', size=(12, 1), enable_events=True, key='Pepperbell')],
                [sg.Checkbox('All', size=(12, 1), enable_events=True, default=True, key='all')]
            ]),
             sg.T(' ' * 80),
             sg.Frame("Select Chart Type", [
                 [sg.Radio('Pie Chart', 'chart_type', size=(12, 2), default=True, enable_events=True, key='pie_chart')],
                 [sg.Radio('Bar Chart', 'chart_type', size=(12, 2), enable_events=True, key='bar_chart')]])
             ],
            [sg.Canvas(size=(100, 100), key='canvas')]
        ]

        pred_tab_layout = [[sg.T('This is prediction ')]]

        layout = [
            [sg.TabGroup([[sg.Tab('Home', home_tab_layout),
                           sg.Tab('Visualisation', visual_tab_layout),
                           sg.Tab('Prediction', pred_tab_layout)]])],
            [sg.Quit(tooltip='Click to quit')]
        ]

        return layout
