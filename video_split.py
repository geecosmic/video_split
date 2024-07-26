import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import math
import os

# Function to split the video
def split_video(input_file, segment_duration=59):
    # Get the duration of the video
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    duration = float(result.stdout)

    # Calculate the number of segments
    num_segments = math.ceil(duration / segment_duration)

    # Split the video
    for i in range(num_segments):
        start_time = i * segment_duration
        output_file = f"{os.path.splitext(input_file)[0]}_part_{i+1}.mp4"
        subprocess.run(['ffmpeg', '-i', input_file, '-ss', str(start_time), '-t', str(segment_duration), '-c', 'copy', output_file])

    messagebox.showinfo("Success", f"Video split into {num_segments} segments.")

# Function to select video file
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

# Function to start the splitting process
def start_split():
    input_file = file_entry.get()
    if os.path.isfile(input_file):
        split_video(input_file)
    else:
        messagebox.showerror("Error", "Please select a valid video file.")

# Create the main window
app = ctk.CTk()

# Set window title and size
app.title("Video Splitter")
app.geometry("400x200")

# Create and place widgets
file_label = ctk.CTkLabel(app, text="Select Video File:")
file_label.pack(pady=10)

file_entry = ctk.CTkEntry(app, placeholder_text="Enter or select a video file")
file_entry.pack(pady=5, padx=20, fill=tk.X)

browse_button = ctk.CTkButton(app, text="Browse", command=browse_file)
browse_button.pack(pady=5)

split_button = ctk.CTkButton(app, text="Split Video", command=start_split)
split_button.pack(pady=20)

# Run the application
app.mainloop()
