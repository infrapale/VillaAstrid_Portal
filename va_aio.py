"""
'va_aio.py'

"""

import time
class VA_AIO:
    # Villa Astrid Adafruit IO interface
    
    aio_dict = {'Dock_T_Water': {'feed':'villaastrid.water-temp','available': False, 'timeto': 0.0, 'value':0.0},
            'Dock_T_bmp180': {'feed':'villaastrid.dock-temp','available': False, 'timeto': 0.0, 'value':0.0},
            'Dock_P_bmp180': {'feed':'villaastrid.dock-pres','available': False, 'timeto': 0.0, 'value':0.0},
            'Dock_T_dht22': {'feed':'villaastrid.outdoor1-temp-dht22','available': False, 'timeto': 0.0, 'value':0.0},
            'Dock_H_dht22': {'feed':'villaastrid.dock-hum-dht22','available': False, 'timeto': 0.0, 'value':0.0},
            'OD_1_Temp':  {'feed':'villaastrid.outdoor1-temp','available': False, 'timeto': 0.0, 'value':0.0},
            'OD_1_Hum':  {'feed':'villaastrid.outdoor1-hum-dht22','available': False, 'timeto': 0.0, 'value':0.0},
            'OD_1_P_mb':  {'feed':'villaastrid.outdoor1-pmb','available': False, 'timeto': 0.0, 'value':0.0},
            'OD_1_Light1':  {'feed':'villaastrid.outdoor1-ldr1','available': False, 'timeto': 0.0, 'value':0.0},
            'OD_1_Temp2': {'feed':'villaastrid.outdoor1-temp-dht22','available': False, 'timeto': 0.0,  'value':0.0}}

    def __init__(self):

        for key in aio_dict:      
            aio_dict[key]['timeto'] = time.monotonic()
            
    def print_all(self):
        print(aio_dict)
        
