import customtkinter as ctk
from customtkinter import *
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading, time, os

# Paths for icons and images
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
search_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "search.png")), size=(41, 39))
logo_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(60, 60))
like_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "like_empty.png")), size=(25, 25))
dislike_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "dislike_empty.png")), size=(25, 25))
like_icon2 = ctk.CTkImage(Image.open(os.path.join(image_path, "like_filled.png")), size=(25, 25))
dislike_icon2 = ctk.CTkImage(Image.open(os.path.join(image_path, "dislike_filled.png")), size=(25, 25))
save_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "download.png")), size=(25, 25))
close_icon = ctk.CTkImage(Image.open(os.path.join(image_path, "close.png")), size=(25, 25))

# Function to fetch and display the image
def fetch_and_display_image(image_url):
    like_button.configure(image=like_icon)
    dislike_button.configure(image=dislike_icon)
    try:
        progressbar.set(0)
        progressbar.start()
        time.sleep(0.5)  # Small delay for natural loading feel

        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((700, 600), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(img)

        # Update UI after loading
        image_label.configure(image=tk_image)
        image_label.image = tk_image

        button_frame.pack(side=BOTTOM, fill=X)

        error_label.configure(text="")
    except requests.exceptions.RequestException as e:
        error_label.configure(text=f"Error loading image: {e}")
    finally:
        progressbar.stop()
        progressbar.set(100)  # Fill progress bar to 100%
        time.sleep(0.5)
        progressbar.set(0)  # Reset progress bar after a short delay

# Function to start image fetching in a separate thread
def search_image():
    query = search_entry.get().strip()
    if query:
        threading.Thread(target=fetch_and_display_image, args=(query,), daemon=True).start()

# Function to handle like/dislike actions
def like_dislike(name):
    if name == "like_icon":
        like_button.configure(image=like_icon2)
        dislike_button.configure(image=dislike_icon)
        threading.Thread(target=feedback).start()
    
    if name == "dislike_icon":
        like_button.configure(image=like_icon)
        dislike_button.configure(image=dislike_icon2)
    
def feedback():
    feedback_frame = CTkFrame(root, fg_color="#111", corner_radius=10)
    feedback_text = ctk.CTkLabel(feedback_frame, text="Thanks for your feedback!", font=("monospace", 20), fg_color="#111")
    feedback_text.pack(padx=10, pady=10)
    
    feedback_frame.pack(side=TOP, pady=(20, 0))  

    time.sleep(2)
    feedback_frame.pack_forget()

# Function to save the displayed image
def save_image():
    if image_label.image:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", 
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            try:
                img = ImageTk.getimage(image_label.image)
                img.save(file_path)
                print(f"Image saved to {file_path}")
                success_feedback()
            except Exception as e:
                print(f"Error saving image: {e}")

# Function to show success feedback
def success_feedback():
    feedback_frame = CTkFrame(root, fg_color="#111", corner_radius=10)
    feedback_text = ctk.CTkLabel(feedback_frame, text="Image saved successfully!", font=("monospace", 20), fg_color="#111")
    feedback_text.pack(padx=10, pady=10)
    
    feedback_frame.pack(side=TOP, pady=(20, 0))  

    time.sleep(2)
    feedback_frame.pack_forget()

# Window setup
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Online Image Viewer")
root.geometry("800x600")
root.iconbitmap("images\\logo.ico")

# Navigation frame (top)
nav_frame = ctk.CTkFrame(root, fg_color="transparent")
nav_frame.pack(side=TOP, anchor="nw", padx=20, pady=5, fill=X, expand=True)

logo_label = ctk.CTkLabel(nav_frame, text="", image=logo_icon, fg_color="transparent")
logo_label.pack(side=LEFT)

search_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
search_frame.pack(side=RIGHT, fill=X, padx=10, expand=True)

search_entry = ctk.CTkEntry(search_frame, width=100, height=45, placeholder_text="Enter Image URL...", corner_radius=10, border_color="#222", font=("monospace", 14))
search_entry.pack(side=LEFT, fill=X, expand=True)

search_button = ctk.CTkButton(search_frame, text="", command=search_image, image=search_icon, width=0, fg_color="transparent", hover_color="#333")
search_button.pack(padx=4)

# Image display area (centered and aligned at the top)
image_frame = ctk.CTkFrame(root, fg_color="transparent")

image_label = ctk.CTkLabel(image_frame, text="")
image_label.pack(side=TOP)

button_frame = CTkFrame(image_frame, fg_color="transparent")
save_button = ctk.CTkButton(button_frame, text="", image=save_icon, fg_color="transparent", hover_color="#111", width=10, command=save_image)
save_button.pack(side=RIGHT, pady=5, ipadx=2, ipady=2)

like_button = ctk.CTkButton(button_frame, text="", image=like_icon, fg_color="transparent", hover_color="#111", width=10, command=lambda: like_dislike("like_icon"))
like_button.pack(side=LEFT, pady=5, ipadx=2, ipady=2)

dislike_button = ctk.CTkButton(button_frame, text="", image=dislike_icon, fg_color="transparent", hover_color="#111", width=10, command=lambda: like_dislike("dislike_icon"))
dislike_button.pack(side=LEFT, pady=5, ipadx=2, ipady=2)

#button_frame.pack()
# 👇 Fix: Align the image frame to the top!
image_frame.pack(side=TOP, pady=(10, 0))

# Progress bar
progressbar = ctk.CTkProgressBar(root, orientation="horizontal", mode="determinate", determinate_speed=1, fg_color="#222", height=5, progress_color="#e74f4b", corner_radius=0)
progressbar.set(0)
progressbar.pack(fill="x", side="bottom")

# Error label
error_label = ctk.CTkLabel(root, text="", text_color="white")
error_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()

# Test URL: https://www.worldatlas.com/r/w1200/upload/13/56/41/shutterstock-200702498.jpg
