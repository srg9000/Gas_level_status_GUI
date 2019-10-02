# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 19:28:35 2018

@author: srg
"""

import sqlite3 as sql
import tkinter as tk
import random
from datetime import datetime
from datetime import time as tm
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
style.use('seaborn-paper')




def d_entry(c):

    c.execute("select meth_ppm,meth_safe from methane where numbers=(select max(numbers) from methane)")
    meth_prev=c.fetchone()
    c.execute("select butane_ppm,but_safe from butane where numbers=(select max(numbers) from methane)")
    but_prev=c.fetchone()
    c.execute("select lpg_ppm,lpg_safe from lpg where numbers=(select max(numbers) from methane)")
    lpg_prev=c.fetchone()
    c.execute("select smoke_ppm,smoke_safe from smoke where numbers=(select max(numbers) from methane)")
    smoke_prev=c.fetchone()
    
    l=datetime.now()
    date="-".join([str(l.year),str(l.month),str(l.day)])
    times=":".join([str(l.hour),str(l.minute),str(l.second)])
    c.execute(str(("INSERT into time values ("+str(numbers)+", '"+ date +"', '"+ times +"')")))

    te=random.randint(50,100)
    if te>90:
        tesf="no"
    else:
        tesf="yes"
    k=random.randint(1,30)
    if k/10<=2.2:
        sf="yes"
    else :
        sf="no"
    v_err=(random.randint(49,51)/10)
    c.execute(str(("INSERT into temp_read values ("+str(numbers)+","+ str(te)+", '"+ str(tesf)+"' )")))
#    temp.write(temp_string)
    c.execute(str(("INSERT into gas_read values ("+str(numbers)+","+ str(k)+")")))
#    gas.write(gas_string)
    c.execute(str(("INSERT into calculation values ("+str(numbers)+","+ str(k)+", "+ str((5+v_err)/k)[:4]+", "+str(5+v_err)+", "+str(k/10)+")")))
#    calc.write(calc_string)
    if numbers%4==0:
        meth_prev=str(","+ str(k/10)+", '"+ str(sf)+"' )")
    elif numbers%4==1:
        but_prev=str(","+ str(k/10)+", '"+ str(sf)+"' )")
    elif numbers%4==2:
        lpg_prev=str(","+ str(k/10)+", '"+ str(sf)+"' )")
    elif numbers%4==3:
        smoke_prev=str(","+ str(k/10)+", '"+ str(sf)+"' )")

    c.execute(str("INSERT into Methane values ("+str(numbers)+","+str(meth_prev)[1:-1] +")"))
    c.execute(str("INSERT into butane values ("+str(numbers)+","+str(but_prev)[1:-1] +")"))
    c.execute(str("INSERT into LPG values ("+str(numbers)+","+str(lpg_prev)[1:-1] +")"))
    c.execute(str("INSERT into smoke values ("+str(numbers)+","+str(smoke_prev)[1:-1] +")"))
    if(tesf=="no" or sf=="no"):
        c.execute(str(("INSERT into analysis values ("+str(numbers)+", 'unsafe' )")))
    else:            
        c.execute(str(("INSERT into analysis values ("+str(numbers)+", 'safe' )")))
    time.sleep(10)

def graph_data():
    l_dates=[]
    l_ppm=[]
    c.execute("SELECT dates,time,lpg_ppm from lpg natural join time")
    for row in c.fetchall()[::4]:
#        print(row)
        string=str(row[0])+"-"+str(row[1])
        l_dates.append(datetime.strptime(string,'%Y-%m-%d-%H:%M:%S'))
        if row[2]!=None:
            l_ppm.append(row[2])
        else:
            l_ppm.append(0)
    plt.plot(l_dates,l_ppm, '-')
    plt.show()



conn =sql.connect("Team31.db")
c= conn.cursor()

c.execute("Select max(numbers) from time ")
x=c.fetchone()
#print(x[0])
numbers=x[0]
numbers+=1
for _ in range(1000):
    d_entry()
    numbers+=1

#graph_data(c)
conn.commit()
c.close()
conn.close()

