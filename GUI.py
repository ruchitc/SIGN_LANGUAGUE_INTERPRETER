import tkinter as tk
from tkinter import ttk
from tkVideoPlayer import TkinterVideo
from pathlib import Path
from PIL import Image, ImageTk

import keywords


class VideoPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player App")
        self.root.geometry("800x600")  # Set the initial window size

        # Placeholder image
        self.placeholder_image = tk.PhotoImage(
            file="F:\Automatic-Indian-Sign-Language-Translator-ISL-master\SIGN LANGUAGE INTERPRETER\capa-blogpost-cultura-surda.png"
        )  # Replace with your placeholder image path
        self.image_label = tk.Label(root, image=self.placeholder_image)
        self.image_label.pack(pady=10)

        # Video player frame
        self.video_frame = ttk.Frame(root)
        self.video_frame.pack(expand=True, fill="both")

        # Text box
        self.entry_var = tk.StringVar()
        self.text_entry = ttk.Entry(root, textvariable=self.entry_var)
        self.text_entry.pack(pady=10)

        # Button to play video
        play_button = ttk.Button(root, text="Give Sign Languague", command=self.play_video)
        play_button.pack(pady=10)

        self.video_queue = []

        self.current_player = None

    def play_video(self):
        # Get the video filename based on the entered text
        text = self.entry_var.get()
        video_list = keywords.find_keywords(text)

        self.video_queue.clear()

        for video in video_list:
            video_filename = self.get_video_filename(video)
            if video_filename:
                self.video_queue.append(video_filename)

        self.play_next_video()

        '''
        if video_filename:
            # Load and play the video using tkVideoPlayer
            self.image_label.pack_forget()

            # Load and play the video using tkVideoPlayer in the video frame
            player = TkinterVideo(
                master=self.video_frame, scaled=True, width=800, height=600
            )
            player.load(r"{}".format(video_filename))
            player.pack(expand=True, fill="both")
            player.play()
        '''

    def get_video_filename(self, text):
        # Replace this function with your logic to get the video filename based on the entered text
        # For example, you might query a database to get the filename
        # Here, we'll assume the videos are stored in the "videos" folder with the same name as the entered text
        video_folder = Path("F:/Automatic-Indian-Sign-Language-Translator-ISL-master/SIGN LANGUAGE INTERPRETER/3d dataset")
        video_filename = video_folder / (text + ".mp4")
        #print(str(video_filename))
        if video_filename.is_file():
            return str(video_filename)
        else:
            print(f"Video not found for text: {text}")
            return None

    def play_next_video(self):
        if self.video_queue:
            # Get the next video filename from the queue
            video_filename = self.video_queue.pop(0)

            # Destroy the existing video player if it exists
            if self.current_player:
                self.current_player.destroy()

            # Load and play the video using tkVideoPlayer
            self.image_label.pack_forget()

            # Load and play the video using tkVideoPlayer in the video frame
            player = TkinterVideo(master=self.video_frame, scaled=True, width=800, height=600)
            player.load(r"{}".format(video_filename))
            player.pack(expand=True, fill="both")

            # Set a callback for when the video finishes
            # player.on_end(self.play_next_video)
            player.bind('<<Ended>>', lambda event: self.play_next_video())
            # player.bind('<<Ended>>', lambda event: player.destroy())

            player.play()

            self.current_player = player
        else:
            print("No more videos in the queue.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()

