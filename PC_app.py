
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk as ttk
import math
import serial
import time
import string
import matplotlib
from sympy.plotting.pygletplot import plot_window
from _codecs import decode
from time import sleep
from future.backports.test.pystone import TRUE


matplotlib.use("tkAgg")

import matplotlib.pyplot as plt
import numpy as np
import keyboard
import sys
import glob


# take the data



def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


# find total number of rows and
# columns in list



class Window(tk.Frame):
    def __init__(self,*args,**kwargs):

        tk.Frame.__init__(self, *args, **kwargs)
        
        self.canvas1 = tk.Canvas(root, width=600, height=500, bg='lightsteelblue')
    
        # self.Mode_Rot = tk.Button(self.canvas1, text='Mode rotation: 0', command=self.rotation_change_fcn, bg='white', fg='black',
        #                                 font=('helvetica', 12, 'bold'))
        # self.disp_data = tk.Button(self.canvas1, text='Display graph from measured data', command=self.show_graph, bg='white', fg='black',
        #                                 font=('helvetica', 12, 'bold'))
        self.run_button = tk.Button(self.canvas1, text='Run', command=self.run, bg='white', fg='black',
                                        font=('helvetica', 12, 'bold'))
        self.upd_btn = tk.Button(self.canvas1, text='Update data', command=self.send_data, bg='white', fg='black',
                                        font=('helvetica', 12, 'bold'))
        # self.mode_button = tk.Label(self.canvas1,text='B = 0,000 T', width=500,  height=3, bg='white',fg='black', font=('helvetica',20,'bold'))
        self.clicked = tk.StringVar()
        self.clicked2 = tk.StringVar()

        self.send_msg_btn = tk.Button(self.canvas1, text='Send one msg', command=self.send_one_msg, bg='white', fg='black',
                                         font=('helvetica', 12, 'bold'))
        self.send_repeat_msg_btn = tk.Button(self.canvas1, text='Send repeating msg', command=self.send_repeat_msg, bg='white', fg='black',
                                         font=('helvetica', 12, 'bold'))
        self.send_stop_msg_btn = tk.Button(self.canvas1, text='Turn off msg', command=self.send_turn_off_msg, bg='white', fg='black',
                                         font=('helvetica', 12, 'bold'))
        self.stop_button = tk.Button(self.canvas1, text='Stop', command=self.fast_mode_fcn, bg='white', fg='black',
                                        font=('helvetica', 12, 'bold'))
        self.silen_button = tk.Button(self.canvas1, text='Normal mode', command=self.silent_mode, bg='white', fg='black',
                                        font=('helvetica', 12, 'bold'))
        self.log_btn = tk.Button(self.canvas1, text='Log is OFF', command=self.make_log_file, bg='white', fg='black',
                                        font=('helvetica', 12, 'bold'))
    
        # self.my_column = tk.Entry(self.canvas1,text = "IDE")

