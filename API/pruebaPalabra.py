import requests
from moviepy.editor import VideoFileClip


url = "http://127.0.0.1:8080/video/coche"
response = requests.get(url)


with open("prueba.mp4", 'wb') as f:
        f.write(response.content)


