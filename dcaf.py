#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 11:30:13 2019
@author: Esteban
"""
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
import os.path as path
import shutil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time
import picamera
import os

longitud, altura = 150, 150
modelo = './modelo/modelo.h5'
pesos_modelo = './modelo/pesos.h5'
cnn = load_model(modelo)
cnn.load_weights(pesos_modelo)
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("Cargando modelo")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
time.sleep(2)
print("Preparando carpetas")
carpetadefo=r"./Deforestados"
carpetafore=r"./Forestados"
carpetaince=r"./Incendios"
contador=1
if os.path.exists(carpetadefo):
    shutil.rmtree(carpetadefo)
if os.path.exists(carpetafore):
    shutil.rmtree(carpetafore)
if os.path.exists(carpetaince):
    shutil.rmtree(carpetaince)
if not os.path.exists(carpetadefo):
    os.mkdir('./Deforestados')
if not os.path.exists(carpetafore):
    os.mkdir('./Forestados')
if not os.path.exists(carpetaince):
    os.mkdir('./Incendios')
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
time.sleep(2)
print("Iniciando reconocimiento")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
time.sleep(2)
while True:
    if contador<9:
        imagen=r"./DJI_000"+str(contador)+".JPG"
    if contador>9:
        imagen=r"./DJI_00"+str(contador)+".JPG"
    if not path.exists(imagen):
        with picamera.PiCamera() as picam:
            picam.start_preview()
            time.sleep(2)
            picam.capture(imagen)
            picam.stop_preview()
            picam.close()
        time.sleep(1)
        print("Imagen capturada con éxito")
    if path.exists(imagen):
        time.sleep(3)
        def predict(file):
            time.sleep(3)
            x = load_img(file, target_size=(longitud, altura))
            x = img_to_array(x)
            x = np.expand_dims(x, axis=0)
            array = cnn.predict(x)
            result = array[0]
            answer = np.argmax(result)
            print("Analizando "+imagen)
            if answer == 0:
                print("Se ha detectado una zona deforestada")
                shutil.move(imagen, r"./Deforestados")
                msg = MIMEMultipart()
                message = "Se ha detectado una zona en peligro"
                password = "noaladeforestacion"
                msg['From'] = "dcadeforestacion@gmail.com"
                msg['To'] = "estebangfernandeza@gmail.com"
                msg['Subject'] = "ALERTA"
                msg.attach(MIMEText(message, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com: 587')
                server.starttls()
                server.login(msg['From'], password)
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                server.quit()
                print ("Correo electrónico de alerta enviado con éxito")
            elif answer == 1:
                print("Se ha detectado una zona con riesgo de incendio")
                shutil.move(imagen, r"./Incendios")
                msg = MIMEMultipart()
                message = "Se ha detectado una zona en peligro"
                password = "noaladeforestacion"
                msg['From'] = "dcadeforestacion@gmail.com"
                msg['To'] = "estebangfernandeza@gmail.com"
                msg['Subject'] = "ALERTA RIESGO DE INCENDIO"
                msg.attach(MIMEText(message, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com: 587')
                server.starttls()
                server.login(msg['From'], password)
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                server.quit()
                print ("Correo electrónico de alerta enviado con éxito")
            elif answer == 2:
                print("Se ha detectado una zona forestada")
                shutil.move(imagen, r"./Forestados")
            return answer
        contador=contador+1
        predict(imagen)
