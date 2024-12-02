import tkinter as tk
from tkinter import messagebox
import random
import math
from itertools import permutations


def calculate_entropy(possible_numbers):
    """
    Calculate Shannon entropy for the current set of possible numbers.
    """
    total = len(possible_numbers)
    if total == 0:
        return 0  # No uncertainty if there are no possibilities
    return math.log2(total)  # Entropy is log2 of the number of possibilities


def get_feedback(secret, guess):
    """
    Calculate the Bulls and Cows feedback for a given guess.
    - Bulls: Correct digits in the correct positions.
    - Cows: Correct digits but in the wrong positions.
    """
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(min(secret.count(digit), guess.count(digit)) for digit in set(guess)) - bulls
    return bulls, cows


def generate_possible_numbers(length):
    """
    Generate all possible unique digit combinations of a given length.
    Uses permutations to ensure digits are unique.
    """
    return [''.join(p) for p in permutations("0123456789", length)]


class BullsAndCowsGame:
    """
    Main class to handle the logic and user interface of the Bulls and Cows game.
    """
    def __init__(self, root):
        """
        Initialize the game, including the secret number, possible numbers, and UI components.
        """
        self.root = root
        self.root.title("Bulls and Cows Game")

        # Generate a random 4-digit secret number with unique digits
        self.secret = ''.join(random.sample("0123456789", 4))

        # Generate all possible numbers (4-digit combinations with unique digits)
        self.possible_numbers = generate_possible_numbers(4)

        # Create UI components
        tk.Label(root, text="Enter your guess:").pack(pady=5)
        self.guess_entry = tk.Entry(root)
        self.guess_entry.pack(pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.history_label = tk.Label(root, text="History:", font=("Arial", 12))
        self.history_label.pack(pady=5)

        self.history_text = tk.Text(root, height=15, width=60, state=tk.DISABLED)
        self.history_text.pack(pady=5)

        # Buttons for game actions
        tk.Button(root, text="Submit", command=self.submit_guess).pack(pady=5)
        tk.Button(root, text="Restart", command=self.restart_game).pack(pady=5)
        tk.Button(root, text="Reveal Number", command=self.reveal_number).pack(pady=5)

    def submit_guess(self):
        """
        Handle the submission of a guess, calculate feedback, update the game state, and display results.
        """
        guess = self.guess_entry.get().strip()
        if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != len(guess):
            messagebox.showerror("Invalid Input", "Please enter a 4-digit number with unique digits.")
            return

        bulls, cows = get_feedback(self.secret, guess)
        initial_entropy = calculate_entropy(self.possible_numbers)

        # Filter possible numbers based on feedback
        self.possible_numbers = [
            num for num in self.possible_numbers if get_feedback(num, guess) == (bulls, cows)
        ]
        updated_entropy = calculate_entropy(self.possible_numbers)
        mutual_information = initial_entropy - updated_entropy

        # Update the UI with the results
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(
            tk.END,
            f"Guess: {guess}, Bulls: {bulls}, Cows: {cows}, "
            f"Entropy: {updated_entropy:.4f}, Mutual Info: {mutual_information:.4f}\n"
        )
        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)

        self.result_label.config(
            text=f"Bulls: {bulls}, Cows: {cows}\nEntropy: {updated_entropy:.4f}\nMutual Information: {mutual_information:.4f}"
        )

        # Check if the player guessed correctly
        if bulls == 4:
            messagebox.showinfo("Congratulations!", f"You guessed the number {self.secret}!")
            self.restart_game()
        elif not self.possible_numbers:
            messagebox.showerror("Error", "No possible numbers remain. Restarting game.")
            self.restart_game()

    def reveal_number(self):
        """
        Reveal the secret number to the player and restart the game.
        """
        messagebox.showinfo("Secret Number", f"The secret number is: {self.secret}")
        self.restart_game()

    def restart_game(self):
        """
        Restart the game by resetting the secret number, possible numbers, and UI components.
        """
        self.secret = ''.join(random.sample("0123456789", 4))
        self.possible_numbers = generate_possible_numbers(4)
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        self.result_label.config(text="")
        self.guess_entry.delete(0, tk.END)


# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = BullsAndCowsGame(root)
    root.mainloop()
