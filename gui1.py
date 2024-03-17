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
        self.root.geometry("800x600")  # Set the initial window size

        # Placeholder image
        self.placeholder_image = tk.PhotoImage(
            file="C:\\Users\\ruchi\\Code\\SignLanguageInterpreter\\SIGN_LANGUAGUE_INTERPRETER\\capa-blogpost-cultura-surda.png"
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

        # Text widget to display the entered text
        self.text_display = tk.Text(root, state="disabled", wrap="word", height=3, font=("Helvetica", 14, "bold"))
        self.text_display.pack(pady=5)
        self.text_display.tag_config('available', foreground='green')
        self.text_display.tag_config('unavailable', foreground='red')

        # Create a frame for buttons
        self.button_frame = ttk.Frame(root)
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
        self.current_player = None

    def play_video(self):
        # Get the video filename based on the entered text
        text = self.entry_var.get()
        input_words = text.split(' ')
        video_list = keywords.find_keywords(text)

        self.video_queue.clear()

        for video in video_list:
            video_filename = self.get_video_filename(video)
            if video_filename:
                self.video_queue.append((video_filename, video))

        self.text_display.config(state='normal')
        self.text_display.delete(1.0, tk.END)
        for word in input_words:
            if word in video_list:
                self.text_display.insert(tk.END, f"{word} ", 'available')
            else:
                self.text_display.insert(tk.END, f"{word} ", 'unavailable')
        self.text_display.config(state='disabled')

        self.play_next_video()

    def get_video_filename(self, text):
        # Replace this function with your logic to get the video filename based on the entered text
        # For example, you might query a database to get the filename
        # Here, we'll assume the videos are stored in the "videos" folder with the same name as the entered text
        video_folder = Path(
            "C:\\Users\\ruchi\\Code\\SignLanguageInterpreter\\SIGN_LANGUAGUE_INTERPRETER\\trimmed_new")
        video_filename = video_folder / (text + ".mp4")
        if video_filename.is_file():
            return str(video_filename)
        else:
            print(f"Video not found for text: {text}")
            return None

    def play_next_video(self):
        if self.video_queue:
            # Get the next video filename and associated text from the queue
            video_filename, video_text = self.video_queue.pop(0)

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
            player.bind('<<Ended>>', lambda event: self.play_next_video())

            player.play()

            # Update the text widget with the entered text
            # self.text_display.delete(1.0, tk.END)
            # self.text_display.insert(tk.END, f"Text: {video_text}", "green")

            self.current_player = player
            # Decrease the delay between videos (adjust the value in milliseconds)
            self.root.after(2000, self.play_next_video)  # Set the delay here (in milliseconds)
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
                self.video_queue.append((video_filename, video))

        # Highlight words in the text widget based on their presence in the video_list
        self.play_next_video()


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()
