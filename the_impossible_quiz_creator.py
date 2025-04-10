# Author: Israfil Palabay
# The Impossible Quiz Creator
# April 10, 2025

import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import os
import webbrowser
from PIL import Image, ImageTk
import json

class ImpossibleQuizCreator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("The Impossible Quiz Creator")
        self.root.geometry("800x600")
        
        # Initialize pygame mixer for sound
        pygame.mixer.init()
        
        # Colors
        self.colors = {
            'baby_power': '#FDFFFC',
            'lapis_lazuli': '#235789',
            'fire_engine_red': '#C1292E',
            'school_bus_yellow': '#F1D302',
            'raisin_black': '#161925'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['baby_power'])
        
        # Load start button image
        start_img = Image.open("begin_interface.jpg")
        start_img = start_img.resize((200, 100), Image.Resampling.LANCZOS)
        self.start_photo = ImageTk.PhotoImage(start_img)
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=self.colors['baby_power'])
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Center frame for start button
        self.start_frame = tk.Frame(self.main_frame, bg=self.colors['baby_power'])
        self.start_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Start button
        self.start_button = tk.Button(
            self.start_frame,
            image=self.start_photo,
            command=self.start_quiz_creator,
            borderwidth=0
        )
        self.start_button.pack()
        
        # Create quiz creator frame (initially hidden)
        self.quiz_frame = tk.Frame(self.main_frame, bg=self.colors['baby_power'])
        
        # Load sounds
        self.fart_sound = os.path.join(os.path.dirname(__file__), "quick_reverb_fart_sound_effect.mp3")
        self.zipper_sound = os.path.join(os.path.dirname(__file__), "zipper_sound_effect.mp3")
        self.explosion_sound = os.path.join(os.path.dirname(__file__), "explosion_effect_sound.mp3")
        self.ding_sound = os.path.join(os.path.dirname(__file__), "ding_sound_effect.mp3")
        self.rick_roll_sound = os.path.join(os.path.dirname(__file__), "rick_astley_never_gonna_give_you_up_instrumental.mp3")
        self.mars_sings_sound = os.path.join(os.path.dirname(__file__), "what_is_the_light_by_the_flaming_lips.mp3")
        self.epic_10_music_sound = os.path.join(os.path.dirname(__file__), "miserlou_by_dick_dale.mp3")
        self.question_84_music_sound = os.path.join(os.path.dirname(__file__), "star_wars_cantina_remix.mp3")
        self.quiz_music_2_sound = os.path.join(os.path.dirname(__file__), "the_yeah_yeah_yeah_song_instrumental.mp3")
        self.quiz_music_1_sound = os.path.join(os.path.dirname(__file__), "rocky_theme.mp3")
        self.title_music_sound = os.path.join(os.path.dirname(__file__), "boombots_bonus_song_by_terry_taylor.mp3")
    
    def start_quiz_creator(self):
        # Play fart sound
        pygame.mixer.music.load(self.fart_sound)
        pygame.mixer.music.play()
        
        # Hide start button and show quiz creator
        self.start_button.pack_forget()
        self.start_frame.place_forget()
        self.quiz_frame.pack(expand=True, fill='both')
        
        # Show quiz creator interface
        self.create_quiz_interface()
    
    def create_quiz_interface(self):
        # Username entry
        username_frame = tk.Frame(self.quiz_frame, bg=self.colors['baby_power'])
        username_frame.pack(pady=10)
        
        username_label = tk.Label(
            username_frame,
            text="Enter your username:",
            font=('Comica', 12),
            bg=self.colors['baby_power'],
            fg=self.colors['lapis_lazuli']
        )
        username_label.pack(side='left', padx=5)
        
        self.username_entry = tk.Entry(username_frame, font=('Comica', 12))
        self.username_entry.pack(side='left', padx=5)
        
        # Question entry
        question_frame = tk.Frame(self.quiz_frame, bg=self.colors['baby_power'])
        question_frame.pack(pady=10)
        
        question_label = tk.Label(
            question_frame,
            text="Enter your question:",
            font=('Comica', 12),
            bg=self.colors['baby_power'],
            fg=self.colors['lapis_lazuli']
        )
        question_label.pack()
        
        self.question_entry = tk.Text(question_frame, height=3, width=50, font=('Comica', 12))
        self.question_entry.pack(pady=5)
        
        # Answer choices
        answers_frame = tk.Frame(self.quiz_frame, bg=self.colors['baby_power'])
        answers_frame.pack(pady=10)
        
        self.answer_entries = {}
        for choice in ['a', 'b', 'c', 'd']:
            frame = tk.Frame(answers_frame, bg=self.colors['baby_power'])
            frame.pack(pady=5)
            
            label = tk.Label(
                frame,
                text=f"Choice {choice.upper()}:",
                font=('Comica', 12),
                bg=self.colors['baby_power'],
                fg=self.colors['lapis_lazuli']
            )
            label.pack(side='left', padx=5)
            
            entry = tk.Entry(frame, width=40, font=('Comica', 12))
            entry.pack(side='left', padx=5)
            self.answer_entries[choice] = entry
        
        # Correct answer selection
        correct_answer_frame = tk.Frame(self.quiz_frame, bg=self.colors['baby_power'])
        correct_answer_frame.pack(pady=10)
        
        correct_label = tk.Label(
            correct_answer_frame,
            text="Select correct answer:",
            font=('Comica', 12),
            bg=self.colors['baby_power'],
            fg=self.colors['lapis_lazuli']
        )
        correct_label.pack(side='left', padx=5)
        
        self.correct_answer = tk.StringVar()
        for choice in ['a', 'b', 'c', 'd']:
            rb = tk.Radiobutton(
                correct_answer_frame,
                text=choice.upper(),
                variable=self.correct_answer,
                value=choice,
                font=('Comica', 12),
                bg=self.colors['baby_power'],
                fg=self.colors['lapis_lazuli']
            )
            rb.pack(side='left', padx=10)
        
        # Buttons
        buttons_frame = tk.Frame(self.quiz_frame, bg=self.colors['baby_power'])
        buttons_frame.pack(pady=20)
        
        # Save button
        save_button = tk.Button(
            buttons_frame,
            text="Save Question",
            command=self.save_question,
            font=('Comica', 12),
            bg=self.colors['school_bus_yellow'],
            fg=self.colors['raisin_black']
        )
        save_button.pack(side='left', padx=10)
        
        # Instructions button
        instructions_button = tk.Button(
            buttons_frame,
            text="Instructions",
            command=self.show_instructions,
            font=('Comica', 12),
            bg=self.colors['lapis_lazuli'],
            fg=self.colors['baby_power']
        )
        instructions_button.pack(side='left', padx=10)
        
        # GitHub button
        github_button = tk.Button(
            buttons_frame,
            text="ISRAFILMATTER'S GITHUB",
            command=self.open_github,
            font=('Comica', 12),
            bg=self.colors['fire_engine_red'],
            fg=self.colors['baby_power']
        )
        github_button.pack(side='left', padx=10)
    
    def show_instructions(self):
        instructions = """
INSTRUCTIONS:
Enter your quiz questions and answers carefully.
Each question must have exactly 4 choices (a, b, c, d).
Select the correct answer for each question.
Click 'Save Question' to save your question.
Continue adding questions until you're done.
        """
        messagebox.showinfo("Instructions", instructions)
    
    def open_github(self):
        webbrowser.open("https://github.com/IsrafilMatter")
    
    def save_question(self):
        username = self.username_entry.get()
        question = self.question_entry.get("1.0", tk.END).strip()
        answers = {k: v.get() for k, v in self.answer_entries.items()}
        correct = self.correct_answer.get()
        
        if not all([username, question, all(answers.values()), correct]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        # Save to file
        with open("quiz_data.txt", "a") as f:
            f.write(f"Q: {question}\n")
            for choice, answer in answers.items():
                f.write(f"{choice.upper()}: {answer}\n")
            f.write(f"ANSWER: {correct}\n")
            f.write("---\n")
        
        # Clear fields
        self.question_entry.delete("1.0", tk.END)
        for entry in self.answer_entries.values():
            entry.delete(0, tk.END)
        self.correct_answer.set("")
        
        # Ask if user wants to continue
        if messagebox.askyesno("Continue?", "Do you want to add another question?"):
            self.question_entry.focus()
        else:
            self.root.quit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImpossibleQuizCreator()
    app.run()