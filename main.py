import tkinter as tk
import subprocess
import sys

class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("310x400")
        self.root.configure(bg="#050734") 
        
        # Create a frame to hold the content
        frame = tk.Frame(self.root, bg="#050734")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the heading label
        heading_label = tk.Label(frame, text="Tic Tac Toe", font=("sans-serif", 50), bg="#050734", fg="white")
        heading_label.pack(pady=(20, 40))  # Add vertical padding
        
        # Create the buttons
        button1vs1 = tk.Button(frame, text="1vs1", command=self.launch_game_1vs1, width=15, height=2, font=("sans-serif", 20))
        button1vs1.pack(pady=10)  # Add vertical padding
        button1vsPC = tk.Button(frame, text="1vsCPU", command=self.launch_game_1vsPC, width=15, height=2, font=("sans-serif", 20))
        button1vsPC.pack()  # No vertical padding
        
    def launch_game_1vs1(self):
        self.root.destroy()  # Close the main menu window
        self.launch_game("game1vs1.py")
        
    def launch_game_1vsPC(self):
        self.root.destroy()  # Close the main menu window
        self.launch_game("game1vsPC.py")
        
    def launch_game(self, script_name):
        python_executable = sys.executable  # Get the Python interpreter path
        subprocess.Popen([python_executable, script_name])  # Launch the game interface
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.run()