# initial menu text
        self.names = ["IDE", "Size","D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]
        self.name_box = []
        for i in range(10):
             self.name_box.append(tk.Entry(self.canvas1))
             self.name_box[i].grid(row = 1, column = i)

        self.table =  ttk.Treeview(self.canvas1,column=("IDE", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"), show='headings', height=5)
        self.canvas1.create_window(300,400,window=self.table,width = 550,height = 175)
        self.canvas1.create_window(100,275,window=self.upd_btn)
        for i in range(10):
            self.canvas1.create_window(50*i+75,200,window=tk.Label(self.canvas1,text = self.names[i],bg='lightsteelblue', fg='black',font=('helvetica', 10)),width = 40)
            self.canvas1.create_window(50*i+75,220,window=self.name_box[i],width = 40)
        self.table.column("# 1", anchor=tk.CENTER,width = 50)
        self.table.heading("# 1", text="IDE")
        self.table.column("# 2", anchor=tk.CENTER,width = 50)
        self.table.heading("# 2", text="D1")
        self.table.column("# 3", anchor=tk.CENTER,width = 50)
        self.table.heading("# 3", text="D2")
        self.table.column("# 4", anchor=tk.CENTER,width = 50)
        self.table.heading("# 4", text="D3")
        self.table.column("# 5", anchor=tk.CENTER,width = 50)
        self.table.heading("# 5", text="D4")
        self.table.column("# 6", anchor=tk.CENTER,width = 50)
        self.table.heading("# 6", text="D5")
        self.table.column("# 7", anchor=tk.CENTER,width = 50)
        self.table.heading("# 7", text="D6")
        self.table.column("# 8", anchor=tk.CENTER,width = 50)
        self.table.heading("# 8", text="D7")
        self.table.column("# 9", anchor=tk.CENTER,width = 50)
        self.table.heading("# 9", text="D8")





        self.clicked.set( "Choose port:" )
        self.clicked2.set( "Choose speed in Baud:" )
        # self.text = tk.Text(self.canvas1,width=50, height=10)
        # print(serial_ports())
        self.opt_menu = tk.OptionMenu(self.canvas1,self.clicked,*serial_ports() )
        self.opt_menu2 = tk.OptionMenu(self.canvas1,self.clicked2,u'125kBaud',u'250kBaud',u'500kBaud',u'1000kBaud' )
        self.df1 = None
        self.df2 = None
        self.canvas1.pack() 
        self.canvas1.create_window(110, 150,window=self.send_msg_btn)
        self.canvas1.create_window(475,150,window=self.send_repeat_msg_btn)
        self.canvas1.create_window(300,150,window=self.silen_button)
        self.canvas1.create_window(500,275,window=self.send_stop_msg_btn)
        self.canvas1.create_window(70,75,window=self.run_button)
        self.canvas1.create_window(230,75,window=self.log_btn)
        self.canvas1.create_window(350,75,window=self.opt_menu)
        self.canvas1.create_window(500,75,window=self.opt_menu2)
        self.canvas1.create_window(130,75,window=self.stop_button)
        self.textid1 = self.canvas1.create_text(300, 275, text='',font=('helvetica',12,'bold'))
        # self.canvas1.create_window(250,250,window=self.text)
        self.checking = 0
        self.import_file_path1 = None
        self.import_file_path2 = None
        self.fast_mode = True
        self.x = 0
        self.out_rec =None
        self.fill_rec =None
        self.turn_off_mes = True
        self.one_msg = False
        self.repeat_msg = False
        self.stop_msg = False
        self.running_program = False
        self.silent_on = False
        self.silent = 'n'
        self.send_mydata = False
        self.mydata = ""
        self.make_log = False
        # code for creating table
        
    def rotation_change_fcn(self):
        self.x += 1
        self.checking = 1
        if self.x > 1:
            self.x = 0
        txt_string = "Mode rotation: "+str(self.x)
        self.Mode_Rot.config(text=txt_string)
    # def write_new_data_Frame(self):    
    def send_message(self,text):
        if "Choose" in  self.clicked.get():
                self.canvas1.itemconfig(self.textid1, text = "You did not select the port" )
                return
            
        self.canvas1.itemconfig(self.textid1, text = "" )
        ser = serial.Serial(self.clicked.get())
        ser.flushInput()
        for i in text:
            ser.write(i.encode('utf-8'))
        ser.close()
    
        
    def send_one_msg(self):
        if not self.running_program:
            self.send_message('i')
        else:
            self.one_msg = True
    
    def send_repeat_msg(self):
        if not self.running_program:
            self.send_message('r')
        else:
            self.repeat_msg = True
    
    def make_log_file(self):
        self.make_log = not(self.make_log) 
        if self.make_log:
            self.log_btn.config( text="Log is ON")
        else:
            self.log_btn.config( text="Log is OFF")    
        
    def send_turn_off_msg(self):
        if not self.running_program:
            self.send_message('r')
        else:
            self.stop_msg = True

    def send_data(self):
        txt = "d"
        for i in range(int(self.name_box[1].get())+2):
            txt += str(self.name_box[i].get())
            txt +="-"
        if not self.running_program:
            self.send_message(txt)
        else:
            self.send_mydata = True
            self.mydata = txt
            # print(txt)
    def fast_mode_fcn(self):
        self.turn_off_mes= False

    def silent_mode(self):
        if 's' in self.silent:
            self.silent = 'n'
            self.silen_button.config( text="Normal mode")
        else:
            self.silent = 's'
            self.silen_button.config( text="Silent mode")
        if not self.running_program:
            self.send_message(self.silent)
        else:
            self.silent_on= True
            
            
    def run(self):
        self.running_program = True
        if self.make_log:
            f = open("result.txt", "w")
        if "Choose" in  self.clicked.get():
            self.canvas1.itemconfig(self.textid1, text = "You did not select the port" )
            return
        
        self.canvas1.itemconfig(self.textid1, text = "" )
        ser = serial.Serial(self.clicked.get())
        ser.flushInput()
        decode_string =""
        number = ""
        record_number = 0
        baud_dict = {'125kBaud':'3','250kBaud':'2','500kBaud':'1','1000kBaud':'0'}
        my_dict = {}
        x = 0
        if "Choose" in  self.clicked2.get():
            self.canvas1.itemconfig(self.textid1, text = "You did not select the bautrate" )
            return
        # print(baud_dict[self.clicked2.get()])
        ser.write(baud_dict[self.clicked2.get()].encode('utf-8'))
        while self.turn_off_mes:
            if self.one_msg:
                ser.write(x.encode('utf-8'))
                self.one_msg = False
            if self.repeat_msg:
                x = 'r'
                ser.write('r'.encode('utf-8'))
                self.repeat_msg = False
            if self.stop_msg:
                x = 'i'
                ser.write('i'.encode('utf-8'))
                self.stop_msg = False
            if self.silent_on:
                ser.write(self.silent.encode('utf-8'))
                self.silent_on = False
            if self.send_mydata:
                for i in self.mydata:
                    ser.write(i.encode('utf-8'))
                self.send_mydata = False
           
                
            try:
        
                ser_bytes = ser.readline()
                try:
                    decode_bts =  ser_bytes.decode("utf-8")
                    if self.make_log:
                        f.write(decode_bts+"\n")
                        f.flush()
                    # if "mT" in decode_bts:
                    #     self.mode_button.config(text = decode_bts[:-1])
                    #     decode_string = decode_bts.split("=")
                    #     decode_string = decode_string[1].split("mT")
                    #     number = decode_string[0]
                    #     decode_bts= float(number)
                    #
                    #
                    # elif "T" in decode_bts:
                    #     self.mode_button.config(text = decode_bts[:-1])
                    #     decode_string = decode_bts.split("=")
                    #     decode_string = decode_string[1].split("T")
                    #     number = decode_string[0]
                    #     decode_bts = float(number)*1000
                    if  "Ide" in decode_bts:
                        sec  = decode_bts.replace("Ide: ","")
                        if "\n" in sec:
                            sec = sec.replace("\n","")
                        if "\r" in sec:
                            sec = sec.replace("\r","")
                        
                        sec  = sec.replace("D:","")
                        
                        sec  =  sec.split(",")
                        if len(sec) < 9:
                            for i in range(len(sec),9):
                                sec.append("") 
                        # print(sec)
                        if sec[0] in my_dict.keys():
                            self.table.item(my_dict[sec[0]], values =( sec[0],sec[1],sec[2],sec[3],sec[4],sec[5],sec[6],sec[7],sec[8]))
                            # print(decode_bts)
                            
                        else:  
                            s = self.table.insert("", record_number, values = (sec[0],sec[1],sec[2],sec[3],sec[4],sec[5],sec[6],sec[7],sec[8]))
                            my_dict[ sec[0]] = s
                            record_number += 1
                            # print(decode_bts + "else" +s)
                    # print(decode_bts)
                    
                    self.canvas1.update()
                    

                except:
                    # print("my house")
                    continue

            except:
                print("Keyboard Interrupt")
                break
        
            if keyboard.is_pressed("q"):
                break
          
         
        
        ser.close()     
        if self.make_log:   
            f.close()
        self.turn_off_mes= True
        self.running_program = False

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CAN Analyzer")
    view = Window(root)
    view.pack()
    root.mainloop()
 