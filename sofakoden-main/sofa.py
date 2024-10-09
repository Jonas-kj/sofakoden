#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 10:18:16 2024

@author: oleandersnetland
"""

import csv
from datetime import datetime

def les_data(filnavn):
    dato_tid = []
    tid_siden_start = []
    trykk_barometer = []
    trykk_absolutt = []
    temperatur = []

    with open(filnavn, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  # Hopp over header-linjen

        for row in reader:
            dato_tid.append(row[0])
            tid_siden_start.append(float(row[1]))
            trykk_barometer.append(row[2] if row[2] != '' else None)
            trykk_absolutt.append(float(row[3].replace(',', '.')))
            temperatur.append(float(row[4].replace(',', '.')))

    return dato_tid, tid_siden_start, trykk_barometer, trykk_absolutt, temperatur

# Test lesing av data
filnavn = 'trykk_og_temperatur.csv.txt'  # Sett inn riktig filnavn
dato_tid, tid_siden_start, trykk_barometer, trykk_absolutt, temperatur = les_data(filnavn)

# Sjekk at indeksene stemmer
for i in range(len(dato_tid)):
    print(f"Tidspunkt: {dato_tid[i]}, Tid: {tid_siden_start[i]} s, Barometertrykk: {trykk_barometer[i]}, "
          f"Absolutt trykk: {trykk_absolutt[i]} bar, Temperatur: {temperatur[i]}°C")

# Funksjon for å lese data fra Sola værstasjon
def les_data_sola(filnavn):
    navn = []
    stasjon = []
    tid_norsk_normaltid = []
    lufttemperatur = []
    lufttrykk_havniva = []

    with open(filnavn, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  # Hopp over header-linjen

        for row in reader:
            navn.append(row[0])
            stasjon.append(row[1])
            # Sjekk om tidskolonnen ikke er tom før parsing
            if row[2].strip():  # Sørger for at strengen ikke er tom eller bare mellomrom
                tid_norsk_normaltid.append(datetime.strptime(row[2], '%d.%m.%Y %H:%M'))  # Dato og tid-formatet for Sola
            else:
                tid_norsk_normaltid.append(None)  # Hvis tid mangler, legg til None

            # Sjekk om temperaturkolonnen ikke er tom før konvertering
            if row[3].strip():
                lufttemperatur.append(float(row[3].replace(',', '.')))  # Erstatt komma med punktum for konvertering
            else:
                lufttemperatur.append(None)  # Hvis temperatur mangler, legg til None

            # Sjekk om lufttrykkkolonnen ikke er tom før konvertering
            if row[4].strip():
                lufttrykk_havniva.append(float(row[4].replace(',', '.')))  # Erstatt komma med punktum
            else:
                lufttrykk_havniva.append(None)  # Hvis lufttrykk mangler, legg til None

    return navn, stasjon, tid_norsk_normaltid, lufttemperatur, lufttrykk_havniva

# Test lesing av data fra Sola
filnavn_sola = 'temperatur_sola.csv'  # Sett inn riktig filnavn
navn, stasjon, tid_norsk_normaltid, lufttemperatur, lufttrykk_havniva = les_data_sola(filnavn_sola)

# Sjekk de første 5 radene
for i in range(len(navn)):
    print(f"Navn: {navn[i]}, Tid: {tid_norsk_normaltid[i]}, Temperatur: {lufttemperatur[i]}, Lufttrykk: {lufttrykk_havniva[i]}")
    
    


# Her er koden du legger til eller erstatter med for å plotte dataene:
import matplotlib.pyplot as plt
from datetime import datetime, timedelta  # Importer timedelta

# Funksjon for å konvertere tid fra listene til datetime-objekter for plotting
def konverter_tid(datoer, tid_siden_start=None):
    if tid_siden_start:
        # Hvis vi har tid siden start (lokal fil), beregn tidspunktene
        start_tid = datetime.strptime(datoer[0], '%m.%d.%Y %H:%M')
        return [start_tid + timedelta(seconds=tid) for tid in tid_siden_start]
    else:
        # Sola-fil datoene er allerede i datetime-format
        return datoer

# Konverter tid fra begge filene
tid_lokal = konverter_tid(dato_tid, tid_siden_start)
tid_sola = konverter_tid(tid_norsk_normaltid)

# Funksjon for å beregne glidende gjennomsnitt
def beregn_gjennomsnitt(tid, temperatur, n):
    ny_tid = []
    ny_temp = []
    
    # Beregn gjennomsnitt for hver gyldig posisjon
    for i in range(n, len(temperatur) - n):
        gjennomsnitt = sum(temperatur[i-n:i+n+1]) / (2*n + 1)
        ny_tid.append(tid[i])
        ny_temp.append(gjennomsnitt)
    
    return ny_tid, ny_temp

# Test gjennomsnitt med n=30
n = 30
ny_tid_lokal, ny_temp_lokal = beregn_gjennomsnitt(tid_lokal, temperatur, n)

# Plot med glidende gjennomsnitt og temperatur fra Sola
plt.figure(figsize=(10, 5))

# Plot original temperatur fra lokal værstasjon
plt.plot(tid_lokal, temperatur, label='Lokal temperatur', color='blue')

# Plot glidende gjennomsnitt fra lokal værstasjon
plt.plot(ny_tid_lokal, ny_temp_lokal, label=f'Lokal temperatur (Gjennomsnitt n={n})', color='orange')

# Plot temperaturen fra Sola værstasjon
plt.plot(tid_sola, lufttemperatur, label='Sola temperatur', color='green')

# Legg til tittel og akser
plt.title('Temperaturdata med glidende gjennomsnitt og Sola værstasjon')
plt.xlabel('Tid')
plt.ylabel('Temperatur (°C)')
plt.legend()

# Vis plottet
plt.show()



#HALLO


