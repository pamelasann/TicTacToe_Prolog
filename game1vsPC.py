import tkinter as tk
from tkinter import messagebox
from subprocess import Popen, PIPE
import re
import json
import threading

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()
        self.prolog = Popen(["swipl", "-q"], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True, bufsize=1, universal_newlines=True)
        self.initialize_prolog()
        self.root.geometry("310x400")
        self.root.configure(bg="#050734") 

    def create_board(self):
        frame = tk.Frame(self.root, bg="#050734")  # Create a frame to hold the buttons
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame
        for i in range(3):
            for j in range(3):
                button = tk.Button(frame, text="", width=6, height=7,
                                   command=lambda i=i, j=j: self.user_move(i, j))
                button.grid(row=i, column=j, padx=4, pady=4) 
                self.buttons[i][j] = button

    def initialize_prolog(self):
        threading.Thread(target=self.send_prolog_command, args=("consult('tic_tac_toe_computer.pl').\n",)).start()
        threading.Thread(target=self.send_prolog_command, args=("iniciar_juego.\n",)).start()


    def user_move(self, row, col):
        command = f"jugada(x, {row + 1}, {col + 1}).\n"
        threading.Thread(target=self.send_prolog_command, args=(command,)).start()

    def send_prolog_command(self, command):
        self.prolog.stdin.write(command)
        self.prolog.stdin.flush()
        self.process_prolog_output()

    def process_prolog_output(self):
        output_lines = []
        while True:
            output = self.prolog.stdout.readline().strip()
            if output:
                output_lines.append(output)
            if "El ganador es" in output or "El juego es un empate" in output or output == "false.":
                break
        
        for output in output_lines:
            print(f"Prolog output: {output}")  # Debug print
            if "El ganador es" in output or "El juego es un empate" in output:
                self.show_winner(output)
                return
            elif re.match(r'\[\[.*\]\]', output):  # Board state
                self.update_board(output)

    def update_board(self, board_string):
        board = json.loads(board_string.replace("'", '"'))
        for i in range(3):
            for j in range(3):
                if board[i][j] != '-':
                    self.buttons[i][j].config(text=board[i][j])
                    self.buttons[i][j].configure(disabledforeground='#050734')
                    self.buttons[i][j].configure(font=('sans-serif', 89)) 
                    self.buttons[i][j].configure(width=1, height=1) 
                    self.buttons[i][j].config(state=tk.DISABLED)
                else:
                    self.buttons[i][j].config(text="")

    def show_winner(self, message):
        if "El ganador es" in message:
            winner = re.search(r'El ganador es: (.)', message).group(1)
            messagebox.showinfo("Game Over", f"El ganador es: {winner}")
        elif "El juego es un empate" in message:
            messagebox.showinfo("Game Over", "El juego es un empate")
        self.disable_buttons()
        # Create and display the restart button
        restart_button = tk.Button(self.root, text="Restart Game", command=self.restart_game)
        restart_button.pack()
        self.prolog.terminate()
    
    def restart_game(self):
        # Destroy the root window and restart the application
        self.root.destroy()
        self.__init__()  # Reinitialize the application
        self.run()  # Start the game again


    def disable_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.DISABLED)
    
    def on_closing(self):
        # Terminate the subprocess when the window is closed
        self.prolog.terminate()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        self.prolog.terminate()

if __name__ == "__main__":
    app = TicTacToe()
    app.run()
