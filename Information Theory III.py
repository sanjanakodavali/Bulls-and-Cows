import tkinter as tk
from tkinter import messagebox
import random
import math
from itertools import permutations


def calculate_entropy(possible_numbers):
    """
    Calculate Shannon entropy for the current set of possible numbers.
    Entropy quantifies the uncertainty about the secret number.

    Parameters:
    - possible_numbers: List of all remaining valid numbers.

    Returns:
    - Entropy value (float).
    """
    total = len(possible_numbers)
    if total == 0:
        return 0  # No uncertainty if there are no possibilities
    return math.log2(total)  # Entropy is log2 of the number of possibilities


def get_feedback(secret, guess):
    """
    Compute the Bulls and Cows feedback for a given guess.
    - Bulls: Number of digits in the correct position.
    - Cows: Number of correct digits but in the wrong positions.

    Parameters:
    - secret: The secret number as a string.
    - guess: The player's guess as a string.

    Returns:
    - A tuple (bulls, cows).
    """
    bulls = sum(s == g for s, g in zip(secret, guess))  # Count matching digits in the correct position
    cows = sum(min(secret.count(digit), guess.count(digit)) for digit in set(guess)) - bulls  # Count correct digits in wrong positions
    return bulls, cows


def generate_possible_numbers(length):
    """
    Generate all possible unique-digit numbers of a given length.

    Parameters:
    - length: The number of digits for the numbers to generate.

    Returns:
    - A list of all possible numbers as strings.
    """
    return [''.join(p) for p in permutations("0123456789", length)]


class BullsAndCowsGame:
    """
    A class to handle the logic and user interface of the Bulls and Cows game.
    Includes entropy and mutual information calculations to provide insights on uncertainty.
    """
    def __init__(self, root):
        """
        Initialize the game, including the secret number, possible numbers, and UI components.

        Parameters:
        - root: The Tkinter root window.
        """
        self.root = root
        self.root.title("Bulls and Cows Game")

        # Generate a random 4-digit secret number with unique digits
        self.secret = ''.join(random.sample("0123456789", 4))

        # Generate all possible numbers (4-digit combinations with unique digits)
        self.possible_numbers = generate_possible_numbers(4)

        # Create UI components
        tk.Label(root, text="Enter your guess:", font=("Arial", 12)).pack(pady=5)
        self.guess_entry = tk.Entry(root, font=("Arial", 12))  # Input field for guesses
        self.guess_entry.pack(pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")  # Label to display results
        self.result_label.pack(pady=5)

        self.history_label = tk.Label(root, text="History:", font=("Arial", 12))  # History section label
        self.history_label.pack(pady=5)

        self.history_text = tk.Text(root, height=10, width=50, font=("Arial", 10))  # Text box for guess history
        self.history_text.pack(pady=5)

        # Buttons for game actions
        tk.Button(root, text="Submit", font=("Arial", 12), command=self.submit_guess).pack(pady=5)
        tk.Button(root, text="Restart", font=("Arial", 12), command=self.restart_game).pack(pady=5)

    def submit_guess(self):
        """
        Handle the submission of a guess, calculate feedback, update the game state,
        and display results, including entropy and mutual information.
        """
        guess = self.guess_entry.get().strip()  # Get the player's guess

        # Validate the input (must be 4 unique digits)
        if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != len(guess):
            messagebox.showerror("Invalid Input", "Please enter a 4-digit number with unique digits.")
            return

        # Calculate Bulls and Cows feedback
        bulls, cows = get_feedback(self.secret, guess)

        # Calculate entropy and mutual information
        initial_entropy = calculate_entropy(self.possible_numbers)  # Entropy before filtering

        # Filter possible numbers based on the feedback
        filtered_possibilities = [
            num for num in self.possible_numbers if get_feedback(num, guess) == (bulls, cows)
        ]

        # Calculate updated entropy and mutual information
        updated_entropy = calculate_entropy(filtered_possibilities)
        mutual_information = initial_entropy - updated_entropy

        # Update the game's possible numbers
        self.possible_numbers = filtered_possibilities
        # Update the history and result labels
        self.history_text.insert(
            tk.END,
            f"Guess: {guess}, Bulls: {bulls}, Cows: {cows}, Entropy: {updated_entropy:.4f}, Mutual Info: {mutual_information:.4f}\n"
        )
        self.history_text.see(tk.END)  # Auto-scroll to the latest guess
        self.result_label.config(
            text=(
                f"Bulls: {bulls}, Cows: {cows}\n"
                f"Entropy: {updated_entropy:.4f}\n"
                f"Mutual Information: {mutual_information:.4f}"
            )
        )

        # Check if the player has guessed the secret number
        if bulls == 4:
            messagebox.showinfo("Congratulations!", f"You guessed the number {self.secret}!")
            self.restart_game()

        # Handle edge case where no possible numbers remain
        if not self.possible_numbers:
            messagebox.showerror("Error", "No possible numbers remain. Restarting game.")
            self.restart_game()

    def restart_game(self):
        """
        Restart the game by resetting the secret number, possible numbers, and UI components.
        """
        self.secret = ''.join(random.sample("0123456789", 4))  # Generate a new secret number
        self.possible_numbers = generate_possible_numbers(4)  # Reset possible numbers
        self.history_text.delete(1.0, tk.END)  # Clear the guess history
        self.result_label.config(text="")  # Clear the result label


# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = BullsAndCowsGame(root)
    root.mainloop()
