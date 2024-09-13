import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from PIL import Image

def load_model():
    # Load the stable diffusion model (ensure you have enough GPU/CPU resources)
    model_id = "CompVis/stable-diffusion-v1-4"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to(device)
    return pipe

def generate_image(prompt, pipe, output_path="generated_image.png"):
    # Generate the image
    with autocast("cuda"):
        image = pipe(prompt).images[0]
    
    # Save the image
    image.save(output_path)
    print(f"Image saved at {output_path}")
    image.show()

def main():
    # Load the model
    pipe = load_model()

    print("Welcome to the AI Image Generator!")
    while True:
        # Get the text prompt from the user
        prompt = input("Enter the prompt for the image (or type 'exit' to quit): ")
        if prompt.lower() == "exit":
            print("Exiting the program.")
            break

        # Generate and save the image
        generate_image(prompt, pipe)

if __name__ == "__main__":
    main()
