import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from faker import Faker

class TypingTestGame:
    def __init__(self):
        self.faker = Faker()
        self.time = 10  # Set the initial time
        self.timer_started = False
        self.game_done = False
        self.entered_chars = []  # List to store entered characters
        self.correct_words = []  # List to store correctly entered words

        self.main_window = tk.Tk()
        self.main_window.title("Typing Test Game")
        self.main_window.resizable(False, False)

        self.create_widgets()

        self.cbo_time.bind("<<ComboboxSelected>>", self.cbo_time_ComboboxSelected)
        self.txt_user_word.bind("<KeyPress>", self.txt_user_word_KeyPress)
        self.txt_user_word.bind("<KeyRelease>", self.txt_user_word_KeyRelease)
        self.btn_replay.bind("<Button-1>", self.btn_replay_Button_1)

    def create_widgets(self):
        self.random_words = [self.faker.word() for _ in range(5)]
        
        self.lbl_random_words = ttk.Label(self.main_window, text=" ".join(self.random_words))
        self.txt_user_word = ttk.Entry(self.main_window)
        self.lbl_timer = ttk.Label(self.main_window, text=f"Time: {self.time}s")

        # Create a Combobox for selecting the time
        self.cbo_time = ttk.Combobox(self.main_window, values=["10s", "30s", "60s"], state="readonly")
        self.cbo_time.set("10s")  # Set the default value

        # Create a replay button
        self.btn_replay = ttk.Button(self.main_window, text="Replay")

        self.lbl_random_words.grid(row=0, column=0, padx=5, pady=5)
        self.txt_user_word.grid(row=1, column=0, padx=5, pady=5)
        self.lbl_timer.grid(row=2, column=0, padx=5, pady=5)
        self.cbo_time.grid(row=3, column=0, padx=5, pady=5)  # Add the Combobox to the grid
        self.btn_replay.grid(row=4, column=0, padx=5, pady=5)  # Add the replay button to the grid

    def cbo_time_ComboboxSelected(self, event):
        self.lbl_timer['text'] = f"Time: {self.cbo_time.get()}"
        self.time = int(self.cbo_time.get()[:-1])

    def txt_user_word_KeyRelease(self, event):
        user_sequence = self.txt_user_word.get().strip()
        if TypingTestGame.compare_tying_word(user_sequence, self.random_words[0]):
            self.lbl_random_words.config(foreground="black")
        else:
            self.lbl_random_words.config(foreground="red")

        if event.char == ' ' and user_sequence == self.random_words[0]:
            self.correct_words.append(self.random_words[0])
            self.random_words.pop(0)
            self.random_words.append(self.faker.word())
            self.lbl_random_words.config(text=" ".join(self.random_words))
            self.txt_user_word.delete(0, tk.END)  # Clear the input after processing
        
        self.entered_chars.append(event.char)

    @staticmethod
    def compare_tying_word(user_sequence, right_word):
        if len(user_sequence) == 0:
            return True
        return user_sequence == right_word[:len(user_sequence)]

    def txt_user_word_KeyPress(self, event):
        if not self.timer_started:
            self.timer_started = True
            self.cbo_time.config(state="disable")
            self.countdown()

    def countdown(self):
        if self.time > 0 and self.timer_started:
            self.time -= 1
            self.lbl_timer.config(text=f"Time: {self.time}s")
            self.main_window.after(1000, self.countdown)  # Update the timer every 1000ms (1 second)
        elif self.time == 0 or self.game_done:
            self.txt_user_word.config(state='disabled')  # Disable the textbox
            num_correct_words, wpm, accuracy = self.calculate_metrics()
            showinfo(message=f"Correct Word Number: {num_correct_words}\nWords Per Minute: {wpm}\nTyping Accuracy: {accuracy}%")
            self.game_done = True
            self.cbo_time.config(state="readonly")
            

    def calculate_accuracy(self):
        correct_characters = list(" ".join(self.correct_words))
        return len(correct_characters) / len(self.entered_chars[:-1]) # exclude the last space character

    def calculate_wpm(self):
        num_correct_words = len(self.correct_words)
        return num_correct_words * 60 / (int(self.cbo_time.get()[:-1]) - self.time)

    def calculate_metrics(self):
        num_correct_words = len(self.correct_words)

        # Calculate Words Per Minute (WPM)
        wpm = self.calculate_wpm()

        # Calculate Typing Accuracy
        accuracy = self.calculate_accuracy() * 100

        return num_correct_words, wpm, accuracy

    def btn_replay_Button_1(self, event):
        self.random_words = [self.faker.word() for _ in range(5)]
        self.time = int(self.cbo_time.get()[:-1])
        self.timer_started = False
        self.entered_chars = []
        self.correct_words = []
        self.lbl_random_words.config(text=" ".join(self.random_words))
        self.lbl_timer.config(text=f"Time: {self.time}s")
        self.txt_user_word.config(state='normal')
        self.txt_user_word.delete(0, tk.END)
        self.game_done = False
        self.cbo_time.config(state="readonly")

    def run(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    game = TypingTestGame()
    game.run()
