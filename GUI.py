import tkinter as tk
from tkinter import ttk
from tkVideoPlayer import TkinterVideo
from pathlib import Path

import keywords
from translate import Translator
import speech_recognition as sr
import threading


class VideoPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player App")
        self.root.geometry("1000x600")  # Adjust the initial window size

        # Create a frame for the left and right sections
        self.left_frame = ttk.Frame(root)
        self.left_frame.pack(side="left", padx=10)

        self.right_frame = ttk.Frame(root)
        self.right_frame.pack(side="left", expand=True, fill="both", padx=10)

        # Left Panel (Preview)
        self.preview_frame = ttk.Frame(self.left_frame, width=200, height=150)
        self.preview_frame.pack(expand=True, fill="both", pady=10)

        # Placeholder image for preview
        self.preview_image = tk.PhotoImage(
            file="F:\Automatic-Indian-Sign-Language-Translator-ISL-master\SIGN LANGUAGE INTERPRETER\capa-blogpost-cultura-surda.png"
        )  # Replace with your placeholder image path
        self.preview_label = tk.Label(self.preview_frame, image=self.preview_image)
        self.preview_label.pack(pady=10)

        # Right Panel (Video Player)
        self.video_frame = ttk.Frame(self.right_frame)
        self.video_frame.pack(expand=True, fill="both")

        # Text box
        self.entry_var = tk.StringVar()
        self.text_entry = ttk.Entry(self.right_frame, textvariable=self.entry_var)
        self.text_entry.pack(pady=10)

        # Label to display the entered text
        self.text_label = tk.Label(self.right_frame, text="", font=("Helvetica", 14, "bold"))
        self.text_label.pack(pady=5)

        # Create a frame for buttons
        self.button_frame = ttk.Frame(self.right_frame)
        self.button_frame.pack(pady=10)

        # Button to play video
        play_button = ttk.Button(self.button_frame, text="Give Sign Language", command=self.play_video)
        play_button.pack(side="left", padx=5)

        # Button to translate from Hindi to English
        translate_button = ttk.Button(self.button_frame, text="give Hindi Input", command=self.translate_to_english)
        translate_button.pack(side="left", padx=5)

        # Button to input voice in English
        voice_button = ttk.Button(self.button_frame, text="Input Voice in English", command=self.input_voice)
        voice_button.pack(side="left", padx=5)

        self.video_queue = []
        self.current_player_left = None
        self.current_player_right = None

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

    def get_video_filename(self, text):
        # Replace this function with your logic to get the video filename based on the entered text
        # For example, you might query a database to get the filename
        # Here, we'll assume the videos are stored in the "videos" folder with the same name as the entered text
        video_folder = Path(
            "F:/Automatic-Indian-Sign-Language-Translator-ISL-master/SIGN LANGUAGE INTERPRETER/3d dataset")
        video_filename = video_folder / (text + ".mp4")
        if video_filename.is_file():
            return str(video_filename)
        else:
            print(f"Video not found for text: {text}")
            return None

    def play_next_video(self):
        if self.video_queue:
            # Get the next video filename from the queue
            video_filename = self.video_queue.pop(0)

            # Destroy the existing video players if they exist
            if self.current_player_left:
                self.current_player_left.destroy()
            if self.current_player_right:
                self.current_player_right.destroy()

            # Load and play the video using tkVideoPlayer in the preview frame (left)
            self.preview_label.pack_forget()
            player_left = TkinterVideo(master=self.preview_frame, scaled=True, width=200, height=150)
            player_left.load(r"{}".format(video_filename))
            player_left.pack(expand=True, fill="both")
            player_left.play()

            # Load and play the video using tkVideoPlayer in the main frame (right)
            player_right = TkinterVideo(master=self.video_frame, scaled=True, width=800, height=600)
            player_right.load(r"{}".format(video_filename))
            player_right.pack(expand=True, fill="both")
            player_right.play()

            # Set a callback for when the video finishes
            player_left.bind('<<Ended>>', lambda event: self.play_next_video())
            player_right.bind('<<Ended>>', lambda event: self.play_next_video())

            self.current_player_left = player_left
            self.current_player_right = player_right

        else:
            print("No more videos in the queue.")

    def translate_to_english(self):
        # Translate the entered Hindi text to English
        hindi_text = self.entry_var.get()
        translator = Translator(to_lang="en", from_lang="hi")
        english_text = translator.translate(hindi_text)

        # Update the entry field with the translated text
        self.entry_var.set(english_text)

        # Play the sign language video for the translated text
        self.play_video_for_text(english_text)

    def play_translated_video(self):
        # Play sign language video based on translated English text
        english_text = self.entry_var.get()
        self.play_video_for_text(english_text)

    def input_voice(self):
        # Define a separate thread for voice recognition
        voice_thread = threading.Thread(target=self.perform_voice_recognition)

        # Start the thread
        voice_thread.start()

    def perform_voice_recognition(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Speak something...")
            audio = recognizer.listen(source)

        try:
            # Recognize the voice input
            english_text = recognizer.recognize_google(audio)
            print(f"You said: {english_text}")

            # Set the recognized text in the entry field
            self.entry_var.set(english_text)

            # Play the sign language video for the recognized English text
            self.play_video_for_text(english_text)

        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")

    def play_video_for_text(self, text):
        # Play the sign language video for the given English text
        video_list = keywords.find_keywords(text)

        self.video_queue.clear()

        for video in video_list:
            video_filename = self.get_video_filename(video)
            if video_filename:
                self.video_queue.append(video_filename)

        self.play_next_video()


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()
