#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sampling temperature data from BMP180 sensor connected to an arduino board

 
Created on Thu Feb  4 17:34:38 2021

@author: erickmfs
"""
import serial
import time
import json
import csv
import os
from datetime import datetime
import numpy as np


csvfilepath = r'C:\Users\hjara\OneDrive\IA apps\xubuntu\ai_apps\projects\smart_sensor\FW\sampler_fw_v1'

dt = 1 #sampling time
sampling_time = 2
sample_max_num = 2
cou = 0 #counter
temp = []
pres = []

def command_addressing(command):     
    # Get the function from switcher dictionary
    print("running switcher to get proper sampler function")
    func = switcher.get(command, "nothing")
    # Execute the function
    return func()

def strt_com(COM):
    print("Starting communication")
    smplr_ser = serial.Serial(COM, 9600)
    smplr_ser.reset_input_buffer()
    return smplr_ser

def com_test():
    print("sending confirmation message to sampler hw")
    smplr_ser.write(('c' +'\r'+'\n').encode('utf-8'))
    er = 0
    c = 0
    
    while(smplr_ser.in_waiting < 0): 
        if c < 20:
            print(".")
            time.sleep(0.2)
        else:
            er = 1
            break
        c += 1
        
    #Read response from sampler hw
    chr_msg = smplr_ser.readline().strip().decode('ascii')
    print(chr_msg)
    if er == 1:
        print("communication test: FAILED - HW DISCONNECTED")
        return 0
    else:
        if chr_msg == "c":
            print("communication test: OK")
            return 1
        else:
            print("communication test: FAILED - INNCORRECT CHARACTER")
            return 0

def update_sampling_time(st):
    global sample_max_num, sampling_time
    sampling_time = st
    sample_max_num = sampling_time/dt
    
def reset_values():
    global cou, temp, pres
    temp = []
    pres = []
    cou = 0  
    
def save_temp_values(temp_sampler):
    global temp, pres, cou 
    
    temp.append(temp_sampler["bmp180"]["temp"])
    pres.append(temp_sampler["bmp180"]["pres"])
    cou += 1
    
def create_csv():
    global cou, temp
    print("-----creating csv file with temp values-----")
    
    now = datetime.now()
    dt_str = now.strftime("%d-%m-%Y_%H-%M-%S")
    filename = os.path.join(csvfilepath,dt_str + '_tempdata.csv')

    #getting an array from temp values
    temp = np.array(temp)
    
    
    with open(filename, 'w') as file:
        #writer = csv.writer(file)
        writer = csv.writer(file, delimiter=',')#,quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Temperatura(C)'])
        for c in range(cou):
            writer.writerow([str(temp[c])])
    
    print("-----csv file created-----")
        
def strt_sam():
    global sampling_time, sample_max_num, cou    
    print("Starting sampling process")
    #asking for sampling time and updating    
    p = int(input("                    Insert sampling time: "))
    update_sampling_time(p)
    #sending command to IMU physical device
    smplr_ser.write(('s'+ str(sampling_time) +'\r'+'\n').encode('utf-8'))
    time.sleep(0.5)
    #Start getting samples
    smplr_ser.write(('i'+'\r'+'\n').encode('utf-8'))
    #forever loop
    while True:
        if smplr_ser.in_waiting > 0:
            ser_data = smplr_ser.readline()
            print(ser_data)
            if(cou < sample_max_num):
                j2msg = json.loads(ser_data)
                save_temp_values(j2msg)
        if cou >= sample_max_num:
            create_csv()
            reset_values()
            break
    return 1

def fini_com(smplr_ser):
    print("Closing communication ports")
    smplr_ser.close()
    
    
def basic_IMU_user_interface():
    print("############################################")
    print("############################################")
    print("((((((BMP180-based temperature sampler))))))")
    print("############################################")
    print("############################################")
    print("a - Start getting samples")
    print("b - Communication test")
    print("              ------------------------------")          
    op = input("             Type option and press enter: ")
    return op

    
################LIST OF EVENTS################
switcher = {"a": strt_sam,
            "b": com_test}
##############################################

########## SAMPLER GUI  ################
while True:
    op = basic_IMU_user_interface()
    #Start Serial connection
    smplr_ser = strt_com('COM5')
    result_msg = command_addressing(op)
    print(result_msg)
    #Closing connection so as to avoiding dummy open ports
    fini_com(smplr_ser)
    time.sleep(1)



