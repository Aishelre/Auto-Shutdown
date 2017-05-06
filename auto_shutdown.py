#python 3.6
"""
windows auto shutdown program using tkinter
this program is only for WINDOWS
"""

import tkinter
from tkinter import ttk
from tkinter import messagebox
import datetime
import os

class AutoShutdown():
    def __init__(self, rt):
        # master
        self.root = rt
        # top level frames
        self.setting_frame = ttk.LabelFrame(self.root, text="자동 종료 프로그램 설정", height=100)
        self.menu_frame = ttk.LabelFrame(self.root, text ="메뉴", height = 100)
        # low level frames
        self.frame0 = tkinter.Frame(self.setting_frame)
        self.sp = tkinter.ttk.Separator(self.setting_frame, orient="horizontal")
        self.frame1_1 = tkinter.Frame(self.setting_frame)
        self.frame1_2 = tkinter.Frame(self.setting_frame)
        self.frame2_1 = tkinter.Frame(self.setting_frame)
        self.frame2_2 = tkinter.Frame(self.setting_frame)

        self.clicked = False # Clicked, Timer runs.
        self.alert_c = 0 # timer is less than 1 min, pop up alert message.

        self.timer_temp = tkinter.IntVar() # seconds
        self.timer_h = tkinter.IntVar()
        self.timer_m = tkinter.IntVar()
        self.timer_s = tkinter.IntVar()

        self.setup_frame()
        self.setup_widget()
        self.timer() # decrease timer, alert
        # End of __init__

    def setup_frame(self):
        # pack top level
        self.setting_frame.pack(fill='both', padx = 10, pady = 10)
        self.menu_frame.pack(fill='both', padx=10, pady=10)
        # pack low level
        self.frame0.pack()
        self.sp.pack(fill='both')
        self.frame1_1.pack()
        self.frame1_2.pack()
        self.frame2_1.pack()
        self.frame2_2.pack()

    def setup_widget(self):
        # initialization
        self.shutdown_menu = tkinter.IntVar() # 1 : power off, 2 : restart
        self.shutdown_menu.set(1)
        self.check_start = tkinter.Checkbutton(self.frame0, variable=self.shutdown_menu, onvalue=1, offvalue=2, text="종료")
        self.check_restart = tkinter.Checkbutton(self.frame0, variable=self.shutdown_menu, onvalue=2, text="재부팅                                                  ")

        self.timer_menu = tkinter.IntVar() # 1 : set timer, 2 : by that time
        self.timer_menu.set(1)
        self.check_1 = tkinter.Checkbutton(self.frame1_1, variable=self.timer_menu, onvalue=1, offvalue=2, text="지정한 시간 경과 후에 종료                                   ")
        self.check_2 = tkinter.Checkbutton(self.frame2_1, variable=self.timer_menu, onvalue=2, text="지정한 시각에 종료                                              ")

        self.hour_val_1 = tkinter.IntVar()
        self.min_val_1 = tkinter.IntVar()
        self.box1_hour = tkinter.ttk.Combobox(self.frame1_2, textvariable=self.hour_val_1, width = 2)
        self.box1_min = tkinter.ttk.Combobox(self.frame1_2, textvariable=self.min_val_1, width = 2)
        self.box1_hour['value'] = tuple(range(0,24))
        self.box1_min['value'] = tuple(range(0,60))
        self.lb1_hour = tkinter.Label(self.frame1_2, text="시간 ")
        self.lb1_min = tkinter.Label(self.frame1_2, text="분 후에 윈도우를 종료합니다.")
        self.box1_hour.current(1) # Combobox에 표시될 default 값의 인덱스를 설정

        self.hour_val_2 = tkinter.IntVar()
        self.min_val_2 = tkinter.IntVar()
        self.box2_hour = tkinter.ttk.Combobox(self.frame2_2, textvariable=self.hour_val_2, width = 2)
        self.box2_min = tkinter.ttk.Combobox(self.frame2_2, textvariable=self.min_val_2, width = 2)
        self.box2_hour['value'] = tuple(range(0,24))
        self.box2_min['value'] = tuple(range(0,60))
        self.lb2_hour = tkinter.Label(self.frame2_2, text="  시  ")
        self.lb2_min = tkinter.Label(self.frame2_2, text="분에 윈도우를 종료합니다.    ")


        self.lb_timer_1 = tkinter.Label(self.menu_frame, textvariable = self.timer_h, foreground ='red', width = 2)
        self.lb_timer_2 = tkinter.Label(self.menu_frame, textvariable = self.timer_m, foreground ='red', width = 2)
        self.lb_timer_3 = tkinter.Label(self.menu_frame, textvariable = self.timer_s, foreground ='red', width = 2)
        self.lb_info_timer_1 = tkinter.Label(self.menu_frame, text ="시간", foreground = 'red')
        self.lb_info_timer_2 = tkinter.Label(self.menu_frame, text ="분", foreground = 'red')
        self.lb_info_timer_3 = tkinter.Label(self.menu_frame, text ="초 남음", foreground = 'red')

        self.btn_start = tkinter.Button(self.menu_frame, text="타이머 시작")
        self.btn_start.bind('<Button-1>', self.start_wrapper())
        self.btn_restart = tkinter.Button(self.menu_frame, text="재시작")
        self.btn_restart.bind('<Button-1>', self.restart_wrapper())
        self.btn_stop = tkinter.Button(self.menu_frame, text="정지")
        self.btn_stop.bind('<Button-1>', self.stop_wrapper())
        self.btn_close = tkinter.Button(self.menu_frame, text="닫기", command=self.root.destroy)

        # grid all widgets
        self.check_start.grid(row=0, column=0, sticky='w')
        self.check_restart.grid(row=0, column=1, sticky='w')

        self.check_1.grid(row=0, column=0, sticky='w')
        self.check_2.grid(row=0, column=0, sticky='w')

        self.box1_hour.grid(row=1, column=0)
        self.box1_min.grid(row=1, column=2)
        self.lb1_hour.grid(row=1, column=1)
        self.lb1_min.grid(row=1, column=3)

        self.box2_hour.grid(row=1, column=4)
        self.box2_min.grid(row=1, column=6)
        self.lb2_hour.grid(row=1, column=5)
        self.lb2_min.grid(row=1, column=7)

        self.btn_start.grid(row=1, column=0, padx=10, pady=2, sticky = 'we', ipadx=8)
        self.btn_restart.grid(row=2, column=0, padx=10, pady=2, sticky = 'we', ipadx=14)
        self.btn_stop.grid(row=1, column=8, padx=10, pady=2, ipadx=14, sticky = 'we')
        self.btn_close.grid(row=2, column=8, padx=10, pady=2, ipadx=14, sticky = 'we')

        self.lb_timer_1.grid(row=1, column=2)
        self.lb_info_timer_1.grid(row=1, column=3)
        self.lb_timer_2.grid(row=1, column = 4)
        self.lb_info_timer_2.grid(row=1, column=5)
        self.lb_timer_3.grid(row=1, column=6)
        self.lb_info_timer_3.grid(row=1, column=7)

    def timer(self):
        if self.clicked:
            self.timer_temp.set(self.timer_temp.get() - 1) # decrease by 1s
            # for displaying remaining time
            self.timer_h.set(self.timer_temp.get() // 3600)
            self.timer_m.set((self.timer_temp.get() - self.timer_h.get() * 3600) // 60)
            self.timer_s.set(self.timer_temp.get() % 60)
        #if remaining minute is less than 1 min, alert.
        if self.timer_m.get() < 1 and self.alert_c == 0 and self.clicked:
            self.alert_c = 1
            tkinter.messagebox.showwarning("경고", "1분 후 컴퓨터를 종료합니다.")
        self.menu_frame.after(1000, self.timer)

    def start_wrapper(self):
        return lambda e : self.start()
    def restart_wrapper(self):
        return lambda e : self.restart()
    def stop_wrapper(self):
        return lambda e : self.stop()

    def rearrange_timer_temp(self):
        if self.now.hour > self.hour_val_2.get():
            self.timer_temp.set(self.timer_temp.get() + 3600 * 24) # 24h
        elif self.now.hour == self.hour_val_2.get() and self.now.minute > self.min_val_2.get():
            self.timer_temp.set(self.timer_temp.get() + 3600 * 24) # 24h

    def start(self):
        if self.timer_menu.get() == 1: # set timer
            self.clicked = True
            self.timer_temp.set(self.hour_val_1.get() * 60 * 60 + self.min_val_1.get() * 60) # set timer as second
        elif self.timer_menu.get() == 2: # by that time
            self.clicked = True
            self.now = datetime.datetime.now()
            self.timer_temp.set((self.hour_val_2.get() - self.now.hour) * 3600 + (self.min_val_2.get() - self.now.minute) * 60)
            self.rearrange_timer_temp() #
        self.set_timer()

    def restart(self):
        if self.clicked == False:
            self.clicked = True
            self.set_timer()

    def stop(self):
        self.alert_c = 0
        self.clicked = False

    def set_timer(self):
        if self.clicked == True and self.timer_temp.get() <= 0: # when Timeout
            if self.shutdown_menu.get() == 1: # power off
                os.system("shutdown -s -t 0")
            elif self.shutdown_menu.get() == 2: # restart
                os.system("shutdown -r")
        elif self.clicked == True:
            self.menu_frame.after(1000, self.set_timer)
        else:
            return


def main():
    root = tkinter.Tk()
    root.title("Auto Shutdown")
    root.geometry("375x260")
    p = AutoShutdown(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# error 1116 : 진행 중인 시스템 종료가 없으므로 시스템 종료를 취소할 수 없습니다.
# error 1190 : 시스템 종료가 이미 예약되어 있습니다.

