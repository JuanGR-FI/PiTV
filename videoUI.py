#!/usr/bin/env python3

#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
## FACULTAD DE INGENIERIA
## FUNDAMENTOS DE SISTEMAS DISTRIBUIDOS
## CELIS DIAZ MIGUEL ANGEL
## CERVANTES GUATI ROJO JUAN ANDRES
## LOPEZ HERNANDEZ EMANUEL
## ALVIRDE SOSA ANGEL
## SEMESTRE 2023-1
#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

#Bibliotecas necesarias para la visualizacion de interfaces graficas
from tkinter import *
from tkinter.font import Font
from tkinter import filedialog
#Bibliotecas necesarias para manejo de imagenes
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
#Bibliotecas necesarias para instrucciones del SO
from sys import argv
import os
from os import listdir
from os.path import isfile, isdir

#Colores
color_black = "#080808"
color_dark_gray = "#101010"
color_white = "#FFFFFF"

#Variables Globales
videoFiles = []
videoIndex = 0
PATH = ""
cap = None

#Lista los archivos de una ruta especifica
def listDirFiles(path):    
    return [obj for obj in listdir(path) if isfile(path + obj)]

#Se encarga de listar los videos que se encuentran en la usb
def listVideoFiles(PATH):
    #Se guardan los nombres de los archivos que se vayan encontrando
    global videoFiles
    
    #Se manda la ruta del directorio que queremos buscar
    files=listDirFiles(PATH)
    
    #Se hace un filtrado de los archivos de video
    for file in files:
        split_tup = os.path.splitext(file)
        extension = split_tup[1]
        print(file + " extension: " + extension)
        if(extension == ".mp4" or extension == ".avi"):
            videoFiles.append(file)
        else:
            print("File extension not supported...")
            
    print("Video files: " + str(videoFiles))

#Se encarga de seleccionar el video que se desea reproducir abriendo un filedialog
def chooseVideoToPlay():
    global cap
    if cap is not None:#Si llega otro video para reproducirse, detiene el actual y limpia el label
        lblVideo.image = ""
        cap.release()
        cap = None
    video_path = filedialog.askopenfilename(filetypes = [
        ("all video format", ".mp4"),
        ("all video format", ".avi")])
    if len(video_path) > 0:#Si se elige una ruta se comienza a reproducir el video
        lblInfoVideoPath.configure(text="Now playing: " + video_path)
        cap = cv2.VideoCapture(video_path)
        visualize()
    else:
        lblInfoVideoPath.configure(text="No video selected yet...")

#Se encarga de mostrar el video a pantalla
def visualize():
    global cap
    if cap is not None:
        ret, frame = cap.read()#Se leen los frames del video
        if ret == True:#Mientras existan frames se seguiran actualizando
            frame = imutils.resize(frame, width=1080)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualize)
        else:
            lblInfoVideoPath.configure(text="No video selected yet...")
            lblVideo.image = ""
            cap.release()

#Se encarga de reproducir el modo galeria de videos
def playGalleryMode():
    global cap
    global videoFiles
    global videoIndex
    global PATH
    
    if cap is not None:#Si llega otro video para reproducirse, detiene el actual y limpia el label
        lblVideo.image = ""
        cap.release()
        cap = None
    if(videoIndex != len(videoFiles)):#Si todavia no llegamos al ultimo archivo debe ejecutar el siguiente video
        lblInfoVideoPath.configure(text="Now playing: " + videoFiles[videoIndex])
        cap = cv2.VideoCapture(PATH + videoFiles[videoIndex])
        visualizeNext()
    else:#Caso contrario actualizamos el indice
        videoIndex = 0

#Se encarga de mostrar el siguiente video del modo galeria a pantalla
def visualizeNext():
    global cap
    global videoIndex
    #Realiza el mismo proceso que visualize()
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=1080)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizeNext)
        else:
            lblInfoVideoPath.configure(text="No video selected yet...")
            lblVideo.image = ""
            cap.release()
            videoIndex += 1#Lo unico que cambia es que actualiza el indice para reproducir el siguiente video
            playGalleryMode()
    
#Cierra la ventana
def closeWindow(root):
    root.destroy()

#Atrapamos la ruta de la usb que llega desde otro script
script, path = argv
listVideoFiles(path)
PATH = path

print("La ruta que me llego fue: " + path)

#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-PROGRAMA PRINCIPAL*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

root = Tk()
root.configure(bg=color_black)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.title("Video Player")
root.attributes('-fullscreen', True)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)

root.rowconfigure(3, weight=1)

text_font = Font(family="Roboto", size=10, weight="bold")
#Imagenes utilizadas
nofile_logo = Image.open("Images/file-notfound-logo.png")
nofile_logo = ImageTk.PhotoImage(nofile_logo, master=root)

lbl_title = Label(root,font=text_font, text="VIDEO GALLERY", compound="right", bg=color_black, foreground=color_white)
lbl_title.grid(column=0,row=0,padx=10,pady=10, sticky="W", columnspan=2)

btnVisualizar = Button(root, text="Choose video", command=chooseVideoToPlay, font=text_font, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
btnVisualizar.grid(column=1, row=1, padx=5, pady=5, sticky="WSEN")

btnGallery = Button(root, text="Gallery Mode", command=playGalleryMode, font=text_font, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
btnGallery.grid(column=2, row=1, padx=5, pady=5, sticky="WSEN")

lblInfoVideoPath = Label(root, text="No video selected yet...", bg=color_black, foreground=color_white)
lblInfoVideoPath.grid(column=1, row=2,padx=5,pady=5)

lblVideo = Label(root, bg=color_black, image=nofile_logo)
lblVideo.grid(column=1, row=3,padx=5,pady=5, columnspan=2)

btn_close = Button(root, command=lambda: closeWindow(root), text="RETURN", font=text_font, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
btn_close.grid(column=3,row=1,padx=2,pady=2, sticky="WSEN")

root.mainloop()



