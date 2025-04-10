# Author: Israfil Palabay
# The Impossible Quiz Creator
# April 10, 2025

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