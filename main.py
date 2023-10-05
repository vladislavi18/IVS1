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

#
# def draw_graph(xi, yi, date_frame):
#     fig, ax = plt.subplots()
#     ax.plot(date_frame[xi], date_frame[yi], color='red', linestyle='-',
#             label='График {} от {}'.format(header_list_rus[xi - 1],
#                                            header_list_rus[yi - 1]))
#     ax.set_xlabel(header_list_rus[xi - 1])
#     ax.set_ylabel(header_list_rus[yi - 1])
#
#     disconnect_zoom = zoom_factory(ax)
#     pan_handler = panhandler(fig)
#
#     return fig
#
#
# def create_layout(data):
#     table = [
#         [sg.Text('Содержимое файла: ')],
#         [sg.Table(values=data,
#                   headings=header_list,
#                   font='Helvetica',
#                   pad=(25, 25),
#                   display_row_numbers=True,
#                   def_col_width=20,
#                   num_rows=25)]
#     ]
#
#     layout = [[sg.TabGroup([[sg.Tab('Таблица', [[sg.Column(table, element_justification='c')],
#                                                 [sg.Button('Закрыть')]])],
#
#                             [sg.Tab('График', [[sg.Frame('График зависимости Широты от Долготы',
#                                                          [[sg.Canvas(key='-CANVAS1-',
#                                                                      size=(300, 200),
#                                                                      pad=(15, 15))],
#                                                           [sg.Button('Построить график')]]),
#
#                                                 sg.Frame('График зависимости Скорости от времени',
#                                                          [[sg.Canvas(key='-CANVAS2-',
#                                                                      size=(300, 200),
#                                                                      pad=(15, 15))],
#                                                           [sg.Button('Построить график')]])]])]
#                             ])]]
#     return layout
#
#
# def show_window(data, data_frame):
#     layout = create_layout(data)
#     fig1 = draw_graph(6, 4, data_frame)
#     fig2 = draw_graph(3, 8, data_frame)
#
#     window = sg.Window('Лабораторная работа №1', layout, element_justification='c', finalize=True)
#
#     # Устанавливаем положение окна
#     window.move(300, 150)
#
#     figure_canvas_agg1 = FigureCanvasTkAgg(fig1, window['-CANVAS1-'].TKCanvas)
#     figure_canvas_agg1.draw()
#     figure_canvas_agg1.get_tk_widget().pack(side='top', fill='both',
#                                             expand=1)
#     figure_canvas_agg2 = FigureCanvasTkAgg(fig2, window['-CANVAS2-'].TKCanvas)
#     figure_canvas_agg2.draw()
#     figure_canvas_agg2.get_tk_widget().pack(side='top', fill='both',
#                                             expand=1)
#
#     while True:
#         event, values = window.read()
#         if event == sg.WIN_CLOSED or event == "Exit":
#             break
#         elif event == "Построить график":
#             draw_graph(4, 6, data_frame)
#
#
data_frame, data = read_file()
# show_window(data, data_frame)

a = data_frame[data_frame[3] == 180832].index[0]
print(data_frame[a::][3])

# [sg.Combo(options, default_value=options[0], key="-OPTION-", size=(20, 1))],

# import PySimpleGUI as sg

# Основное окно
# layout = [
#     [sg.Button('Выбрать элемент')],
#     [sg.Button('Выход')]
# ]
#
# window = sg.Window('Основное окно', layout)
#
# while True:
#     event, values = window.read()
#
#     if event == sg.WIN_CLOSED:
#         break
#     elif event == 'Выбрать элемент':
#         # Создаем окно для выбора элемента
#         layout_select = [
#             [sg.Text('Выберите элемент:')],
#             [sg.Listbox(data_frame[3], size=(20, 4), key='-LISTBOX-')],
#             [sg.Button('Выбрать', key='-SELECT-')],
#         ]
#
#         window_select = sg.Window('Выбор элемента', layout_select)
#
#         while True:
#             event_select, values_select = window_select.read()
#
#             if event_select == sg.WIN_CLOSED:
#                 break
#             elif event_select == '-SELECT-':
#                 selected_item = values_select['-LISTBOX-'][0] if values_select['-LISTBOX-'] else None
#                 if selected_item:
#                     sg.popup(f'Выбран элемент: {selected_item}')
#                 break
#
#         window_select.close()
#
# window.close()





