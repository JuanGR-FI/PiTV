#Bibliotecas necesarias para la visualizacion de interfaces graficas
from tkinter import *
from tkinter.font import Font
from tkinter import filedialog
#Bibliotecas necesarias para manejo de imagenes
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
#Biblioteca para manejo de audio
import pygame
from audioplayer import AudioPlayer
#Bibliotecas necesarias para instrucciones del SO
import os
from os import listdir
from os.path import isfile, isdir
from subprocess import Popen, PIPE
from signal import SIGTERM
#Biblioteca necesaria para abrir navegadores web
import webbrowser

#URLs
url_netflix = "https://www.netflix.com"
url_spotify = "https://www.spotify.com"

#Colores
color_black = "#080808"
color_dark_gray = "#101010"
color_white = "#FFFFFF"

#Variables globales necesarias para el manejo de imagenes y video
image = None
cap = None
mixer = None
imageIndex = 0
songToPlay = None

#Lista los archivos de una ruta especifica
def listDirFiles(path):    
    return [obj for obj in listdir(path) if isfile(path + obj)]

#Se encarga de abrir una nueva ventana para poder reproducir Netflix
def playNetflix():
    #global url_netflix
    
    #webbrowser.open(url_netflix, new=1)
    root = Toplevel()
    root.configure(bg=color_black)
    width = root.winfo_screenwidth()
    #root.attributes('-alpha', 0.5)
    root.attributes('-type','splash')
    root.attributes('-topmost', True)
    #root.attributes('-fullscreen', True)
    root.geometry("%dx110+0+0" % (width))
    text_font5 = Font(family="Roboto", size=10, weight="bold")
    
    btn_close = Button(root, command=lambda: closeWindowAndBrowser(root), text="RETURN", font=text_font5, width=20, height=5, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_close.grid(column=0,row=0,padx=2,pady=2)
    
    root.after(100, openNetflixBrowser)
    
    root.mainloop()

#Se encarga de abrir una nueva ventana para poder reproducir Spotify
def playSpotify():
    #global url_spotify
    
    #webbrowser.open(url_spotify, new=1)
    
    root = Toplevel()
    root.configure(bg=color_black)
    width = root.winfo_screenwidth()
    #root.attributes('-alpha', 0.5)
    root.attributes('-type','splash')
    root.attributes('-topmost', True)
    #root.attributes('-fullscreen', True)
    root.geometry("%dx110+0+0" % (width))
    text_font5 = Font(family="Roboto", size=10, weight="bold")
    
    btn_close = Button(root, command=lambda: closeWindowAndBrowser(root), text="RETURN", font=text_font5, width=20, height=5, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_close.grid(column=0,row=0,padx=2,pady=2)
    
    root.after(100, openSpotifyBrowser)
    
    root.mainloop()

def openNetflixBrowser():
    global url_netflix
    webbrowser.open(url_netflix, new=1)

def openSpotifyBrowser():
    global url_spotify
    webbrowser.open(url_spotify, new=1)
    

#Se encarga de cerrar el navegador cuando se quiera regresar al menu principal
def closeWindowAndBrowser(root):
    kill_process("chromium-browse")
    root.destroy()

#Se encarga de verificar el tipo de archivos que tiene un directorio en especifico
def verifyFilesType():
    """path = filedialog.askopenfilename(filetypes = [
        ("image",".jpg"),
        ("image",".jpeg"),
        ("image",".png")])"""
    #Se guardan los nombres de los archivos que se vayan encontrando
    imageFiles = []
    videoFiles = []
    audioFiles = []
    
    #Se manda la ruta del directorio que queremos buscar
    files=listDirFiles("/home/raspberry/Desktop/PiTV/Images/Test/")
    files2=listDirFiles("/home/raspberry/Desktop/PiTV/Videos/")
    files3=listDirFiles("/home/raspberry/Desktop/PiTV/Audio/")
    for file in files3:
        split_tup = os.path.splitext(file)
        extension = split_tup[1]
        print(file + " extension: " + extension)
        if(extension == ".jpg" or extension == ".jpeg" or extension == ".png"):
            imageFiles.append(file)
        elif(extension == ".mp4" or extension == ".avi"):
            videoFiles.append(file)
        elif(extension == ".mp3"):
            audioFiles.append(file)
        else:
            print("File extension not supported...")
            
    print("Video files: " + str(videoFiles))
    print("Image files: " + str(imageFiles))
    print("Audio files: " + str(audioFiles))
    
    if(len(imageFiles) > 0 and len(videoFiles) == 0 and len(audioFiles) == 0):
        openImageGallery(imageFiles)
    elif(len(videoFiles) > 0 and len(imageFiles) == 0 and len(audioFiles) == 0):
        openVideos(videoFiles)
    elif(len(audioFiles) > 0 and len(imageFiles) == 0 and len(videoFiles) == 0):
        openAudios(audioFiles)
    else:
        print("Archivos mixtos")

def openAudios(audioList):
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.title("Audio Player")
    #root.geometry("%dx%d" % (width,height))
    root.attributes('-fullscreen', True)
    root.configure(bg=color_black)
    
    #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-Contenedor Frame Galeria de imagenes*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    frame = Frame(root)
    frame.config(bd="10", bg=color_dark_gray)
    frame.pack(fill="both",padx=20,pady=20, expand=True)
    #frame.grid(column=0,row=0,padx=20,pady=20,sticky="NSEW")
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.columnconfigure(3, weight=1)
    frame.columnconfigure(4, weight=1)
    frame.columnconfigure(5, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    
    text_font3 = Font(family="Roboto", size=40, weight="bold")
    
    #Imagenes utilizadas
    itunes_logo = Image.open("Images/itunes-logo.png")
    itunes_logo = ImageTk.PhotoImage(itunes_logo, master=frame)
    
    song_playing_logo = Image.open("Images/song-playing-logo.png")
    song_playing_logo = ImageTk.PhotoImage(song_playing_logo, master=frame)
    
    lbl_title = Label(frame,font=text_font3, image=itunes_logo, text="AUDIO PLAYER", compound="right", bg=color_dark_gray, foreground=color_white)
    lbl_title.grid(column=2,row=0,padx=10,pady=10, sticky="N", columnspan=2)
    
    lbl_songname = Label(frame,font=text_font3, image=song_playing_logo, text="Now playing: ", compound="top", bg=color_dark_gray, foreground=color_white)
    lbl_songname.grid(column=2,row=1,padx=10,pady=10, columnspan=2)
    
    #lblImage = Label(frame, fg=color_black )
    #lblImage.grid(column=1, row=1,padx=10,pady=10)
    
    btn_prev = Button(frame, text="PREVIOUS", font=text_font3, width=30, height=5, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_prev.grid(column=0,row=2,padx=10,pady=10,ipadx=10,ipady=10)
    
    btn_play = Button(frame, text="PLAY", font=text_font3, width=30, height=5, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_play.grid(column=1,row=2,padx=10,pady=10)
    
    btn_pause = Button(frame, text="PAUSE", font=text_font3, width=30, height=5, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_pause.grid(column=2,row=2,padx=10,pady=10)
    
    btn_resume = Button(frame, text="RESUME", font=text_font3, width=30, height=5, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_resume.grid(column=3,row=2,padx=10,pady=10)
    
    btn_stop = Button(frame, text="STOP", font=text_font3, width=30, height=5, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_stop.grid(column=4,row=2,padx=10,pady=10)
    
    btn_next = Button(frame, text="NEXT", font=text_font3, width=30, height=5, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_next.grid(column=5,row=2,padx=10,pady=10,ipadx=10,ipady=10)
    
    btn_close = Button(frame, text="CLOSE", command=lambda: closeAudio(root), font=text_font3, width=30, height=5, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_close.grid(column=2,row=3,padx=10,pady=10, sticky="S", columnspan=2)
    
    playAudioFiles(audioList, lbl_songname)
    
    root.mainloop()

#Se encarga de reproducir los sonidos en bucle
def playAudioFiles(audioList, label):
    global songToPlay
    
    songToPlay = AudioPlayer("/home/raspberry/Desktop/PiTV/Audio/" + audioList[0])
    songToPlay.play(loop=True, block=False)
    label.configure(text="Playing: " + str(audioList[0]))

def closeAudio(root):
    global songToPlay
    songToPlay.stop()
    #pygame.mixer.music.stop()
    root.destroy()
        
def openImageGallery(imageList):
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.title("Image Gallery")
    #root.geometry("%dx%d" % (width,height))
    root.attributes('-fullscreen', True)
    root.configure(bg=color_black)
    
    #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-Contenedor Frame Galeria de imagenes*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    frame = Frame(root)
    frame.config(bd="10", bg=color_dark_gray)
    frame.pack(fill="both",padx=20,pady=20, expand=True)
    #frame.grid(column=0,row=0,padx=20,pady=20,sticky="NSEW")
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    
    text_font3 = Font(family="Roboto", size=40, weight="bold")
    
    #Imagenes utilizadas
    gallery_logo = Image.open("Images/AppsGallery-logo.png")
    gallery_logo = ImageTk.PhotoImage(gallery_logo, master=frame)
    
    lbl_title = Label(frame,font=text_font3, image=gallery_logo, text="IMAGE GALLERY", compound="right", bg=color_dark_gray, foreground=color_white)
    lbl_title.grid(column=1,row=0,padx=10,pady=10, sticky="N")
    
    lblImage = Label(frame, fg=color_black )
    lblImage.grid(column=1, row=1,padx=10,pady=10)
    
    btn_prev = Button(frame, text="<<", command=lambda: prevImage(imageList, lblImage, frame), font=text_font, width=10, height=10, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_prev.grid(column=0,row=1,padx=10,pady=10, sticky="W")
    
    btn_next = Button(frame, text=">>", command=lambda: nextImage(imageList, lblImage, frame), font=text_font, width=10, height=10, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_next.grid(column=2,row=1,padx=10,pady=10, sticky="E")
    
    btn_close = Button(frame, text="CLOSE", command=root.destroy, font=text_font3, width=30, height=5, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_close.grid(column=1,row=2,padx=10,pady=10, sticky="S")
    
    putImage(lblImage, frame, imageList[0])
    
    root.mainloop()

def openVideos(videoList):
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.title("Video Player")
    #root.geometry("%dx%d" % (width,height))
    root.attributes('-fullscreen', True)
    root.configure(bg=color_black)
    
    #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-Contenedor Frame Video Player*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    frame = Frame(root)
    frame.config(bd="10", bg=color_dark_gray)
    frame.pack(fill="both",padx=20,pady=20, expand=True)
    #frame.grid(column=0,row=0,padx=20,pady=20,sticky="NSEW")
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    
    text_font4 = Font(family="Roboto", size=40, weight="bold")
    
    #Imagenes utilizadas
    video_logo = Image.open("Images/MediaPlayer-logo.png")
    video_logo = ImageTk.PhotoImage(video_logo, master=frame)
    
    lbl_title = Label(frame,font=text_font4, image=video_logo, text="VIDEO PLAYER", compound="right", bg=color_dark_gray, foreground=color_white)
    lbl_title.grid(column=0,row=0,padx=10,pady=10, sticky="WN")
    
    lblVideo = Label(frame, fg=color_black )
    lblVideo.grid(column=1, row=0,padx=10,pady=10)
    
    btn_video = Button(frame, text="Choose video", command=lambda: chooseVideo(lblVideo, frame), font=text_font4, width=30, height=5, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_video.grid(column=0,row=1,padx=10,pady=10, sticky="W")
    
    btn_close = Button(frame, text="CLOSE", command=root.destroy, font=text_font4, width=30, height=5, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
    btn_close.grid(column=0,row=2,padx=10,pady=10, sticky="WS")
    
    root.mainloop()
    
def visualize(lblVideo, root):
    global cap
    ret, frame = cap.read()
    if ret == True:
        frame = imutils.resize(frame, width=640)
        #frame = frame.resize((640,640),Image.LANCZOS)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(im, master=root)
        
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualize(lblVideo, root))
        
def chooseVideo(lblVideo, root):
    global cap
    videoPath = filedialog.askopenfilename(filetypes = [
        ("all video format",".mp4"),
        ("all video format",".avi")])
    if len(videoPath) > 0:
        print(videoPath)
        cap = cv2.VideoCapture(videoPath)
        visualize(lblVideo, root)
    else:
        print("No se selecciono ningun video")

def nextImage(imList, label, root):
    global imageIndex
    imageIndex += 1
    if(imageIndex == len(imList)):
        imageIndex -= 1
    else:
        putImage(label, root, imList[imageIndex])

def prevImage(imList, label, root):
    global imageIndex
    imageIndex -= 1
    if(imageIndex < 0):
        imageIndex += 1
    else:
        putImage(label, root, imList[imageIndex])
    
def putImage(lblImage, root, imName):
    global image
    lblImage.image = ""
    print("Cambiando a imagen: " + imName)
    path = "/home/raspberry/Desktop/PiTV/Images/Test/" + imName
    image = Image.open(path)
    width, height = image.size
    if(width == height):
        image = image.resize((500,500),Image.LANCZOS)
    else:
        image = image.resize((600,400),Image.LANCZOS)
    
    
    img = ImageTk.PhotoImage(image, master=root)
    lblImage.configure(image=img)
    lblImage.image = img

def kill_process(name):
    ps = Popen(["ps","-e"], stdout=PIPE)
    grep = Popen(["grep", name], stdin=ps.stdout, stdout=PIPE)
    ps.stdout.close()
    data = grep.stdout.read().decode()
    if data:
        print("Proceso activo con nombre " + name + " encontrado")
        lines =data.split('\n')
        print(lines)
        for line in lines:
            pid = line.split('?')[0]
            pid = pid.strip()
            print("pid: " + pid)
            if pid:
                print("Matando " + pid + "...")
                try:
                    os.kill(int(pid), SIGTERM)
                except Exception as e:
                    print(e)
    else:
        print("No hay procesos activos...")
    

#Creando ventana principal
root = Tk()

#Dimensiones de la ventana
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
print(str(width) + "x" + str(height))

#Configuraciones ventana principal a pantalla completa
root.title("PiTV")
#root.geometry("%dx%d" % (width,height))
root.attributes('-fullscreen', True)
root.configure(bg=color_black)
root.columnconfigure(0, weight=1)

#Imagenes utilizadas
netflix_logo = Image.open("Images/netflix-logo2.png")
netflix_logo = ImageTk.PhotoImage(netflix_logo)

spotify_logo = Image.open("Images/spotify-logo.png")
spotify_logo = ImageTk.PhotoImage(spotify_logo)

rasp_logo = Image.open("Images/raspberry-logo.png")
rasp_logo = ImageTk.PhotoImage(rasp_logo)

usb_logo = Image.open("Images/usb-logo.png")
usb_logo = ImageTk.PhotoImage(usb_logo)

#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-Contenedor Frame principal*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
frame = Frame(root)
frame.config(bd="10", bg=color_dark_gray)
frame.pack(fill="both",expand=True, padx=20,pady=20)
#frame.grid(column=0,row=0,padx=20,pady=20,sticky="NSEW")
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)
frame.rowconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)
frame.rowconfigure(2, weight=1)

text_font = Font(family="Roboto", size=20, weight="bold")
text_font2 = Font(family="Roboto", size=10, weight="bold")

lbl_title = Label(frame,font=text_font, image=rasp_logo, text="Pi TV", compound="right", bg=color_dark_gray, foreground=color_white)
lbl_title.grid(column=1,row=0,padx=10,pady=10)

btn_netflix = Button(frame, image = netflix_logo, command=playNetflix, text="NETFLIX", compound="top",width=30, height=30, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
btn_netflix.grid(column=0,row=1,padx=10,pady=10, ipadx=150, ipady=150)

btn_spotify = Button(frame, image = spotify_logo, command=playSpotify, text="SPOTIFY", compound="top",width=30, height=30, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
btn_spotify.grid(column=1,row=1,padx=10,pady=10, ipadx=150, ipady=150)

btn_imagenes = Button(frame, image = usb_logo,command=verifyFilesType, text="MEDIA", compound="top",width=30, height=30, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
btn_imagenes.grid(column=2,row=1,padx=10,pady=10, ipadx=150, ipady=150)

btn_close = Button(frame, text="CLOSE", command=root.destroy, font=text_font, width=10, height=2, bg=color_black, fg=color_white, highlightbackground=color_dark_gray, activebackground="#272727")
btn_close.grid(column=1,row=2,padx=10,pady=10, sticky="S")

lbl_copyright = Label(frame,text="© Copyright 2023", compound="right", bg=color_dark_gray, foreground=color_white)
lbl_copyright.grid(column=2,row=2,padx=10,pady=10, sticky="SE")

root.mainloop()

