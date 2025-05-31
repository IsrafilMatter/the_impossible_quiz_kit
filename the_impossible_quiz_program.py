# Author: Israfil Palabay
# The Impossible Quiz
# May 5, 2025

import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import os
import random
from PIL import Image, ImageTk
import time

class ImpossibleQuiz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("The Impossible Quiz")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Initialize pygame mixer for sound
        pygame.mixer.init()
        
        # Game state
        self.lives = 3
        self.skips = 3
        self.score = 0
        self.current_question = None
        self.questions = []
        self.bomb_timer = None
        self.question_timer = None
        self.question_time = 30  # Default time for each question
        
        # Colors - Modern color palette
        self.colors = {
            'background': '#F5F7FA',
            'primary': '#3498DB',
            'secondary': '#2ECC71',
            'accent': '#9B59B6',
            'danger': '#E74C3C',
            'warning': '#F39C12',
            'text': '#2C3E50',
            'light_text': '#7F8C8D'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['background'])
        
        # Create custom font styles
        self.title_font = ('Helvetica', 28, 'bold')
        self.heading_font = ('Helvetica', 18, 'bold')
        self.normal_font = ('Helvetica', 14)
        self.button_font = ('Helvetica', 12, 'bold')
        
        # Try to load images or use fallbacks
        try:
            # Load start button image
            start_img = Image.open("begin_interface.jpg")
            start_img = start_img.resize((300, 150), Image.LANCZOS)
            self.start_photo = ImageTk.PhotoImage(start_img)
        except:
            # Create a fallback button if image not found
            self.start_photo = None
        
        # Create main frame with padding
        self.main_frame = tk.Frame(self.root, bg=self.colors['background'], padx=30, pady=30)
        self.main_frame.pack(expand=True, fill='both')
        
        # Create title label
        self.title_label = tk.Label(
            self.main_frame,
            text="THE IMPOSSIBLE QUIZ",
            font=self.title_font,
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        self.title_label.pack(pady=(0, 20))
        
        # Center frame for start button
        self.start_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        self.start_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Start button (with image or text)
        if self.start_photo:
            self.start_button = tk.Button(
                self.start_frame,
                image=self.start_photo,
                command=self.start_game,
                borderwidth=0,
                cursor="hand2"
            )
        else:
            self.start_button = tk.Button(
                self.start_frame,
                text="START GAME",
                command=self.start_game,
                font=self.heading_font,
                bg=self.colors['primary'],
                fg='white',
                padx=30,
                pady=15,
                borderwidth=0,
                cursor="hand2"
            )
            # Add hover effect
            self.start_button.bind("<Enter>", lambda e: self.start_button.config(bg=self.colors['accent']))
            self.start_button.bind("<Leave>", lambda e: self.start_button.config(bg=self.colors['primary']))
        
        self.start_button.pack()
        
        # Add subtitle
        self.subtitle = tk.Label(
            self.start_frame,
            text="Are you ready for the challenge?",
            font=self.normal_font,
            bg=self.colors['background'],
            fg=self.colors['light_text']
        )
        self.subtitle.pack(pady=20)
        
        # Create game frame (initially hidden)
        self.game_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        
        # Load sounds
        self.sound_files = {
            'fart': "quick_reverb_fart_sound_effect.mp3",
            'explosion': "explosion_effect_sound_effect.mp3",
            'ding': "ding_sound_effect.mp3"
        }
        
        # Load questions
        self.load_questions()
        
        # Add footer
        footer_frame = tk.Frame(self.root, bg=self.colors['text'], height=30)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        footer_label = tk.Label(
            footer_frame, 
            text="© 2025 Israfil Palabay", 
            fg="white", 
            bg=self.colors['text'],
            font=('Helvetica', 10)
        )
        footer_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
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
            # Create sample questions if file not found
            self.questions = [
                {
                    'question': 'What is the answer to life, the universe, and everything?',
                    'choices': {'A': '24', 'B': '42', 'C': '12', 'D': 'Chocolate'},
                    'correct': 'B'
                },
                {
                    'question': 'Which of these is NOT a fruit?',
                    'choices': {'A': 'Tomato', 'B': 'Apple', 'C': 'Carrot', 'D': 'Avocado'},
                    'correct': 'C'
                },
                {
                    'question': 'How many holes does a straw have?',
                    'choices': {'A': '1', 'B': '2', 'C': '0', 'D': 'Infinite'},
                    'correct': 'B'
                }
            ]
            messagebox.showinfo("Info", "Using sample questions as quiz_data.txt was not found.")
    
    def start_game(self):
        # Play fart sound
        self.play_sound('fart')
        
        # Hide start elements
        self.title_label.pack_forget()
        self.start_frame.place_forget()
        
        # Show game
        self.game_frame.pack(expand=True, fill='both')
        
        # Create game interface
        self.create_game_interface()
        
        # Show first question
        self.show_next_question()
    
    def create_game_interface(self):
        # Game header with title
        game_header = tk.Frame(self.game_frame, bg=self.colors['primary'], padx=20, pady=10)
        game_header.pack(fill='x')
        
        header_title = tk.Label(
            game_header,
            text="THE IMPOSSIBLE QUIZ",
            font=self.heading_font,
            bg=self.colors['primary'],
            fg='white'
        )
        header_title.pack(side='left')
        
        # Score display
        self.score_display = tk.Label(
            game_header,
            text="Score: 0",
            font=self.button_font,
            bg=self.colors['primary'],
            fg='white'
        )
        self.score_display.pack(side='right')
        
        # Status frame with modern styling
        status_frame = tk.Frame(self.game_frame, bg=self.colors['background'], pady=15)
        status_frame.pack(fill='x')
        
        # Lives with heart icons
        lives_frame = tk.Frame(status_frame, bg=self.colors['background'])
        lives_frame.pack(side='left', padx=20)
        
        lives_label = tk.Label(
            lives_frame,
            text="Lives:",
            font=self.normal_font,
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        lives_label.pack(side='left', padx=(0, 10))
        
        self.heart_labels = []
        for i in range(3):
            heart = tk.Label(
                lives_frame,
                text="❤️",
                font=('Helvetica', 16),
                bg=self.colors['background']
            )
            heart.pack(side='left', padx=2)
            self.heart_labels.append(heart)
        
        # Question timer frame (red box area)
        self.question_timer_frame = tk.Frame(
            status_frame, 
            bg=self.colors['danger'],
            highlightbackground=self.colors['danger'],
            highlightthickness=2,
            padx=15,
            pady=5
        )
        self.question_timer_frame.pack(side='left', padx=20, fill='y')
        
        self.question_timer_label = tk.Label(
            self.question_timer_frame,
            text="Time: 30",
            font=('Helvetica', 16, 'bold'),
            bg=self.colors['danger'],
            fg='white'
        )
        self.question_timer_label.pack()
        
        # Skips with modern styling and clickable functionality
        skips_frame = tk.Frame(status_frame, bg=self.colors['background'])
        skips_frame.pack(side='right', padx=20)
        
        # Make "Skips:" text clickable
        skips_label = tk.Label(
            skips_frame,
            text="Skips:",
            font=self.normal_font,
            bg=self.colors['background'],
            fg=self.colors['primary'],
            cursor="hand2"
        )
        skips_label.pack(side='left', padx=(0, 10))
        
        # Bind click event to skip_question function
        skips_label.bind("<Button-1>", lambda e: self.skip_question())
        
        # Add hover effect to indicate it's clickable
        skips_label.bind("<Enter>", lambda e: skips_label.config(fg=self.colors['accent'], underline=True))
        skips_label.bind("<Leave>", lambda e: skips_label.config(fg=self.colors['primary'], underline=False))
        
        self.skip_indicators = []
        for i in range(3):
            skip_ind = tk.Label(
                skips_frame,
                text="⏭️",
                font=('Helvetica', 16),
                bg=self.colors['background']
            )
            skip_ind.pack(side='left', padx=2)
            self.skip_indicators.append(skip_ind)
        
        # Question number
        self.question_number = tk.Label(
            self.game_frame,
            text="Question 1",
            font=self.heading_font,
            bg=self.colors['background'],
            fg=self.colors['accent']
        )
        self.question_number.pack(pady=(20, 5))
        
        # Question frame with card-like styling
        self.question_card = tk.Frame(
            self.game_frame,
            bg='white',
            padx=30,
            pady=20,
            highlightbackground=self.colors['light_text'],
            highlightthickness=1
        )
        self.question_card.pack(fill='x', padx=40, pady=10)
        
        self.question_label = tk.Label(
            self.question_card,
            text="",
            font=self.normal_font,
            bg='white',
            fg=self.colors['text'],
            wraplength=700,
            justify='center'
        )
        self.question_label.pack(pady=10)
        
        # Answers frame
        self.answers_frame = tk.Frame(self.game_frame, bg=self.colors['background'])
        self.answers_frame.pack(pady=20)
        
        # Create answer buttons with modern styling
        self.answer_buttons = {}
        button_colors = [self.colors['primary'], self.colors['secondary'], 
                         self.colors['accent'], self.colors['warning']]
        
        for i, choice in enumerate(['A', 'B', 'C', 'D']):
            btn_frame = tk.Frame(self.answers_frame, bg=self.colors['background'])
            btn_frame.pack(pady=8)
            
            # Choice letter indicator
            choice_indicator = tk.Label(
                btn_frame,
                text=choice,
                font=self.button_font,
                bg=button_colors[i],
                fg='white',
                width=2,
                padx=10
            )
            choice_indicator.pack(side='left')
            
            # Answer button
            btn = tk.Button(
                btn_frame,
                text="",
                font=self.normal_font,
                bg='white',
                fg=self.colors['text'],
                width=50,
                height=1,
                anchor='w',
                padx=15,
                pady=8,
                command=lambda c=choice: self.check_answer(c),
                cursor="hand2"
            )
            btn.pack(side='left')
            
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn, c=button_colors[i]: b.config(bg=f'#{int(c[1:3], 16):02x}{int(c[3:5], 16):02x}{int(c[5:7], 16):02x}20'))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg='white'))
            
            self.answer_buttons[choice] = btn
        
        # Bottom controls frame
        controls_frame = tk.Frame(self.game_frame, bg=self.colors['background'])
        controls_frame.pack(pady=20)
        
        # Skip button
        self.skip_button = tk.Button(
            controls_frame,
            text="Skip Question",
            command=self.skip_question,
            font=self.button_font,
            bg=self.colors['accent'],
            fg='white',
            padx=15,
            pady=8,
            borderwidth=0,
            cursor="hand2"
        )
        self.skip_button.pack(side='left', padx=10)
        
        # Add hover effect
        self.skip_button.bind("<Enter>", lambda e: self.skip_button.config(bg='#8E44AD'))
        self.skip_button.bind("<Leave>", lambda e: self.skip_button.config(bg=self.colors['accent']))
        
        # Quit button
        quit_button = tk.Button(
            controls_frame,
            text="Quit Game",
            command=self.confirm_quit,
            font=self.button_font,
            bg=self.colors['danger'],
            fg='white',
            padx=15,
            pady=8,
            borderwidth=0,
            cursor="hand2"
        )
        quit_button.pack(side='left', padx=10)
        
        # Add hover effect
        quit_button.bind("<Enter>", lambda e: quit_button.config(bg='#C0392B'))
        quit_button.bind("<Leave>", lambda e: quit_button.config(bg=self.colors['danger']))
        
        # Timer label (for bomb questions)
        self.timer_frame = tk.Frame(self.game_frame, bg=self.colors['background'])
        self.timer_frame.pack(pady=10)
        
        self.timer_label = tk.Label(
            self.timer_frame,
            text="",
            font=('Helvetica', 24, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['danger']
        )
        self.timer_label.pack()
    
    def show_next_question(self):
        if not self.questions:
            self.show_victory_screen()
            return
        
        # Reset bomb timer if it exists
        if self.bomb_timer:
            self.root.after_cancel(self.bomb_timer)
            self.bomb_timer = None
            self.timer_label.config(text="")
        
        # Reset question timer if it exists
        if self.question_timer:
            self.root.after_cancel(self.question_timer)
        
        # Select random question
        self.current_question = random.choice(self.questions)
        self.questions.remove(self.current_question)
        
        # Update question number
        question_num = self.score + 1
        self.question_number.config(text=f"Question {question_num}")
        
        # Update interface with animation
        self.question_label.config(text="")
        self.root.update()
        
        # Typewriter effect for question
        self.typewriter_effect(self.current_question['question'])
        
        # Update answer buttons
        for choice, button in self.answer_buttons.items():
            button.config(text=self.current_question['choices'][choice])
        
        # Start question timer
        self.question_time = 30
        self.update_question_timer()
        
        # Set bomb timer for some questions (20% chance)
        if random.random() < 0.2:
            self.start_bomb_timer()
    
    def update_question_timer(self):
        if self.question_time > 0:
            self.question_timer_label.config(text=f"Time: {self.question_time}")
            
            # Change color based on time remaining
            if self.question_time <= 5:
                self.question_timer_frame.config(bg=self.colors['danger'])
                self.question_timer_label.config(bg=self.colors['danger'])
            elif self.question_time <= 10:
                self.question_timer_frame.config(bg=self.colors['warning'])
                self.question_timer_label.config(bg=self.colors['warning'])
            
            self.question_time -= 1
            self.question_timer = self.root.after(1000, self.update_question_timer)
        else:
            self.play_sound('explosion')
            self.lose_life("Time's up!")
    
    def typewriter_effect(self, text, delay=30):
        """Create a typewriter effect for displaying the question"""
        def type_char(index=0):
            if index < len(text):
                current_text = self.question_label.cget("text") + text[index]
                self.question_label.config(text=current_text)
                self.root.after(delay, type_char, index + 1)
        
        type_char()
    
    def start_bomb_timer(self):
        self.time_left = random.randint(5, 10)
        
        # Show bomb icon
        self.timer_label.config(text=f"💣 {self.time_left}")
        
        # Flash effect for timer
        self.flash_timer()
        
        # Start countdown
        self.update_timer()
    
    def flash_timer(self):
        """Create flashing effect for the timer"""
        if self.bomb_timer:  # Only flash if timer is active
            current_fg = self.timer_label.cget("fg")
            new_fg = self.colors['background'] if current_fg == self.colors['danger'] else self.colors['danger']
            self.timer_label.config(fg=new_fg)
            self.root.after(500, self.flash_timer)
    
    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"💣 {self.time_left}")
            self.time_left -= 1
            self.bomb_timer = self.root.after(1000, self.update_timer)
        else:
            self.play_sound('explosion')
            self.lose_life("Time's up!")
    
    def check_answer(self, choice):
        # Cancel timers
        if self.bomb_timer:
            self.root.after_cancel(self.bomb_timer)
            self.bomb_timer = None
            self.timer_label.config(text="")
        
        if self.question_timer:
            self.root.after_cancel(self.question_timer)
            self.question_timer = None
        
        if choice.upper() == self.current_question['correct'].upper():
            self.play_sound('ding')
            
            # Highlight correct answer
            self.answer_buttons[choice].config(bg=self.colors['secondary'])
            self.root.update()
            self.root.after(500)  # Pause to show correct answer
            
            # Update score
            self.score += 1
            self.score_display.config(text=f"Score: {self.score}")
            
            # Show next question
            self.show_next_question()
        else:
            self.play_sound('explosion')
            
            # Highlight wrong answer in red
            self.answer_buttons[choice].config(bg=self.colors['danger'])
            
            # Highlight correct answer in green
            correct = self.current_question['correct'].upper()
            self.answer_buttons[correct].config(bg=self.colors['secondary'])
            
            self.root.update()
            self.root.after(1000)  # Pause to show correct/wrong answers
            
            # Reset button colors
            for btn in self.answer_buttons.values():
                btn.config(bg='white')
            
            self.lose_life("Wrong answer!")
    
    def lose_life(self, message):
        self.lives -= 1
        
        # Update heart display
        if self.lives >= 0:
            self.heart_labels[self.lives].config(text="💔")
        
        if self.lives <= 0:
            self.show_game_over(message)
        else:
            messagebox.showinfo("Oops!", f"{message}\nLives remaining: {self.lives}")
            # Continue with next question
            self.show_next_question()
    
    def skip_question(self):
        if self.skips > 0:
            self.skips -= 1
            
            # Update skip display
            self.skip_indicators[self.skips].config(text="⏹️")
            
            # Cancel any active timers
            if self.bomb_timer:
                self.root.after_cancel(self.bomb_timer)
                self.bomb_timer = None
                self.timer_label.config(text="")
            
            if self.question_timer:
                self.root.after_cancel(self.question_timer)
                self.question_timer = None
            
            self.show_next_question()
        else:
            messagebox.showinfo("No Skips", "You have no skips remaining!")
    
    def show_game_over(self, message):
        # Clear game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # Game over display
        game_over_frame = tk.Frame(self.game_frame, bg=self.colors['background'])
        game_over_frame.pack(expand=True, fill='both')
        
        # Game over message
        game_over_label = tk.Label(
            game_over_frame,
            text="GAME OVER",
            font=('Helvetica', 36, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['danger']
        )
        game_over_label.pack(pady=(100, 20))
        
        # Final score
        score_label = tk.Label(
            game_over_frame,
            text=f"Your Score: {self.score}",
            font=self.heading_font,
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        score_label.pack(pady=10)
        
        # Reason
        reason_label = tk.Label(
            game_over_frame,
            text=message,
            font=self.normal_font,
            bg=self.colors['background'],
            fg=self.colors['light_text']
        )
        reason_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(game_over_frame, bg=self.colors['background'])
        buttons_frame.pack(pady=30)
        
        # Try again button
        try_again_btn = tk.Button(
            buttons_frame,
            text="Try Again",
            command=self.reset_game,
            font=self.button_font,
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=10,
            borderwidth=0,
            cursor="hand2"
        )
        try_again_btn.pack(side='left', padx=10)
        
        # Quit button
        quit_btn = tk.Button(
            buttons_frame,
            text="Quit Game",
            command=self.root.quit,
            font=self.button_font,
            bg=self.colors['danger'],
            fg='white',
            padx=20,
            pady=10,
            borderwidth=0,
            cursor="hand2"
        )
        quit_btn.pack(side='left', padx=10)
    
    def show_victory_screen(self):
        # Clear game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # Victory display
        victory_frame = tk.Frame(self.game_frame, bg=self.colors['background'])
        victory_frame.pack(expand=True, fill='both')
        
        # Victory message
        victory_label = tk.Label(
            victory_frame,
            text="VICTORY!",
            font=('Helvetica', 36, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['secondary']
        )
        victory_label.pack(pady=(100, 20))
        
        # Congratulations message
        congrats_label = tk.Label(
            victory_frame,
            text="Congratulations! You've completed The Impossible Quiz!",
            font=self.heading_font,
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        congrats_label.pack(pady=10)
        
        # Final score
        score_label = tk.Label(
            victory_frame,
            text=f"Your Final Score: {self.score}",
            font=self.normal_font,
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        score_label.pack(pady=10)
        
        # Lives remaining
        lives_label = tk.Label(
            victory_frame,
            text=f"Lives Remaining: {self.lives}",
            font=self.normal_font,
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        lives_label.pack(pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(victory_frame, bg=self.colors['background'])
        buttons_frame.pack(pady=30)
        
        # Play again button
        play_again_btn = tk.Button(
            buttons_frame,
            text="Play Again",
            command=self.reset_game,
            font=self.button_font,
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=10,
            borderwidth=0,
            cursor="hand2"
        )
        play_again_btn.pack(side='left', padx=10)
        
        # Quit button
        quit_btn = tk.Button(
            buttons_frame,
            text="Quit Game",
            command=self.root.quit,
            font=self.button_font,
            bg=self.colors['accent'],
            fg='white',
            padx=20,
            pady=10,
            borderwidth=0,
            cursor="hand2"
        )
        quit_btn.pack(side='left', padx=10)
    
    def reset_game(self):
        # Reset game state
        self.lives = 3
        self.skips = 3
        self.score = 0
        self.load_questions()
        
        # Clear game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # Recreate game interface
        self.create_game_interface()
        
        # Show first question
        self.show_next_question()
    
    def confirm_quit(self):
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.root.quit()
    
    def play_sound(self, sound_name):
        try:
            pygame.mixer.music.load(self.sound_files[sound_name])
            pygame.mixer.music.play()
        except:
            pass  # Silently fail if sound can't be played
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    quiz = impossible_quiz()
    quiz.run()
