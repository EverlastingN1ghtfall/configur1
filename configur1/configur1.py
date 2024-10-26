import tkinter as tk
#from tkinter import ttk
from tkinter import scrolledtext

class LinuxConsole(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Linux Console")
        self.geometry("800x600")

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_text.config(state=tk.DISABLED)

        self.input_frame = tk.Frame(self)
        self.input_frame.pack(fill=tk.X)

        self.input_entry = tk.Entry(self.input_frame, width=80)
        self.input_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.input_entry.bind("<Return>", self.execute_command)

        self.prompt = tk.Label(self.input_frame, text="user@host:~$ ")
        self.prompt.pack(side=tk.LEFT)

    def execute_command(self, event=None):
        command = self.input_entry.get()
        self.input_entry.delete(0, tk.END)

        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"user@host:~$ {command}\n")
        self.output_text.config(state=tk.DISABLED)

        self.output_text.see(tk.END)

if __name__ == "__main__":
    app = LinuxConsole()
    app.mainloop()