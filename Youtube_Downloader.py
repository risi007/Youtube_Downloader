import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
import asyncio
import threading
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import customtkinter

@lru_cache(maxsize=None)  # Cache results indefinitely
def fetch_video_info(url):
    try:
        yt = YouTube(url)
        return yt.title
    except Exception as e:
        return f"Error fetching title: {str(e)}"

async def fetch_video_info_async(url):
    try:
        yt = YouTube(url)
        return yt.title
    except Exception as e:
        return f"Error fetching title: {str(e)}"

async def download_video_async(url, itag, output_folder):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.get_by_itag(itag)
        if stream:
            stream.download(output_folder)
            messagebox.showinfo("Download Complete", "Video downloaded successfully.")
        else:
            messagebox.showerror("Error", "No suitable stream found for download.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def update_title_async(event=None):
    url = url_entry.get()
    title = asyncio.run(fetch_video_info_async(url))
    title_label.configure(text=f"Video Title: {title}")

def run_download_async():
    url = url_entry.get()
    itag = itag_combobox.get().split()[0]
    output_folder = output_folder_label.cget("text").replace("Output Folder: ", "")
    threading.Thread(target=asyncio.run, args=(download_video_async(url, itag, output_folder),)).start()

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent_complete = (bytes_downloaded / total_size) * 100
    per = str(int(percent_complete))
    pPercentage.configure(text=per + '%')
    pPercentage.update()
    progress_bar.set(float(percent_complete) / 100)

def choose_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory()
    output_folder_label.configure(text=f"Output Folder: {output_folder}")

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# Create the main window
root = customtkinter.CTk()
root.geometry("720x480")
root.title("YouTube Video Downloader")

# Create a label to display the video title
title_label = customtkinter.CTkLabel(root, text="")
title_label.pack(padx=10, pady=(10, 5))  # Increased vertical padding for separation

# Create a label and an entry field for the YouTube URL
url_label = customtkinter.CTkLabel(root, text="Enter YouTube URL:")
url_label.pack(padx=10, pady=5, anchor="w")

url_entry = customtkinter.CTkEntry(root, width=400)
url_entry.pack(padx=10, pady=5)

url_entry.bind("<KeyRelease>", update_title_async)

# Create a label and a Combobox for selecting the video quality (itag)
itag_label = customtkinter.CTkLabel(root, text="Select Video Quality:")
itag_label.pack(padx=10, pady=5, anchor="w")

itag_combobox = customtkinter.CTkComboBox(root, values=["18 (360p)", "22 (720p)"])
itag_combobox.pack(padx=10, pady=5)

itag_combobox.set("22 (720p)")

# Create a button to choose the output folder
output_folder_button = customtkinter.CTkButton(root, text="Choose Output Folder", command=choose_output_folder)
output_folder_button.pack(padx=10, pady=5, anchor="w")

# Create a label to display the selected output folder
output_folder_label = customtkinter.CTkLabel(root, text="Output Folder: None")
output_folder_label.pack(padx=10, pady=5, anchor="w")

pPercentage = customtkinter.CTkLabel(root, text='0%')
pPercentage.pack(padx=10, pady=(5, 10))  # Increased vertical padding for separation

# Create a label for download progress
progress_bar = customtkinter.CTkProgressBar(root, width=300)
progress_bar.set(0)
progress_bar.pack(padx=10, pady=(0, 10))  # Increased vertical padding for separation

# Create a download button
download_button = customtkinter.CTkButton(root, text="Download Video", command=run_download_async)
download_button.pack(padx=10, pady=10)

# Start the GUI main loop
root.mainloop()
