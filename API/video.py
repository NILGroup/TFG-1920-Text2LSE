import os, uuid
from moviepy.editor import VideoFileClip, concatenate_videoclips


#Poner ruta donde tengáis los vídeos
path = "C:/Users/Miguel/Desktop/videos/"


def existeVideo(token):
    #Se puede utilizar con el Texto ya que solo hay que
    #pasarle el token (bucle for).
    if(os.path.isfile(path + token +".mp4")):
        return True
    return False

#-----------------------------------------------#
#----------------- PALABRA ---------------------#
#-----------------------------------------------#
def getVideoPalabra(palabra):
    return VideoFileClip(path + palabra +".mp4")

 

#-----------------------------------------------#
#----------------- TEXTO -----------------------#
#-----------------------------------------------#

        












