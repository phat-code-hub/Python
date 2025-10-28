import PySimpleGUI as sg
import os
import re

def create_form():
    layout = [
        [sg.Text('Filename:'), sg.InputText(key='filename')],
        [sg.Text('Search Folder:'), sg.InputText(key='search_folder'), sg.FolderBrowse('Browse')],
        [sg.Listbox(values=[], size=(40, 10), key='file_list')],
        [sg.Button('Search'), sg.Button('Open'), sg.Button('Rename'), sg.Button('Cancel')]
    ]

    window = sg.Window('File Search and Rename', layout)

    while True:
        event, values = window.read()
        if event == 'Browse':
            folder_path = sg.popup_get_folder('Select Search Folder')
            window['search_folder'].update(folder_path)
        elif event == 'Search':
            filename = values['filename']
            search_folder = values['search_folder']
            file_list = search_files(search_folder, filename)
            window['file_list'].update(file_list)
            window['Open'].update(disabled=len(file_list) == 0)
            window['Rename'].update(disabled=len(file_list) == 0)
        elif event == 'Open':
            selected_file = values['file_list'][0]
            os.startfile(selected_file)
        elif event == 'Rename':
            # invoke Rename Form
            pass
        elif event == 'Cancel' or event == sg.WINDOW_CLOSED:
            break

    window.close()

def search_files(search_folder, filename):
    file_list = []
    for root, dirs, files in os.walk(search_folder):
        for file in files:
            if re.match(filename, file):
                file_list.append(os.path.join(root, file))
    return [os.path.basename(file) for file in file_list]

create_form()