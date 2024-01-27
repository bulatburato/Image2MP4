# Importieren der benötigten Module
import cv2
import numpy as np
import tkinter as tk
import os
from tkinter import filedialog
from PIL import Image, ImageTk

# Erstellen einer GUI-Anwendung mit tkinter
root = tk.Tk()
root.title("Bild zu Video Konverter")

# Erstellen einer Liste, um die ausgewählten Bildpfade zu speichern
image_list = []

# Erstellen einer Funktion, um ein Bild auszuwählen
def select_image():
    # Überprüfen, ob die maximale Anzahl von Bildern erreicht wurde
    if len(image_list) < 200:
        # Öffnen eines Dateiauswahldialogs
        file_path = filedialog.askopenfilename(title="Wählen Sie bis zu max. 200 Bilder nacheinander aus", filetypes=[("Image files", "*.jpg *.png *.bmp")])
        if file_path:
            # Hinzufügen des Bildpfads zur Liste
            image_list.append(file_path)
            # Anzeigen der Bilder in der Liste
            display_images()
    else:
        # Anzeigen einer Nachricht, dass keine weiteren Bilder ausgewählt werden können
        message_label.config(text="Sie können maximal 200 Bilder auswählen!")

# Erstellen einer Funktion, um die Bilder in der Liste anzuzeigen
def display_images():
    # Löschen des Inhalts des Labels
    image_label.config(image="")
    # Erstellen eines leeren Bildes mit der Größe 640x460 Pixel
    canvas = Image.new("RGB", (640, 460))
    # Berechnen der Breite und Höhe jedes Bildes
    width = 640 // len(image_list)
    height = 460
    # Schleife über die Bilder in der Liste
    for i, file_path in enumerate(image_list):
        # Laden des Bildes und Skalieren auf die berechnete Größe
        image = Image.open(file_path)
        image = image.resize((width, height), Image.LANCZOS)
        # Einfügen des Bildes in das leere Bild an der entsprechenden Position
        canvas.paste(image, (i * width, 0))
    # Erstellen eines PhotoImage-Objekts aus dem leeren Bild
    photo = ImageTk.PhotoImage(canvas)
    # Anzeigen des PhotoImage-Objekts im Label
    image_label.config(image=photo)
    image_label.image = photo

# Erstellen einer Funktion, um das Bild in ein Video umzuwandeln
def convert_image():
    # Überprüfen, ob mindestens ein Bild ausgewählt wurde
    if image_list:
        # Lesen der Eingabe des Benutzers für die Länge des Videos in Sekunden
        try:
            video_length = int(length_entry.get())
        except ValueError:
            # Anzeigen einer Fehlermeldung, wenn die Eingabe ungültig ist
            message_label.config(text="Bitte geben Sie eine gültige Zahl für die Länge des Videos ein!")
            return
        # Erstellen eines VideoWriter-Objekts mit dem MP4-Format und der Full HD-Auflösung
        video = cv2.VideoWriter("video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (1920, 1080))
        # Berechnen der Anzahl der Frames pro Bild
        frame_count = video_length * 30 // len(image_list)
        # Schleife über die Bilder in der Liste
        for file_path in image_list:
            # Lesen des Bildes und Ändern der Größe auf 1920x1080 Pixel
            image = cv2.imread(file_path)
            image = cv2.resize(image, (1920, 1080))
            # Hinzufügen des Bildes zum Video für die berechnete Anzahl von Frames
            for i in range(frame_count):
                video.write(image)
        # Freigeben des VideoWriter-Objekts
        video.release()
        # Anzeigen einer Nachricht, dass das Video fertig ist
        message_label.config(text="Ihr Video ist fertig!")
        # Aktivieren des Download-Buttons
        download_button.config(state=tk.NORMAL)
    else:
        # Anzeigen einer Fehlermeldung, wenn kein Bild ausgewählt wurde
        message_label.config(text="Bitte wählen Sie mindestens ein Bild aus!")

# Erstellen einer Funktion, um das Video herunterzuladen
def download_video():
    # Öffnen eines Dateispeicherdialogs
    save_path = filedialog.asksaveasfilename(title="Speichern Sie das Video,Name bitte mit .mp4 eingeben", filetypes=[("MP4 files", "*.mp4")], defaultextension=".mp4")
    if save_path:
        # Kopieren des Videos an den gewählten Speicherort
        with open("video.mp4", "rb") as source:
            with open(save_path, "wb") as destination:
                destination.write(source.read())
        # Anzeigen einer Nachricht, dass das Video heruntergeladen wurde
        message_label.config(text="Ihr Video wurde heruntergeladen!")
        # Löschen des Videos aus dem aktuellen Ordner
        os.remove("video.mp4")

# Erstellen von Widgets für die GUI
image_label = tk.Label(root, text="Kein Bild ausgewählt", width=80, height=40)
select_button = tk.Button(root, text="Bild auswählen", command=select_image)
convert_button = tk.Button(root, text="Bild in Video umwandeln", command=convert_image)
download_button = tk.Button(root, text="Video herunterladen", command=download_video, state=tk.DISABLED)
message_label = tk.Label(root, text="")
height_label = tk.Label(root, text="Höhe des Videos in Pixeln:")
height_entry = tk.Entry(root)
width_label = tk.Label(root, text="Breite des Videos in Pixeln:")
width_entry = tk.Entry(root)
length_label = tk.Label(root, text="Länge des Videos in Sekunden:") # Dies ist das neue Widget für die Länge des Videos
length_entry = tk.Entry(root) # Dies ist das neue Widget für die Länge des Videos

# Anordnen der Widgets in einem Raster
image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
select_button.grid(row=1, column=0, padx=10, pady=10)
convert_button.grid(row=1, column=1, padx=10, pady=10)
download_button.grid(row=1, column=2, padx=10, pady=10)
message_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
height_label.grid(row=3, column=0, padx=10, pady=10)
height_entry.grid(row=3, column=1, padx=10, pady=10)
width_label.grid(row=4, column=0, padx=10, pady=10)
width_entry.grid(row=4, column=1, padx=10, pady=10)
length_label.grid(row=5, column=0, padx=10, pady=10) # Dies ist das neue Widget für die Länge des Videos
length_entry.grid(row=5, column=1, padx=10, pady=10) # Dies ist das neue Widget für die Länge des Videos

# Starten der GUI-Schleife
root.mainloop()
