import tkinter as tk
from tkinter import messagebox
from subprocess import Popen, PIPE
import json
import re

class TicTacToeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_turn = 'x'  # X always starts
        self.create_widgets()
        self.init_prolog_game()
        self.root.geometry("310x400")
        self.root.configure(bg="#050734") 
        

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="#050734")  # Create a frame to hold the buttons
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

        for i in range(3):
            for j in range(3):
                button = tk.Button(frame, text="", width=6, height=7, command=lambda i=i, j=j: self.handle_click(i, j))
                button.grid(row=i, column=j, padx=4, pady=4)  # Add padding to each button
                self.buttons[i][j] = button

    def handle_click(self, i, j):
        if self.buttons[i][j]['text'] == "":
            self.buttons[i][j]['text'] = self.current_turn  # Update immediately in GUI
            self.buttons[i][j]['state'] = 'disabled'  # Disable the button after clicking
            self.buttons[i][j].configure(disabledforeground='#050734')  # Set blue color for "x"
            self.buttons[i][j].configure(font=('sans-serif', 89))  # Change text font and size
            self.buttons[i][j].configure(width=1, height=1)  # Set a fixed size for the button
            self.root.update_idletasks()  # Update GUI immediately
            self.make_move(self.current_turn, i + 1, j + 1)
            

    def make_move(self, player, row, col):
        command = f"jugada('{player}', {row}, {col}).\n"
        self.prolog.stdin.write(command.encode())
        self.prolog.stdin.flush()
        self.process_prolog_output()

    def process_prolog_output(self):
        output_lines = []
        while True:
            output = self.prolog.stdout.readline().decode().strip()
            if output:
                output_lines.append(output)
            if "El ganador es" in output or "El juego es un empate" in output or output == "false.":
                break
        
        for output in output_lines:
            print(f"Prolog output: {output}")  # Debug print
            if "El ganador es" in output:
                self.show_winner(output)
                return
            elif "El juego es un empate" in output:
                self.show_winner(output)
                return
            elif re.match(r'\[\[.*\]\]', output):  # Match the matrix output
                self.update_board(output)
        
        # Toggle turn after processing the output
        self.current_turn = 'o' if self.current_turn == 'x' else 'x'

    def update_board_from_prolog(self):
        # Request the current board state and update the GUI
        self.prolog.stdin.write("mostrar_matriz.\n".encode())
        self.prolog.stdin.flush()

        while True:
            output = self.prolog.stdout.readline().decode().strip()
            if re.match(r'\[\[.*\]\]', output):  # Match the matrix output
                self.update_board(output)
                break
            else:
                print(f"Ignored Prolog output: {output}")

    def update_board(self, prolog_output):
        try:
            # Convert Prolog list output to JSON-compatible format
            matrix = json.loads(prolog_output.replace("'", "\""))
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j]['text'] = matrix[i][j] if matrix[i][j] != '-' else ""
                    self.buttons[i][j]['state'] = 'normal' if matrix[i][j] == '-' else 'disabled'
        except json.JSONDecodeError as e:
            print(f"Failed to parse Prolog output: {prolog_output} ({e})")

    def init_prolog_game(self):
        # Replace 'swipl' with the full path to swipl if necessary
        self.prolog = Popen(['swipl', '-q', '-f', 'tic_tac_toe.pl', '-g', 'iniciar_juego'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.update_board_from_prolog()

    def show_winner(self, message):
        for row in self.buttons:
            for button in row:
                button['state'] = 'disabled'
        winner_message = message
        messagebox.showinfo("Game Over", winner_message)
        
        # Create and display the restart button
        restart_button = tk.Button(self.root, text="Restart Game", command=self.restart_game)
        restart_button.pack()

        self.prolog.terminate()  # Terminate the Prolog process

    def restart_game(self):
        # Destroy the root window and restart the application
        self.root.destroy()
        self.__init__()  # Reinitialize the application
        self.run()  # Start the game again

    def run(self):
        self.root.mainloop()
        self.prolog.terminate()

if __name__ == "__main__":
    app = TicTacToeApp()
    app.run()