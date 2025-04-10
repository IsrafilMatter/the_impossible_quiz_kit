# Author: Israfil Palabay
# The Impossible Quiz
# April 10, 2025

import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import os
import random
from PIL import Image, ImageTk

class ImpossibleQuiz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("The Impossible Quiz")
        self.root.geometry("800x600")
        
        # Initialize pygame mixer for sound
        pygame.mixer.init()
        
        # Game state
        self.lives = 3
        self.skips = 3
        self.current_question = None
        self.questions = []
        self.bomb_timer = None
        
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
            command=self.start_game,
            borderwidth=0
        )
        self.start_button.pack()
        
        # Create game frame (initially hidden)
        self.game_frame = tk.Frame(self.main_frame, bg=self.colors['baby_power'])
        
        # Load sounds
        self.sound_files = {
            'fart': "quick_reverb_fart_sound_effect.mp3",
            'explosion': "explosion_effect_sound_effect.mp3",
            'ding': "ding_sound_effect.mp3"
        }
        
        # Load questions
        self.load_questions()
        
    def load_questions(self):
        try:
            with open("quiz_data.txt", "r") as f:
                content = f.read().strip()
                question_blocks = content.split("---")
                
                for block in question_blocks:
                    if not block.strip():
                        continue
                    
                    lines = block.strip().split("\n")
                    question = {}
                    
                    for line in lines:
                        if line.startswith("Q: "):
                            question['question'] = line[3:]
                        elif line.startswith(("A: ", "B: ", "C: ", "D: ")):
                            if 'choices' not in question:
                                question['choices'] = {}
                            question['choices'][line[0]] = line[3:]
                        elif line.startswith("ANSWER: "):
                            question['correct'] = line[8:]
                    
                    if question:
                        self.questions.append(question)
        except FileNotFoundError:
            messagebox.showerror("Error", "No questions found! Please create some questions first.")
            self.root.quit()
    
    def start_game(self):
        # Play fart sound
        self.play_sound('fart')
        
        # Hide start button and show game
        self.start_button.pack_forget()
        self.game_frame.pack(expand=True, fill='both')
        
        # Create game interface
        self.create_game_interface()
        
        # Show first question
        self.show_next_question()
    
    def create_game_interface(self):
        # Status frame
        status_frame = tk.Frame(self.game_frame, bg=self.colors['baby_power'])
        status_frame.pack(fill='x', pady=10)
        
        # Lives
        self.lives_label = tk.Label(
            status_frame,
            text=f"Lives: {'❤' * self.lives}",
            font=('Comica', 12),
            bg=self.colors['baby_power'],
            fg=self.colors['fire_engine_red']
        )
        self.lives_label.pack(side='left', padx=10)
        
        # Skips
        self.skips_label = tk.Label(
            status_frame,
            text=f"Skips: {self.skips}",
            font=('Comica', 12),
            bg=self.colors['baby_power'],
            fg=self.colors['lapis_lazuli']
        )
        self.skips_label.pack(side='right', padx=10)
        
        # Question frame
        self.question_frame = tk.Frame(self.game_frame, bg=self.colors['baby_power'])
        self.question_frame.pack(pady=20)
        
        self.question_label = tk.Label(
            self.question_frame,
            text="",
            font=('Comica', 14),
            bg=self.colors['baby_power'],
            fg=self.colors['raisin_black'],
            wraplength=600
        )
        self.question_label.pack(pady=10)
        
        # Answers frame
        self.answers_frame = tk.Frame(self.game_frame, bg=self.colors['baby_power'])
        self.answers_frame.pack(pady=20)
        
        # Create answer buttons
        self.answer_buttons = {}
        for choice in ['A', 'B', 'C', 'D']:
            btn = tk.Button(
                self.answers_frame,
                text="",
                font=('Comica', 12),
                bg=self.colors['school_bus_yellow'],
                fg=self.colors['raisin_black'],
                width=40,
                command=lambda c=choice: self.check_answer(c)
            )
            btn.pack(pady=5)
            self.answer_buttons[choice] = btn
        
        # Skip button
        self.skip_button = tk.Button(
            self.game_frame,
            text="Skip",
            command=self.skip_question,
            font=('Comica', 12),
            bg=self.colors['lapis_lazuli'],
            fg=self.colors['baby_power']
        )
        self.skip_button.pack(pady=10)
        
        # Timer label (for bomb questions)
        self.timer_label = tk.Label(
            self.game_frame,
            text="",
            font=('Comica', 16, 'bold'),
            bg=self.colors['baby_power'],
            fg=self.colors['fire_engine_red']
        )
        self.timer_label.pack(pady=5)
    
    def show_next_question(self):
        if not self.questions:
            messagebox.showinfo("Congratulations!", "You've completed all questions!")
            self.root.quit()
            return
        
        # Reset timer if it exists
        if self.bomb_timer:
            self.root.after_cancel(self.bomb_timer)
            self.bomb_timer = None
            self.timer_label.config(text="")
        
        # Select random question
        self.current_question = random.choice(self.questions)
        self.questions.remove(self.current_question)
        
        # Update interface
        self.question_label.config(text=self.current_question['question'])
        
        for choice, button in self.answer_buttons.items():
            button.config(text=self.current_question['choices'][choice])
        
        # Set bomb timer for some questions (20% chance)
        if random.random() < 0.2:
            self.start_bomb_timer()