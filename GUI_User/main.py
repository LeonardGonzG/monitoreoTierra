import serial, json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re
import threading

arduino = serial.Serial('COM3', 230400)
e = arduino.readline()
limit = 500;
palette={"primary":"#FEF702",
         "background": "#252525",
         "primary_chart":"#F1F1F1",
         "text_color": "#7F7F7F"}

gData = []
gData.append([0])
gData.append([0])

pData = []
pData.append([0])
pData.append([0])

aData = []
aData.append([0])
aData.append([0])

hData = []
hData.append([0])
hData.append([0])

rData = []
rData.append([0])
rData.append([0])

hfData = []
hfData.append([0])
hfData.append([0])

#------------------------------------------------------------------------------------------
#Temparatura
fig = plt.figure()
ax = fig.add_subplot(111)
hl, = plt.plot(gData[0], gData[1], color = "green")
ax.set_ylabel("°C",
              ha="center",
              size=16)
plt.suptitle("Temperatura ambiental",
             horizontalalignment = 'left',
             x=0.05,
             y=0.99,
             transform=fig.transFigure,
             color=palette["background"],
             bbox=dict(facecolor=palette["primary"], edgecolor="none", pad=10.0))
plt.ylim(10, 50)
plt.xlim(0,limit)
#------------------------------------------------------------------------------------------
#Presión
figP = plt.figure()
ax = figP.add_subplot(111)
hlP, = plt.plot(pData[0], pData[1], color = "darkblue")
ax.set_ylabel("Pa",
              ha="center",
              size=16)
plt.suptitle("Presión atmosférica",
             horizontalalignment = 'left',
             x=0.05,
             y=0.99,
             transform=fig.transFigure,
             color=palette["background"],
             bbox=dict(facecolor="#a6f7ef", edgecolor="none", pad=10.0))
plt.ylim(79100, 79900)
plt.xlim(0,limit)

#------------------------------------------------------------------------------------------
#Altitude
figA = plt.figure()
ax = figA.add_subplot(111)
hlA, = plt.plot(aData[0], aData[1], color = "#7c099c")

ax.set_ylabel("Metros",
              ha="center",
              size=16)
plt.suptitle("Altitud",
             horizontalalignment = 'left',
             x=0.05,
             y=0.99,
             transform=fig.transFigure,
             color=palette["background"],
             bbox=dict(facecolor="#b3f7a6", edgecolor="none", pad=10.0))

plt.ylim(2000, 2100)
plt.xlim(0,limit)
#------------------------------------------------------------------------------------------
#Humedad aire
figH = plt.figure()
ax = figH.add_subplot(111)
hlH, = plt.plot(hData[0], hData[1], color = "#696053")
ax.set_ylabel("%",
              ha="center",
              size=16)
plt.suptitle("Humedad del aire",
             horizontalalignment = 'left',
             x=0.05,
             y=0.99,
             transform=fig.transFigure,
             color=palette["background"],
             bbox=dict(facecolor="#ffca75", edgecolor="none", pad=10.0))

plt.ylim(0, 100)
plt.xlim(0,limit)
#------------------------------------------------------------------------------------------
#LLuvia
figR = plt.figure()
ax = figR.add_subplot(111)
hlR, = plt.plot(rData[0], rData[1], color = "#16097d")
ax.set_ylabel("Unidad",
              ha="center",
              size=16)
plt.suptitle("Detección de lluvia",
             horizontalalignment = 'left',
             x=0.05,
             y=0.99,
             transform=fig.transFigure,
             color= palette["background"],
             bbox=dict(facecolor="#a99ff5", edgecolor="none", pad=10.0))
plt.ylim(0, 2000)
plt.xlim(0,limit)
#------------------------------------------------------------------------------------------
#humedad de la tierra
figHF = plt.figure()
ax = figHF.add_subplot(111)
hlHF, = plt.plot(hfData[0], hfData[1], color = "#590024")

ax.set_ylabel("Unidad",
              ha="center",
              size=16)
plt.suptitle("Humedad de la tierra",
             horizontalalignment = 'left',
             x=0.05,
             y=0.99,
             transform=fig.transFigure,
             color=palette["background"],
             bbox=dict(facecolor="#ffabcd", edgecolor="none", pad=10.0))
plt.ylim(200, 600)
plt.xlim(0,limit)
#------------------------------------------------------------------------------------------

def GetData(out_dataT, out_pressure, out_alt, out_hum, out_rain, out_humF):
    while (True):
        datosString = arduino.readline()
        datos = datosString.decode('utf-8')
        ans = json.loads(datos)

        if ans["status"]:

            temp = ans["temperature"]
            pressure = ans["pressure"]
            alt = ans["altitude"]
            hum = ans["humidity"]
            rain = ans["rain"]
            humFloor = ans["humidityFloor"]

            out_dataT[1].append( temp )
            out_pressure[1].append(pressure)

            print('temp',temp)
            print('pressure', pressure)
            print('altitude', alt)
            print('humidity', hum)
            print('rain', rain)
            print('HumidityFloor', humFloor)

            out_alt[1].append(alt)
            out_hum[1].append(hum)
            out_rain[1].append(rain)
            out_humF[1].append(humFloor)

            if len(out_dataT[1]) > limit:
                out_dataT[1].pop(0)
            if len(out_pressure[1]) > limit:
                out_pressure[1].pop(0)
            if len(out_alt[1]) > limit:
                out_alt[1].pop(0)
            if len(out_hum[1]) > limit:
                out_hum[1].pop(0)
            if len(out_rain[1]) > limit:
                out_rain[1].pop(0)
            if len(out_humF[1]) > limit:
                out_humF[1].pop(0)

def update_line(num, hl, data):
    hl.set_data(range(len(data[1])), data[1])
    return hl,

line_ani = animation.FuncAnimation(fig, update_line, fargs=(hl, gData),
    interval=1000, blit=False)

line_aniP = animation.FuncAnimation(figP, update_line, fargs=(hlP, pData),
    interval=1000, blit=False)

line_aniA = animation.FuncAnimation(figA, update_line, fargs=(hlA, aData),
    interval=1000, blit=False)

line_aniH = animation.FuncAnimation(figH, update_line, fargs=(hlH, hData),
    interval=1000, blit=False)

line_aniR = animation.FuncAnimation(figR, update_line, fargs=(hlR, rData),
    interval=1000, blit=False)

line_aniHF = animation.FuncAnimation(figHF, update_line, fargs=(hlHF, hfData),
    interval=1000, blit=False)

dataCollector = threading.Thread(target = GetData, args=(gData,pData,aData,hData,rData,hfData))
dataCollector.start()

plt.show()
dataCollector.join()
