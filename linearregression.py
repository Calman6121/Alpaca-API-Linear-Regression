import json
import threading
import matplotlib
import alpaca_trade_api as tradeapi
import time
import matplotlib.pyplot as plt
import numpy as np
from itertools import count
from matplotlib.animation import FuncAnimation
import tkinter as Tk
from tk import *
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
import websocket
import time
style.use('ggplot')

#assigns all the keys to a varaiable
API_KEY = "*****"
API_SECRET = "*****"
#assigns the link of where to get the data
BASE = "https://paper-api.alpaca.markets"
#comapcts the varification process into a variable 
api = tradeapi.REST(key_id=API_KEY, secret_key=API_SECRET, base_url=BASE, api_version='v2')

#creates all the variables for the linear regression
x1212 = []
y1212 = []
tempx = []
y = []
xy = []
x2 = []
indexY = []
indexX = []
index = count()
index1 = count()
index2 = count()

tempx1 = []
tempy1 = []
tempxy1 = []
tempx21 = []
tempy21 = []
indexY1 = []
indexX1 = []
future = []

#A function that gets the position of the stock price
def again():
    global realprice1
    portfolio = (api.get_position('AAPL'))
    realprice = portfolio.current_price
    realprice1 = np.array(realprice, dtype=np.float32).tolist()
    realprice1 = realprice1

again()
#creates a infinite thread that continuesly updates again()
def threadz1():
    while True:
        x = threading.Thread(target=again)
        x.start()
        time.sleep(1)

t = threading.Thread(target=threadz1)
t.start()

#the function responsible for the real time graph
def animate(i):
    global b
    #appends the price to a list
    y1212.append(round(realprice1, 2))
    #appends the next second to a list
    x1212.append(next(index))
    #plots that on areal time graph
    plt.plot(x1212, y1212, color = "r")
    #gets the psoiton again
    portfolio = (api.get_position('AAPL'))
    price = portfolio.current_price
    #puts the psoiton in an array, bassically a list
    price1 = np.array(price, dtype=np.float32).tolist()
    #appends the price to a list
    indexY.append(round(price1, 2))
    #appends the next second to a list
    indexX.append(len(x1212))
    #checks if the length of x is greater than 3
    if len(indexX) > 3:
        #creates a for loop that runs for the length of x
        for i in range(len(indexY)):
            #does all the linear regression calculations    
            num = len(tempx)
            
            tempx.insert(num, indexX[i])
            x = np.array(tempx,dtype='double')

            y.insert(num, indexY[i])

            xy1 = indexX[i] * indexY[i]
            xy.insert(num, xy1)

            x21 = indexX[i] ** 2
            x2.insert(num, x21)
        #more linear regression calculations 
        n = len(x)
        sumX = sum(x)
        sumY = sum(y)
        sumXY = sum(xy)
        sumX2 = sum(x2)
        meanX = sumX/n
        meanY = sumY/n

        #calculates the y intecept
        b = (round(n*(sumXY), 2)-round(((sumX)*(sumY)), 2))/((n*(sumX2))-((sumX)**2))

        #calculates the gradient
        a = round(meanY - (b*meanX), 2)

        #calculates the position of y
        y212 = a + (b * x)
        #plots all of it on a graph
        plt.plot(x, y212, color = "b")
        #creates another counter
        future.append(next(index2))
