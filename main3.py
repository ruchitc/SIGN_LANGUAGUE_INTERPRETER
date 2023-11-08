import tkinter as tk
from tkinter import ttkk
import vlc

def play_video(video_file):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(video_file)
    media.get_mrl()
    player.set_media(media)

    # Create a tkinter window to display the video
    root = tk.Tk()
    root.geometry("640x480")
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Create a vlc player widget and add it to the tkinter window
    player.set_hwnd(frame.winfo_id())
    player.play()

    # Run the tkinter main loop to display the video
    root.mainloop()

def func():
    r = sr.Recognizer()
    # Define your list of MP4 video files here

    while True:
        # Your code to recognize speech and determine the sign language phrase goes here

        if a.lower() in isl_mp4:
            video_file = 'ISL_Videos/{}.mp4'.format(a.lower())
            play_video(video_file)
        else:
            # Handle displaying images for individual letters here

def main():
    while True:
        image ="capa-blogpost-cultura-surda.png"
        msg = "SIGN LANGUAGE INTERPRETER"
        choices = ["Live Voice", "Text Input", "Hindi Text Input", "All Done!"]
        reply = buttonbox(msg, image=image, choices=choices)

        if reply == "Live Voice":
            func()

        elif reply == "Hindi Text Input":
            text_input = enterbox("Enter the Hindi Text:")
            if text_input:
                mihir = translate_hindi_to_english(text_input)
                text_to_image(mihir)

        elif reply == "Text Input":
            text_input = enterbox("Enter the text:")
            if text_input:
                text_input = text_input.lower()
                text_to_image(text_input)


        elif reply == "All Done!":
            quit()

if __name__ == "__main__":
    main()
