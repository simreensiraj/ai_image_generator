# AI_image_generator
A simple AI image generator using stable diffusion.

Honestly, I'd have used the Open-AI Dall-E API to make this project, which would have been faster and simpler. However, since it uses tokens, the project would not be free and accessible to everyone. So I had to resort to a slower version of the program by using stable diffusers. I'd try making edits and changes to the code to make it faster, but till then this is the base code for it

I used HuggingFace & NVIDIA's CUDA to create this fairly simple program.

Before running it, go to cmd and install the required modules -
> pip install torch transformers diffusers Pillow

Plain.py gives a program without a GUI, kinda faster because of it. Main.py gives a sleek simple gui through which the user can interact.

![image](https://github.com/user-attachments/assets/2fb456eb-fc61-40b1-89fb-3f15606db7fa)


Moreover, do download the NVIDIA CUDA GPU for faster image processing.
If you don't have a GPU, it's totally fine, the program will just take slightly longer to work.

Once that's done, just run the code and you're all good!