#does it all again
def get_b():
        y1212.append(round(realprice1, 2))
        #appends the next second to a list
        x1212.append(next(index))
        #plots that on areal time graph
        #gets the psoiton again
        portfolio = (api.get_position('AAPL'))
        price = portfolio.current_price
        #puts the psoiton in an array, bassically a list
        price1 = np.array(price, dtype=np.float32).tolist()
        #appends the price to a list
        indexY.append(round(price1, 2))
        #appends the next second to a list
        indexX.append(len(x1212)-1)
        #checks if the length of x is greater than 3
        if len(indexX) > 3:
            #creates a for loop that runs for the length of x
            for i in range(len(indexY)):
                #does all the linear regression calculations    
                num = len(tempx)
                
                tempx.insert(num, indexX[i])
                x = np.array(tempx,dtype='double')

                y.insert(num, indexY[i])

                xy1 = indexX[i] * indexY[i]
                xy.insert(num, xy1)

                x21 = indexX[i] ** 2
                x2.insert(num, x21)
            #more linear regression calculations 
            n = len(x)
            sumX = sum(x)
            sumY = sum(y)
            sumXY = sum(xy)
            sumX2 = sum(x2)
        #calculates the gradient
        b = (round(n*(sumXY), 2)-round(((sumX)*(sumY)), 2))/((n*(sumX2))-((sumX)**2))
        #returning b will mean that b will be outputted if the function is called
        return b

def threadz1():
    while True:
        x = threading.Thread(target=again)
        x.start()
        time.sleep(1)

t = threading.Thread(target=threadz1)
t.start()
#starts when the websocket opens
def websocketstart():
    def on_open(ws):
        #authenticates with the websocket
        auth_data = {
            "action": "auth", "key": "PKYZ2JAJGCF9IPNSF8A0", "secret": "n7TywV2oQcooeJivizHDAKYs3LxKaShSMubnlV75"
        }
        ws.send(json.dumps(auth_data))
        

        listen_message = {"action":"subscribe","quotes":["AAPL"]}

        ws.send(json.dumps(listen_message))

    def on_message(ws, message):
        #does the same thing as aniamte(i)
        global position
        y1212.append(round(realprice1, 2))
        x1212.append(next(index))
        plt.plot(x1212, y1212, color = "r")
        message = json.loads(message)
        position = (message[0]['bp'])
        indexY1.append(position, 2)
        indexX1.append(len(indexX1))
        if len(indexX1) > 3:
            for i in range(len(indexY1)):    
                num = len(tempx1)
                indexX1.append(i)

                tempx1.insert(num, indexX1[i])
                x1 = np.array(tempx1,dtype='double')

                tempy1.insert(num, indexY1[i])
                y1 = np.array(tempy1,dtype='double')

                xy11 = indexX1[i] * indexY1[i]
                tempxy1.insert(num, xy1)

                xy1 = np.array(tempxy1,dtype='double')

                x211 = indexX1[i] ** 2
                tempx21.insert(num, x211)
                x22 = np.array(tempx21,dtype='double')

            n1 = len(x1)
            sumX1 = sum(x1)
            sumY1 = sum(y1)
            sumXY1 = sum(xy11)
            sumX21 = sum(x22) 
            meanX1 = sumX1/n1
            meanY1 = sumY1/n1

            b1 = (round(n1*(sumXY1), 2)-round(((sumX1)*(sumY1)), 2))/((n1*(sumX21))-((sumX1)**2))
            a1 = round(meanY1 - (b1*meanX1), 2)

            if len(future) >= 10:
                if get_b() == b1:
            #checks if b is greater than 0
                    if b > 0:
                        #buys a stock
                        print("bought")
                        api.submit_order(
                            symbol="AAPL",
                            qty=1,
                            side="buy",
                            type="market",
                            time_in_force="gtc"
                        )
                    #checks if b is less than 0
                    elif b < 0:
                        #sells a stock
                        print("sold")
                        api.submit_order(
                            symbol="AAPL",
                            qty=1,
                            side="sell",
                            type="market",
                            time_in_force="gtc"
                        )
                    #clears the counter 
                    future.clear()
        
    socket = "wss://stream.data.alpaca.markets/v2/iex"

    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
    ws.run_forever()

t = threading.Thread(target=websocketstart)
t.start()

root = Tk.Tk()
label = Tk.Label(root, text="Realtime Animated Graphs").grid(column=0, row=0)

canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().grid(column=0, row=1)

ani = FuncAnimation(plt.gcf(), animate, interval=1000, blit=False)

Tk.mainloop()