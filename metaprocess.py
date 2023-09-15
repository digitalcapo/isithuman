import os
import random
from moviepy.editor import *

# Ruta a la carpeta que contiene los videos
folder_path = '/Users/capo/Desktop/contenido.sensible/renders/individual_fx'

# Lista todos los archivos en la carpeta y los filtra para obtener solo los archivos .mp4
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.mov')]

# Desordena la lista de archivos para conseguir un orden aleatorio
random.shuffle(files)

# Crea una lista de clips usando la lista de archivos
clips = []
for f in files:
    print(f"Procesando {f}...")
    clip = VideoFileClip(os.path.join(folder_path, f))
    clips.append(clip)

# Concatena los clips
final_clip = concatenate_videoclips(clips, method="compose")

# Exporta el video final
final_clip.write_videofile(os.path.join(folder_path, "video_final.mp4"), codec="libx264", audio_codec="aac")

# Cierra todos los clips para liberar recursos
for clip in clips:
    clip.reader.close()
    clip.audio.reader.close_proc()
