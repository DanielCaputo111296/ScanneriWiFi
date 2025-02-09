import pywifi
import time
import win10toast
import schedule
import pandas as pd
from scanner_wifi.config import SSID
def scanning_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0] ##creazione della interfaccia#
    iface.scan()
    time.sleep(10)
    profile=iface.scan_results() ##restituisce una lista dei vari AP rilevati##
    return profile
def dataframe_creation(profile):
    canale=[]##creo una lista per raccongliere i canali utilizzati dai vari ssid
    ssid=[]
    bssid=[]
    frequency=[]
    rssi=[]
    for AP in profile:
        ssid.append(AP.ssid)
        bssid.append(AP.bssid)
        frequency.append((AP.freq)/1000)
        rssi.append(AP.signal)
        canale.append(int(channel(AP.freq/1000)))

    data={
        'SSID':ssid,
        'BSSID':bssid,
        'Frequency':frequency,
        'RSSI':rssi,
        'Channel':canale
    }
    df=pd.DataFrame(data)
    df=df.drop_duplicates(subset=['BSSID'])
    df.loc[df["RSSI"]>-65,"Potenza"]="FORTE"
    df.loc[(df["RSSI"]>-85) & (df["RSSI"]<-65),"Potenza"]="MEDIA"
    df.loc[df["RSSI"]<-95,"Potenza"]="SCARSA"
    df=df.sort_values(by=['Potenza'])
    df.to_csv('Scan_reti_wifi'+str(time.time())+".csv", index=False)
    print("Esportazione Completata")
def channel(freq):
    if (freq >= 2412 and freq <= 2484):
        return (freq - 2412) / 5 + 1
    elif (freq >= 5170 and freq <= 5825):
        return (freq - 5170) / 5 + 34
    else:
        return -1

## eseguo la scansione delle reti wi-fi vicine ogni 2 minuti, focalizzandomi poi
## sul mio SSID per monitorare la qualità del segnale. Lo scopo è avvisare
## l'utente se il suo segnale sta degradando sotto una certa soglia
def filtra_ssid(profile):
    for AP in profile:
        if(AP.ssid)==SSID:
            return AP


def job():
    profile=scanning_wifi()
    dataframe_creation(profile)
    AP1=filtra_ssid(profile)
    if (AP1.signal < -65):
        toaster.show_toast("Avviso", "Segnale Peggiorato!", duration=10)

toaster = win10toast.ToastNotifier()
schedule.every(2).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
