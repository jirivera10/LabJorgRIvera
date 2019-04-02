import urllib
from io import StringIO
from io import BytesIO
import csv
import numpy as np
from datetime import datetime
import matplotlib.pylab as plt
import pandas as pd
import scipy.signal as signal
Inicio = '20111118'
Final   = '20121125'
datos=pd.read_csv('http://lobo.satlantic.com/cgi-data/nph-data.cgi?min_date='+Inicio+'&max_date='+Final+'&y=temperature',sep="\t")
datos["date [AST]"]=pd.to_datetime(datos["date [AST]"],format='%Y%m%d %H:%M:%S')
datos.set_index(["date [AST]"],inplace=True)
datos.plot(figsize=(20,7))
plt.show()
Inicio = '20111118'
Final   = '20121125'
response=urllib.request.urlopen('http://lobo.satlantic.com/cgi-data/nph-data.cgi?min_date='+Inicio+'&max_date='+Final+'&y=temperature')
leer=response.read()
data = StringIO(leer.decode())
r = csv.DictReader(data,dialect=csv.Sniffer().sniff(data.read(1000)))
data.seek(0)
date, temp = [],[]
date, temp = zip(*[(datetime.strptime(x['date [AST]'], "%Y-%m-%d %H:%M:%S"), x['temperature [C]']) for x in r if x['temperature [C]'] is not None])
temp = np.array(temp)
temp = temp.astype(np.float)
plt.figure(figsize=(20,7))
plt.plot(date,temp)
plt.xticks(rotation=70)
plt.show()
N  = 2    # Orden del filtro
Wn = 0.01 # Corte de frecuancia
B, A = signal.butter(N, Wn)
temp_filtrada = signal.filtfilt(B,A, temp)
fig = plt.figure(figsize=(20,10))
ax1 = fig.add_subplot(211)
plt.plot(date,temp, 'b-')
plt.plot(date,temp_filtrada, 'r-',linewidth=2)
plt.ylabel(r"Temperatura ($^{\circ}C$)")
plt.legend(['Original','Filtrado'])
plt.title("Temperatura de LOBO (Halifax, Canada)")
ax1.axes.get_xaxis().set_visible(False)
ax1 = fig.add_subplot(212)
plt.plot(date,temp-temp_filtrada, 'b-')
plt.ylabel(r"Temperatura ($^{\circ}C$)")
plt.xlabel("Fecha")
plt.legend(['Residuales'])
plt.show()
plt.figure(figsize=(20,7))
ruido=temp-temp_filtrada
corr=signal.correlate(ruido,ruido,mode="full")
plt.plot(corr[len(corr)//2:])
plt.show()
plt.figure(figsize=(20,7))
corr=np.correlate(ruido,ruido,mode="full")
plt.plot(corr[len(corr)//2:])
plt.show()
plt.figure(figsize=(20,7))
corr=np.correlate(ruido,ruido,mode="full")
plt.plot(np.abs(corr[len(corr)//2:]))
plt.show()
response=urllib.request.urlopen('https://raw.githubusercontent.com/ComputoCienciasUniandes/FISI2029-201910/master/Seccion_1/Fourier/Datos/transacciones2008.txt')
leer=response.read()
data = StringIO(leer.decode())
r = csv.DictReader(data,dialect=csv.Sniffer().sniff(data.read(1000)))
data.seek(0)
date, temp = [],[]
date, temp = zip(*[(datetime.strptime(x['date [AST]'], "%Y-%m-%d %H:%M:%S"), x['temperature [C]']) for x in r if x['temperature [C]'] is not None])
temp = np.array(temp)
temp = temp.astype(np.float)
