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