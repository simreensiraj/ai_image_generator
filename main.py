import warnings
import customtkinter as ctk
from tkinter import filedialog, messagebox
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageTk
import threading

# Suppress transformers future warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")

# Function to load the model
def load_model():
    model_id = "CompVis/stable-diffusion-v1-4"
    # Choose float16 if CUDA is available, otherwise float32
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load pipeline with appropriate dtype
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=dtype)
    pipe = pipe.to(device)
    return pipe, device

# Function to generate image based on prompt
def generate_image(prompt, pipe, device):
    try:
        if device == "cuda":
            with autocast("cuda"):
                image = pipe(prompt).images[0]
        else:
            image = pipe(prompt).images[0]
        return image
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", "Failed to generate image.")
        return None

# Function to handle image generation and display (runs on a separate thread)
def handle_generate():
    prompt = prompt_entry.get()
    if not prompt:
        messagebox.showwarning("Input Error", "Please enter a prompt.")
        return
    
    # Run image generation in a new thread to avoid freezing the GUI
    threading.Thread(target=generate_and_display_image, args=(prompt,)).start()

# Separate function to generate and display the image (used in the thread)
def generate_and_display_image(prompt):
    image = generate_image(prompt, model_pipe, device)
    if image:
        # Save the generated image
        image.save("generated_image.png")
        
        # Display the generated image in the GUI
        img = ImageTk.PhotoImage(image.resize((256, 256)))
        image_label.configure(image=img)
        image_label.image = img  # Store the reference to the image

# Function to save the generated image
def save_image():
    try:
        if image_label.image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                image_label.image._PhotoImage__photo.write(save_path)
                messagebox.showinfo("Success", f"Image saved at {save_path}")
        else:
            messagebox.showwarning("No Image", "No image to save.")
    except AttributeError:
        messagebox.showwarning("No Image", "No image has been generated to save.")

# Load the model at the start
model_pipe, device = load_model()

# Configure the main window with customTkinter
ctk.set_appearance_mode("dark")  # Set dark mode
ctk.set_default_color_theme("dark-blue")  # Optional: Use a different color theme

app = ctk.CTk()
app.title("AI Image Generator")
app.geometry("500x500")

# Add a label and entry for the text prompt
prompt_label = ctk.CTkLabel(app, text="Enter your prompt:", font=("Arial", 14))
prompt_label.pack(pady=20)

prompt_entry = ctk.CTkEntry(app, width=400, height=40, placeholder_text="Type your image prompt here")
prompt_entry.pack(pady=10)

# Button to generate the image
generate_button = ctk.CTkButton(app, text="Generate Image", command=handle_generate, width=200, height=40)
generate_button.pack(pady=20)

# Label to display the generated image
image_label = ctk.CTkLabel(app, text="")
image_label.pack(pady=20)

# Button to save the generated image
save_button = ctk.CTkButton(app, text="Save Image", command=save_image, width=150, height=40)
save_button.pack(pady=10)

# Start the Tkinter event loop
app.mainloop()
