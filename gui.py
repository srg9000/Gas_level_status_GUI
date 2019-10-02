# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 18:50:46 2018

@author: srg
"""

import tkinter as tk
from sqlite3.dbapi2 import Cursor
from tkinter import ttk
import sqlite3 as sql
from datetime import datetime
from datetime import time as tm
# import insert
import matplotlib
import matplotlib.animation as animation
from matplotlib import style
import threading
import random
import time
# import wx.lib.wxcairo
# import cairo

style.use("seaborn-paper")
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

f = Figure(figsize=(10, 10), dpi=100)
a = f.add_subplot(111)


class guit(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, "icon.ico")
        tk.Tk.wm_title(self, "Gas Sensing GUI")
        container = tk.Frame(self)

        container.pack(side="left", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.geometry("400x300")
        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Start Page", font=("Helvetica", 12))
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Live graph", command=lambda: controller.show_frame(PageOne))
        button1.pack()

        cg.execute("select lpg_safe from lpg where numbers=(select max(numbers) from lpg)")
        xx=cg.fetchone()
        if(xx[0]=="yes"):
            xy="Safe"
        else:
            xy="unsafe"
        self.s_status ="Current status is: "+ xy

        label = ttk.Label(self, text=self.s_status, font=("Helvetica", 20))
        label.pack(pady=10,padx=10)

        def clicked():
            cg.execute("select lpg_safe from lpg where numbers=(select max(numbers) from lpg)")
            xx = cg.fetchone()
            if (xx[0] == "yes"):
                xy = "Safe"
            else:
                xy = "unsafe"
            self.s_status = "Current status is: " + xy
            label.configure(text=self.s_status, font=("Helvetica", 20))

        button2 = ttk.Button(self, text="Refresh Status", command=clicked)
        button2.pack()



class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One", font=("Helvetica", 12))
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Go back", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # graph_data()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def graph_data(i):
    l_dates = []
    l_ppm = []
    cg.execute("SELECT dates,time,lpg_ppm from lpg natural join time")
    for row in cg.fetchall()[-60::]:
        #        print(row)
        string = str(row[0]) + "-" + str(row[1])
        l_dates.append(datetime.strptime(string, '%Y-%m-%d-%H:%M:%S'))
        if row[2] != None:
            l_ppm.append(row[2])
        else:
            l_ppm.append(0)
    a.clear()
    a.plot(l_dates, l_ppm, '-')
    a.plot(l_dates, l_ppm, 'o')


class D_enter(object):

    def __init__(self):
        insThread = threading.Thread(target=self.enter)
        insThread.daemon = True
        insThread.start()


    def connect(self):
        self.conn = sql.connect("Team31.db")
        self.c = self.conn.cursor()

    def enter(self):
        self.connect()
        self.c.execute("SELECT max(numbers) from time ")
        x = self.c.fetchone()
        # print(x[0])
        numbers = x[0]
        numbers += 1
        for _ in range(1000):
            # self.d_entry()
            # numbers += 1
            # self.conn.commit()

            self.c.execute("select meth_ppm,meth_safe from methane where numbers=(select max(numbers) from methane)")
            meth_prev = self.c.fetchone()
            self.c.execute("select butane_ppm,but_safe from butane where numbers=(select max(numbers) from methane)")
            but_prev = self.c.fetchone()
            self.c.execute("select lpg_ppm,lpg_safe from lpg where numbers=(select max(numbers) from methane)")
            lpg_prev = self.c.fetchone()
            self.c.execute("select smoke_ppm,smoke_safe from smoke where numbers=(select max(numbers) from methane)")
            smoke_prev = self.c.fetchone()

            l = datetime.now()
            date = "-".join([str(l.year), str(l.month), str(l.day)])
            times = ":".join([str(l.hour), str(l.minute), str(l.second)])
            self.c.execute(str(("INSERT into time values (" + str(numbers) + ", '" + date + "', '" + times + "')")))

            te = random.randint(50, 100)
            if te > 90:
                tesf = "no"
            else:
                tesf = "yes"
            k = random.randint(1, 30)
            if k / 10 <= 2.2:
                sf = "yes"
            else:
                sf = "no"
            v_err = (random.randint(49, 51) / 10)
            self.c.execute(
                str(("INSERT into temp_read values (" + str(numbers) + "," + str(te) + ", '" + str(tesf) + "' )")))
            #    temp.write(temp_string)
            self.c.execute(str(("INSERT into gas_read values (" + str(numbers) + "," + str(k) + ")")))
            #    gas.write(gas_string)
            self.c.execute(
                str(("INSERT into calculation values (" + str(numbers) + "," + str(k) + ", " + str((5 + v_err) / k)[
                                                                                               :4] + ", " + str(
                    5 + v_err) + ", " + str(k / 10) + ")")))
            #    calc.write(calc_string)
            if numbers % 4 == 0:
                meth_prev = str("," + str(k / 10) + ", '" + str(sf) + "' )")
            elif numbers % 4 == 1:
                but_prev = str("," + str(k / 10) + ", '" + str(sf) + "' )")
            elif numbers % 4 == 2:
                lpg_prev = str("," + str(k / 10) + ", '" + str(sf) + "' )")
            elif numbers % 4 == 3:
                smoke_prev = str("," + str(k / 10) + ", '" + str(sf) + "' )")

            self.c.execute(str("INSERT into Methane values (" + str(numbers) + "," + str(meth_prev)[1:-1] + ")"))
            self.c.execute(str("INSERT into butane values (" + str(numbers) + "," + str(but_prev)[1:-1] + ")"))
            self.c.execute(str("INSERT into LPG values (" + str(numbers) + "," + str(lpg_prev)[1:-1] + ")"))
            self.c.execute(str("INSERT into smoke values (" + str(numbers) + "," + str(smoke_prev)[1:-1] + ")"))
            if (tesf == "no" or sf == "no"):
                self.c.execute(str(("INSERT into analysis values (" + str(numbers) + ", 'unsafe' )")))
            else:
                self.c.execute(str(("INSERT into analysis values (" + str(numbers) + ", 'safe' )")))
            time.sleep(5)

            numbers += 1
            self.conn.commit()


#    def d_entry(self):


conn2 = sql.connect("Team31.db")
cg = conn2.cursor()
app = guit()

ins = D_enter()
ani = animation.FuncAnimation(f, graph_data, interval=1000)

app.mainloop()
# conn.commit()
cg.close()
conn2.close()
