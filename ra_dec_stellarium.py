#!/usr/bin/env python3

import PySimpleGUI as sg
import requests
import math

url = 'http://localhost:8090/api/main/view'

#Example output from current Stellarium position
#http://localhost:8090/api/main/view
#https://stellarium.org/doc/0.20/remoteControlApi.html#rcStelActionServicePOST

sg.theme('DarkRed1')


font1 = ("Arial, 16")
font0 = ("Arial, 8")


layout = [
    [sg.Text('RA HH:', size=(6, 1),font=font1), sg.InputText('',font=font1, size=(2,1), key='RA_HH', enable_events=True)],
    [sg.Text('RA MM:', size=(6, 1),font=font1), sg.InputText('',font=font1, size=(2,1), key='RA_MM', enable_events=True)],
    [sg.Text('RA SS:',size=(6, 1),font=font1), sg.InputText('',font=font1, size=(2,1), key='RA_SS', enable_events=True)],
    [sg.Text('DEC:',   size=(6, 1),font=font1), sg.InputText('',font=font1, size=(6,1), key='DEC', enable_events=True)],
    [sg.Button('Set view',font=font1, button_color=('white', 'DarkRed'), key='Submit')],
    [sg.Text('',  key='Respons', size=(17, 5),font=font0)],
]

window = sg.Window("RA/DEC Set", 
                        layout, 
                        default_element_size=(14,1), 
                        text_justification='r', 
                       # auto_size_text=False, 
                        keep_on_top = True,
                        auto_size_buttons=False, 
                        default_button_element_size=(14,1), 
                        finalize=True)      
while True:      
        event, values = window.read()      
        print(event)   
        print(len(values['RA_HH']))
        if event == sg.WIN_CLOSED:
            exit(69)
        if event == 'RA_HH' and values['RA_HH'] and values['RA_HH'][-1] not in ('0123456789') or len(values['RA_HH'])>=3:
            window['RA_HH'].update(values['RA_HH'][:-1])
        if event == 'RA_MM' and values['RA_MM'] and values['RA_MM'][-1] not in ('0123456789') or len(values['RA_MM'])>=3:
            window['RA_MM'].update(values['RA_MM'][:-1]) 
        if event == 'RA_SS' and values['RA_SS'] and values['RA_SS'][-1] not in ('0123456789') or len(values['RA_SS'])>=3:
            window['RA_SS'].update(values['RA_SS'][:-1])
        if event == 'DEC' and values['DEC'] and values['DEC'][-1] not in ('0123456789.-'):
            window['DEC'].update(values['DEC'][:-1])     
        if event == 'Submit' and values['RA_HH'] != "" and values['RA_MM'] != "" and values['RA_SS'] != None and values['DEC'] != "":   
            RA_h = values['RA_HH']
            RA_m = values['RA_MM']
            RA_ss = values['RA_SS']
            DEC_degree = values['DEC']
            #Calculate HHMMSS to Degree
            RA_degree = 15*(int(RA_h)+(1/60)*int(RA_m)+(1/3600)*int(RA_ss))
            #Stellarium needs radians
            RA = math.radians(float(RA_degree))
            DEC = math.radians(float(DEC_degree))
            x =	math.cos(DEC)*math.cos(RA)
            y = math.cos(DEC)*math.sin(RA)
            z = math.sin(DEC)
            j2000 = "j2000=["+ str(x) + "," + str(y) + ","+ str(z)+"]"
            try:
                stellarium_post = requests.post(url, data = j2000)
                window['Respons'].update(stellarium_post)
            except requests.exceptions.RequestException as error:
	            window['Respons'].update(error)
