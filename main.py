#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author: Sylleo
Version: 0.0.1
Date: 2022-01-12 08:56:36
LastEditTime: 2022-01-12 15:20:09
LastEditors: Sylleo
Description: An access code generator for RSSHub.
FilePath: /rsshub-access-code-gen/main.py
Environment: Python=3.9.7  PySimpleGUI=4.56.0
Copyright (C) 2022 Sylleo. All rights reserved.
'''

from hashlib import md5
import PySimpleGUI as sg

sg.theme('DarkGreen6')


def main():
    layout = [
        [sg.Text('RSSHub URL', size=(10, 1)), sg.InputText(default_text='https://rsshub.app', key='-URL-', focus=True, size=(65, 1))],
        [sg.Text('Access Key', size=(10, 1)), sg.InputText(key='-KEY-', size=(65, 1))],
        [sg.Text('Route', size=(10, 1)), sg.InputText(key='-ROUTE-', size=(65, 1))],
        [sg.Text('Access Code', size=(10, 1)), sg.Multiline(key='-OUTPUT-', disabled=True, auto_refresh=True, rstrip=True, size=(65, 10))],
        [
            sg.Button('Ok', bind_return_key=True, size=(10, 1), pad=((0, 20), (0, 0))),
            sg.Button('Copy Access Code', button_color='green'),
            sg.Button('Copy Feed URL with Code', button_color='green'),
            sg.Button('Copy Feed URL with Key', button_color='green')
        ]
    ]

    window = sg.Window('RSSHub Access Code Generator', layout=layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        if event == 'Ok':
            url = values['-URL-'] or 'https://rsshub.app'
            key = values['-KEY-']
            route = values['-ROUTE-']

            if not route:
                window['-OUTPUT-'].update('Err: The route is empty!', text_color_for_value='red')
                continue
            
            # Compute access code
            md5encoder = md5()
            md5encoder.update((route + key).encode('utf-8'))
            code = md5encoder.hexdigest()
            # Get feed urls
            feed_url_code = url + route + '?code=' + code
            feed_url_key = url + route + '?key=' + key
            
            window['-OUTPUT-'].update('Access Code:\n')
            window['-OUTPUT-'].update(code, append=True, text_color_for_value='blue')
            window['-OUTPUT-'].update('\nFeed URL with Code:\n', append=True)
            window['-OUTPUT-'].update(feed_url_code, append=True, text_color_for_value='blue')
            window['-OUTPUT-'].update('\nFeed URL with Key:\n', append=True)
            window['-OUTPUT-'].update(feed_url_key, append=True, text_color_for_value='blue')
        if event == 'Copy Access Code':
            output = window['-OUTPUT-'].get().splitlines()

            if output:
                # print(output)
                # code = output[1]
                sg.clipboard_set(output[1])
        if event == 'Copy Feed URL with Code':
            output = window['-OUTPUT-'].get().splitlines()

            if output:
                # print(output)
                # feed_url_code = output[3]
                sg.clipboard_set(output[3])
        if event == 'Copy Feed URL with Key':
            output = window['-OUTPUT-'].get().splitlines()

            if output:
                # print(output)
                # feed_url_key = output[5]
                sg.clipboard_set(output[5])

    window.close()


if __name__ == '__main__':
    main()
