import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    BOARD_SIZE = 3

    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe Pro")
        self.root.resizable(False, False)

        # Players
        self.player1 = "Player 1"
        self.player2 = "Player 2"

        self.ask_player_names()

        # Scores
        self.x_score = 0
        self.o_score = 0
        self.draw_score = 0

        self.games_played = 0

        self.create_widgets()

        self.restart_game()

    def create_widgets(self):

        title = tk.Label(
            self.root, text="🎮 Tic Tac Toe Pro", font=("Arial", 18, "bold")
        )
        title.grid(row=0, column=0, columnspan=3, pady=10)

        self.turn_label = tk.Label(self.root, text="", font=("Arial", 13, "bold"))
        self.turn_label.grid(row=1, column=0, columnspan=3, pady=5)

        self.score_label = tk.Label(self.root, text="", font=("Arial", 11))
        self.score_label.grid(row=2, column=0, columnspan=3, pady=5)

        self.buttons = []

        for row in range(self.BOARD_SIZE):

            button_row = []

            for col in range(self.BOARD_SIZE):

                btn = tk.Button(
                    self.root,
                    text="",
                    width=6,
                    height=2,
                    font=("Arial", 24, "bold"),
                    command=lambda r=row, c=col: self.handle_click(r, c),
                )

                btn.grid(row=row + 3, column=col, padx=3, pady=3)

                button_row.append(btn)

            self.buttons.append(button_row)

        restart_btn = tk.Button(
            self.root, text="🔄 Restart Match", command=self.confirm_restart
        )

        restart_btn.grid(row=6, column=0, columnspan=3, sticky="ew", pady=5)

        stats_btn = tk.Button(
            self.root, text="📊 Statistics", command=self.show_statistics
        )

        stats_btn.grid(row=7, column=0, columnspan=3, sticky="ew", pady=5)

        reset_score_btn = tk.Button(
            self.root, text="🗑 Reset Scores", command=self.reset_scores
        )

        reset_score_btn.grid(row=8, column=0, columnspan=3, sticky="ew", pady=5)

    def ask_player_names(self):

        popup = tk.Toplevel(self.root)
        popup.title("Enter Player Names")
        popup.grab_set()

        tk.Label(popup, text="Player X Name").pack(pady=5)

        p1_entry = tk.Entry(popup)
        p1_entry.pack()

        tk.Label(popup, text="Player O Name").pack(pady=5)

        p2_entry = tk.Entry(popup)
        p2_entry.pack()

        def save():

            if p1_entry.get().strip():
                self.player1 = p1_entry.get().strip()

            if p2_entry.get().strip():
                self.player2 = p2_entry.get().strip()

            popup.destroy()

        tk.Button(popup, text="Start Game", command=save).pack(pady=10)

        self.root.wait_window(popup)

    def restart_game(self):

        self.board = [[""] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]

        self.current_player = "X"
        self.game_over = False
        self.moves = 0

        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):

                self.buttons[row][col].config(
                    text="", bg="SystemButtonFace", state="normal"
                )

        self.update_turn_label()
        self.update_scoreboard()

    def confirm_restart(self):

        answer = messagebox.askyesno("Restart", "Restart the current match?")

        if answer:
            self.restart_game()

    def handle_click(self, row, col):

        if self.game_over:
            return

        if self.board[row][col] != "":
            return

        self.board[row][col] = self.current_player

        color = "blue" if self.current_player == "X" else "red"

        self.buttons[row][col].config(text=self.current_player, fg=color)

        self.moves += 1

        winner, positions = self.check_winner()

        if winner:

            self.game_over = True
            self.games_played += 1

            for r, c in positions:
                self.buttons[r][c].config(bg="lightgreen")

            self.disable_board()

            winner_name = self.player1 if winner == "X" else self.player2

            if winner == "X":
                self.x_score += 1
            else:
                self.o_score += 1

            self.update_scoreboard()

            self.turn_label.config(text=f"🏆 {winner_name} Wins!")

            messagebox.showinfo("Winner", f"{winner_name} ({winner}) wins!")

            return

        if self.moves == 9:

            self.game_over = True
            self.games_played += 1
            self.draw_score += 1

            self.update_scoreboard()

            self.turn_label.config(text="🤝 Match Drawn!")

            messagebox.showinfo("Draw", "The match ended in a draw.")

            return

        self.switch_player()

    def switch_player(self):

        self.current_player = "O" if self.current_player == "X" else "X"

        self.update_turn_label()

    def update_turn_label(self):

        player = self.player1 if self.current_player == "X" else self.player2

        self.turn_label.config(text=f"🎯 {player}'s Turn ({self.current_player})")

    def update_scoreboard(self):

        self.score_label.config(
            text=(
                f"{self.player1} (X): {self.x_score}    "
                f"{self.player2} (O): {self.o_score}    "
                f"Draws: {self.draw_score}"
            )
        )

    def disable_board(self):

        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def check_winner(self):

        winning_positions = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]

        for combo in winning_positions:

            values = [self.board[r][c] for r, c in combo]

            if values[0] != "" and values.count(values[0]) == 3:
                return values[0], combo

        return None, None

    def show_statistics(self):

        messagebox.showinfo(
            "Statistics",
            (
                f"Games Played: {self.games_played}\n\n"
                f"{self.player1} Wins: {self.x_score}\n"
                f"{self.player2} Wins: {self.o_score}\n"
                f"Draws: {self.draw_score}"
            ),
        )

    def reset_scores(self):

        answer = messagebox.askyesno("Reset Scores", "Reset all scores?")

        if not answer:
            return

        self.x_score = 0
        self.o_score = 0
        self.draw_score = 0
        self.games_played = 0

        self.update_scoreboard()

        messagebox.showinfo("Reset", "Scores reset successfully.")


if __name__ == "__main__":

    root = tk.Tk()

    app = TicTacToe(root)

    root.mainloop()
