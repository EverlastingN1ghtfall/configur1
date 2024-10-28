from os import curdir
import tkinter as tk
import tarfile
from tkinter import scrolledtext

class LinuxConsole(tk.Tk):
    cur_path = ""

    def __init__(self, path):
        super().__init__()

        self.file = tarfile.open(path, mode='r')
        self.files = self.file.getnames()

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

        #self.prompt.pack(side=tk.LEFT)

    def execute_command(self, event=None):
        command = self.input_entry.get()
        self.input_entry.delete(0, tk.END)

        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"user@host:~$ {command}\n")
        self.output_text.config(state=tk.DISABLED)

        self.output_text.see(tk.END)

        if command.split()[0] == "ls":
            self.command_ls()
        elif command.split()[0] == "cd":
            self.command_cd(command.split()[1])

    def command_ls(self):
        self.output_text.config(state=tk.NORMAL)
        for i in self.files:
            if i[:len(self.cur_path)] == self.cur_path and '/' not in i[len(self.cur_path):]:
                self.output_text.insert(tk.END, f"{i[len(self.cur_path):]}    ")

        self.output_text.insert(tk.END, "\n")
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)

    def command_cd(self, arg):
        if arg[0] == '/':
            arg = arg[1:]
            slash_pos = arg.rfind('/')
            if slash_pos == -1:
                dest = arg
            else:
                dest = arg[slash_pos+1:]
            for i in self.files:
                if i == arg and (dest.count('.') == 0 or (dest.count('.') == 1 and dest[0] == '.')):
                    self.cur_path = arg + '/'
                    return
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"Destination invalid or was not found: {arg}\n")
            self.output_text.config(state=tk.DISABLED)
            self.output_text.see(tk.END)
        elif arg[:2] == "..":
            nodes = arg.split('/')
            path_nodes = self.cur_path.split('/')
            up_count = nodes.count("..")
            path_count = len(path_nodes)
            if up_count > path_count + 1:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, "Unable to move upwards\n")
                self.output_text.config(state=tk.DISABLED)
                return
            if up_count == path_count + 1 and (up_count == len(nodes) or (up_count == len(nodes) + 1 and nodes[-1] == "")):
                self.cur_path = ""
                return
            for i in range(up_count - 1, -1, -1):
                if nodes[i] == "..":
                    nodes[i] = path_nodes[len(path_nodes) - 1 - i]
            arg = '/' + '/'.join(path_nodes[:len(path_nodes) - up_count]) + '/' + '/'.join(nodes)
            self.command_cd(arg)


                


if __name__ == "__main__":
    path = "files.tar"
    
    app = LinuxConsole(path)
    app.mainloop()