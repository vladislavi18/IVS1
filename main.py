import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_interactions import ioff, panhandler, zoom_factory

sg.theme("DarkTeal2")
header_list = ['DEVICE_ID', 'DATE', 'TIME', 'LATITUDE',
               'N/S', 'LONGTITUDE', 'E/W', 'SPEED', 'COURSE']

header_list_rus = ['id устройства', 'дата', 'время', 'широта',
                   'N/S', 'долгота', 'E/W', 'скорость', 'курс']


def read_file():
    filename = sg.popup_get_file(
        'Выберите файл: ',
        title='Открытие файла',
        no_window=False,
        file_types=(("Text Files", "*.txt"), ("CSV Files", "*.csv")))

    try:
        data_frame = pd.read_csv(filename, sep=',', engine='python',
                                 header=None, usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9])
        data = data_frame.values.tolist()
        return data_frame, data
    except:
        sg.popup_error('Не смог считать файл!')
        return


def draw_graph(xi, yi, date_frame):
    fig, ax = plt.subplots()
    ax.plot(date_frame[xi], date_frame[yi], color='red', linestyle='-',
            label='График {} от {}'.format(header_list_rus[xi - 1],
                                           header_list_rus[yi - 1]))
    ax.set_xlabel(header_list_rus[xi - 1])
    ax.set_ylabel(header_list_rus[yi - 1])

    disconnect_zoom = zoom_factory(ax)
    pan_handler = panhandler(fig)

    return fig


def conversion_to_normal_view(date_frame):
    date_frame_norm = []
    for item in date_frame[3]:
        hours = item // 10000
        minutes = (item % 10000) // 100
        seconds = (item % 100)
        date_frame_norm.append('{:02}:{:02}:{:02}'.format(hours, minutes, seconds))

    return date_frame_norm


def create_window_choice(data_norm):
    layout_select = [
        [sg.Text('Выберите элемент:')],
        [sg.Listbox(data_norm, size=(20, 30), key='-LISTBOX-')],
        [sg.Button('Выбрать', key='-SELECT-')],
    ]

    window_select = sg.Window('Выбор элемента', layout_select, modal=True)
    selected_item = data_frame[3][0]

    while True:
        event_select, values_select = window_select.read()

        if event_select == sg.WIN_CLOSED:
            break
        elif event_select == '-SELECT-':
            selected_item = values_select['-LISTBOX-'][0]
            break

    window_select.close()
    return selected_item


def create_layout(data, data_norm):
    table = [
        [sg.Text('Содержимое файла: ')],
        [sg.Table(values=data,
                  headings=header_list,
                  font='Helvetica',
                  pad=(25, 25),
                  display_row_numbers=True,
                  def_col_width=20,
                  num_rows=25)]
    ]

    layout1 = [sg.Canvas(key='-CANVAS1-',
                         size=(300, 200),
                         pad=(15, 15))]

    layout = [[sg.TabGroup([[sg.Tab('Таблица', [[sg.Column(table, element_justification='c')],
                                                [sg.Button('Закрыть', key='Exit')]])],
                            [sg.Tab('График', [[sg.Frame('График зависимости Широты от Долготы',
                                                         [layout1,
                                                          [sg.Button('Построить график', key='graph1')]]),
                                                sg.Frame('График зависимости Скорости от времени',
                                                         [[sg.Column([[sg.Canvas(key='-CANVAS2-',
                                                                                 size=(300, 200),
                                                                                 pad=(15, 15))]])],
                                                          [sg.Text('Построить график с '),
                                                           sg.Text('13.10.2017'),
                                                           sg.Text('{}'.format(data_norm[0]), key='-TEXT1-')],
                                                          [sg.Button('Выбрать дату и время начала', key='time1')],
                                                          [sg.Text('Построить график до '),
                                                           sg.Text('13.10.2017'),
                                                           sg.Text(data_norm[len(data_norm) - 1], key='-TEXT2-')],
                                                          [sg.Button('Выбрать дату и время окончания',
                                                                     key='time2')],
                                                          [sg.Button('Построить график', key='graph2')]])]])]
                            ])]]

    return layout


def show_window(data, data_frame, data_norm):
    layout = create_layout(data, data_norm)
    fig1 = draw_graph(6, 4, data_frame)
    fig2 = draw_graph(3, 8, data_frame)

    window = sg.Window('Лабораторная работа №1', layout, element_justification='c', finalize=True)

    # Устанавливаем положение окна
    window.move(300, 150)

    figure_canvas_agg1 = FigureCanvasTkAgg(fig1, window['-CANVAS1-'].TKCanvas)
    figure_canvas_agg1.draw()
    figure_canvas_agg1.get_tk_widget().pack(side='top', fill='both',
                                            expand=1)
    figure_canvas_agg2 = FigureCanvasTkAgg(fig2, window['-CANVAS2-'].TKCanvas)
    figure_canvas_agg2.draw()
    figure_canvas_agg2.get_tk_widget().pack(side='top', fill='both',
                                            expand=1)


    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        # elif event == 'graph1':
        # elif event == 'graph2':
        elif event == 'time1':
            select_elem = create_window_choice(data_norm)
            text = ''
            text += ' ' + str(select_elem)
            window['-TEXT1-'].update(text)
        elif event == 'time2':
            select_elem = create_window_choice(data_norm)
            text = ''
            text += ' ' + str(select_elem)
            window['-TEXT2-'].update(text)


data_frame, data = read_file()
data_norm = conversion_to_normal_view(data_frame)
show_window(data, data_frame, data_norm)

# a = data_frame[data_frame[3] == 180832].index[0]
# print(data_frame[a::][3])

# [sg.Combo(options, default_value=options[0], key="-OPTION-", size=(20, 1))],
