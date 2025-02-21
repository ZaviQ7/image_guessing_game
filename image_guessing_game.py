import tkinter as tk
import random
from PIL import Image, ImageTk
import time
import os

class ImageGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Guessing Game")
        self.is_dark_mode = False
        self.user_wins = 0
        self.ai_wins = 0
        self.player2_wins = 0
        self.image_list = [
            os.path.join("images for ai", "x.jfif"),
            os.path.join("images for ai", "apple.jfif"),
            os.path.join("images for ai", "amazon.jfif"),
            os.path.join("images for ai", "DSAI.jfif"),
            os.path.join("images for ai", "OAI.jfif"),
            os.path.join("images for ai", "meta.jfif"),
            os.path.join("images for ai", "insta.jfif"),
            os.path.join("images for ai", "gh.jfif"),
            os.path.join("images for ai", "google.jfif"),
            os.path.join("images for ai", "microsoft.jfif"),
            os.path.join("images for ai", "netflix.jfif"),
            os.path.join("images for ai", "tesla.jfif"),
        ]
        
        self.menu_label = None
        self.name_label = None
        self.github_label = None
        self.difficulty_label = None
        self.explanation_label = None
        self.scoreboard_label = None
        self.feedback_label = None
        self.player_counter_label = None
        self.ai_counter_label = None
        self.player2_counter_label = None

        self.show_menu()

    def show_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.menu_label = tk.Label(self.root, 
                                text="Welcome to the Image Guessing Game!",
                                font=("Arial", 16))
        self.menu_label.pack(pady=10)
        
        self.name_label = tk.Label(self.root, 
                                text="Created by Zavi Quintero",
                                font=("Arial", 12))
        self.name_label.pack()
        
        self.github_label = tk.Label(self.root, 
                                    text="GitHub: ZaviQ7",
                                    font=("Arial", 12))
        self.github_label.pack(pady=(0, 20))

        self.single_player_button = tk.Button(self.root, 
                                            text="Single Player (User vs AI)", 
                                            command=lambda: self.set_multiplayer(False), 
                                            font=("Arial", 14))
        self.single_player_button.pack(pady=20)
        
        self.multiplayer_button = tk.Button(self.root, 
                                        text="Multiplayer (Player vs Player)", 
                                        command=lambda: self.set_multiplayer(True), 
                                        font=("Arial", 14))
        self.multiplayer_button.pack(pady=20)

        # Add common buttons (without reset button)
        self.add_common_buttons(include_reset=False)

        self.update_theme()

    def set_multiplayer(self, is_multiplayer):
        self.is_multiplayer = is_multiplayer
        self.show_difficulty_menu()

    def show_difficulty_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.difficulty_label = tk.Label(self.root, text="Select Difficulty Level", font=("Arial", 16))
        self.difficulty_label.pack(pady=20)
        self.easy_button = tk.Button(self.root, text="Easy (3 Images)", command=lambda: self.start_game_with_difficulty(3), font=("Arial", 12))
        self.easy_button.pack(pady=10)
        self.medium_button = tk.Button(self.root, text="Medium (6 Images)", command=lambda: self.start_game_with_difficulty(6), font=("Arial", 12))
        self.medium_button.pack(pady=10)
        self.hard_button = tk.Button(self.root, text="Hard (12 Images)", command=lambda: self.start_game_with_difficulty(12), font=("Arial", 12))
        self.hard_button.pack(pady=10)

        # Add common buttons (without reset button)
        self.add_common_buttons(include_reset=False)

    def start_game_with_difficulty(self, num_images):
        self.num_images = num_images
        self.initialize_game()

    def initialize_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.columns_per_row = 3 if self.num_images <= 6 else 4
        self.rows = (self.num_images + self.columns_per_row - 1) // self.columns_per_row

        try:
            self.images = [Image.open(img_path).resize((150, 150)) for img_path in self.image_list[:self.num_images]]
            self.image_labels = [ImageTk.PhotoImage(img) for img in self.images]
        except Exception as e:
            print(f"Error loading images: {e}")
            return

        self.buttons_frame = tk.Frame(self.root)
        self.buttons = []

        for i, img_label in enumerate(self.image_labels):
            row = i // self.columns_per_row
            column = i % self.columns_per_row
            button = tk.Button(self.buttons_frame, image=img_label, 
                             command=lambda i=i: self.player_guess(i), 
                             borderwidth=2, relief="raised")
            button.grid(row=row, column=column, padx=10, pady=10)
            self.buttons.append(button)

        self.buttons_frame.pack(pady=20)

        self.explanation_label = tk.Label(self.root, text="Welcome to the Image Guessing Game!\n\nYour goal is to guess which image has been randomly chosen.\n\nClick on the images to make a guess. Good luck!", font=("Arial", 12))
        self.explanation_label.pack(pady=10)

        if self.is_multiplayer:
            self.player_counter_label = tk.Label(self.root, text="Player 1 Guesses: 0", font=("Arial", 12))
            self.player2_counter_label = tk.Label(self.root, text="Player 2 Guesses: 0", font=("Arial", 12))
        else:
            self.player_counter_label = tk.Label(self.root, text="Your Guesses: 0", font=("Arial", 12))
            self.ai_counter_label = tk.Label(self.root, text="AI Guesses: 0", font=("Arial", 12))

        # Add scoreboard and reset button ONLY in game screen
        self.scoreboard_label = tk.Label(self.root, text=f"User Wins: {self.user_wins} | AI Wins: {self.ai_wins} | Player 2 Wins: {self.player2_wins}", font=("Arial", 12))
        self.scoreboard_label.place(x=10, y=10)

        self.reset_button = tk.Button(self.root, 
                                   text="Reset Scoreboard", 
                                   command=self.reset_scoreboard, 
                                   font=("Arial", 12))
        self.reset_button.place(x=330, y=10)

        self.play_again_button = tk.Button(self.root, text="Play Again", command=self.play_again, state="disabled")
        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 12))

        self.player_counter_label.pack(pady=5)
        if not self.is_multiplayer:
            self.ai_counter_label.pack(pady=5)
        else:
            self.player2_counter_label.pack(pady=5)
        self.play_again_button.pack(pady=20)
        self.feedback_label.pack(pady=10)

        # Add common buttons (without reset button)
        self.add_common_buttons(include_reset=False)

        window_width = self.columns_per_row * 170
        window_height = self.rows * 170 + 250
        self.root.geometry(f"{window_width}x{window_height}")

        self.start_game()

    def add_common_buttons(self, include_reset=False):
        # Add Toggle Dark Mode button
        self.toggle_button = tk.Button(self.root, 
                                     text="Toggle Dark Mode", 
                                     command=self.toggle_theme)
        self.toggle_button.place(x=1600, y=10)

        # Add Return to Menu button
        self.return_button = tk.Button(self.root, 
                                      text="Return to Menu", 
                                      command=self.show_menu)
        self.return_button.place(x=1760, y=10)

        # Only add reset button if specified
        if include_reset:
            self.reset_button = tk.Button(self.root, 
                                        text="Reset Scoreboard", 
                                        command=self.reset_scoreboard, 
                                        font=("Arial", 12))
            self.reset_button.place(x=330, y=10)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_theme()

    def update_theme(self):
        bg_color = 'black' if self.is_dark_mode else 'white'
        fg_color = 'white' if self.is_dark_mode else 'black'
        self.root.config(bg=bg_color)
        
        widgets_to_update = [
            self.menu_label, self.name_label, self.github_label,
            self.difficulty_label if hasattr(self, 'difficulty_label') else None,
            self.explanation_label if hasattr(self, 'explanation_label') else None,
            self.scoreboard_label if hasattr(self, 'scoreboard_label') else None,
            self.feedback_label if hasattr(self, 'feedback_label') else None
        ]
    
        if hasattr(self, 'player_counter_label'):
            widgets_to_update.append(self.player_counter_label)
        if hasattr(self, 'ai_counter_label'):
            widgets_to_update.append(self.ai_counter_label)
        if hasattr(self, 'player2_counter_label'):
            widgets_to_update.append(self.player2_counter_label)

        for widget in filter(None, widgets_to_update):
            widget.config(bg=bg_color, fg=fg_color)
    
        all_buttons = []
        if hasattr(self, 'single_player_button'):
            all_buttons.append(self.single_player_button)
        if hasattr(self, 'multiplayer_button'):
            all_buttons.append(self.multiplayer_button)
        if hasattr(self, 'buttons'):
            all_buttons.extend(self.buttons)
        if hasattr(self, 'play_again_button'):
            all_buttons.append(self.play_again_button)
        if hasattr(self, 'toggle_button'):
            all_buttons.append(self.toggle_button)
        if hasattr(self, 'return_button'):
            all_buttons.append(self.return_button)
        if hasattr(self, 'easy_button'):
            all_buttons.extend([self.easy_button, self.medium_button, self.hard_button])
        if hasattr(self, 'reset_button'):
            all_buttons.append(self.reset_button)

        for button in all_buttons:
            button.config(bg='gray' if self.is_dark_mode else 'lightgray', fg=fg_color)

    def start_game(self):
        self.start_time = time.time()
        self.selected_image_index = random.randint(0, self.num_images - 1)
        if self.is_multiplayer:
            self.player1_guess_count = 0
            self.player2_guess_count = 0
            self.player_counter_label.config(text="Player 1 Guesses: 0")
            self.player2_counter_label.config(text="Player 2 Guesses: 0")
            self.feedback_label.config(text="Player 1's turn. Make your guess.", fg="black")
            self.current_player = 1
        else:
            self.player_guess_count = 0
            self.ai_guess_count = 0
            self.player_counter_label.config(text="Your Guesses: 0")
            self.ai_counter_label.config(text="AI Guesses: 0")
            self.feedback_label.config(text="Your turn. Make your guess.", fg="black")
            self.is_user_turn = True
        self.play_again_button.config(state="disabled")

    def player_guess(self, index):
        if self.is_multiplayer:
            if self.current_player == 1:
                self.player1_guess_count += 1
                self.player_counter_label.config(text=f"Player 1 Guesses: {self.player1_guess_count}")
                if index == self.selected_image_index:
                    elapsed_time = time.time() - self.start_time
                    self.feedback_label.config(text=f"Player 1 guessed correctly!\nTime: {elapsed_time:.2f} seconds", fg="green")
                    self.user_wins += 1
                    self.update_scoreboard()
                    self.highlight_correct_guess()
                    for button in self.buttons:
                        button.config(state="disabled")
                    self.play_again_button.config(state="normal")
                    return
                else:
                    self.feedback_label.config(text="Player 1 guessed incorrectly. Now it's Player 2's turn.", fg="red")
                    self.current_player = 2
            else:
                self.player2_guess_count += 1
                self.player2_counter_label.config(text=f"Player 2 Guesses: {self.player2_guess_count}")
                if index == self.selected_image_index:
                    elapsed_time = time.time() - self.start_time
                    self.feedback_label.config(text=f"Player 2 guessed correctly!\nTime: {elapsed_time:.2f} seconds", fg="green")
                    self.player2_wins += 1
                    self.update_scoreboard()
                    self.highlight_correct_guess()
                    for button in self.buttons:
                        button.config(state="disabled")
                    self.play_again_button.config(state="normal")
                    return
                else:
                    self.feedback_label.config(text="Player 2 guessed incorrectly. Now it's Player 1's turn.", fg="red")
                    self.current_player = 1
        else:
            if self.is_user_turn:
                self.player_guess_count += 1
                self.player_counter_label.config(text=f"Your Guesses: {self.player_guess_count}")
                if index == self.selected_image_index:
                    elapsed_time = time.time() - self.start_time
                    self.feedback_label.config(text=f"You guessed correctly!\nTime: {elapsed_time:.2f} seconds", fg="green")
                    self.user_wins += 1
                    self.update_scoreboard()
                    self.highlight_correct_guess()
                    for button in self.buttons:
                        button.config(state="disabled")
                    self.play_again_button.config(state="normal")
                    return
                else:
                    self.feedback_label.config(text="Incorrect, now it's the AI's turn.", fg="red")
                    self.is_user_turn = False
                    self.root.after(1000, self.ai_guess)
            else:
                return

    def ai_guess(self):
        ai_guess_index = random.choice(range(self.num_images))
        self.ai_guess_count += 1
        self.ai_counter_label.config(text=f"AI Guesses: {self.ai_guess_count}")
        if ai_guess_index == self.selected_image_index:
            self.feedback_label.config(text="You lost to the AI.", fg="red")
            self.ai_wins += 1
            self.update_scoreboard()
            self.highlight_correct_guess()
            for button in self.buttons:
                button.config(state="disabled")
            self.play_again_button.config(state="normal")
        else:
            self.feedback_label.config(text="AI guessed incorrectly, now it's your turn.", fg="blue")
            self.is_user_turn = True

    def highlight_correct_guess(self):
        self.buttons[self.selected_image_index].config(bg="green")
        self.buttons[self.selected_image_index].config(relief="sunken")

    def update_scoreboard(self):
        if hasattr(self, 'scoreboard_label'):
            self.scoreboard_label.config(text=f"User Wins: {self.user_wins} | AI Wins: {self.ai_wins} | Player 2 Wins: {self.player2_wins}")

    def reset_scoreboard(self):
        self.user_wins = 0
        self.ai_wins = 0
        self.player2_wins = 0
        self.update_scoreboard()

    def play_again(self):
        self.initialize_game()
        self.update_scoreboard()

root = tk.Tk()
game = ImageGuessingGame(root)
root.mainloop()












