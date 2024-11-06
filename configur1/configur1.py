from os import curdir
import tkinter as tk
import tarfile
import tomllib
from tkinter import scrolledtext

class LinuxConsole(tk.Tk):
    cur_path = ""

    def __init__(self, path, name, host):
        super().__init__()
        self.name = name
        self.host = host

        self.file = tarfile.open(path, mode='r')
        self.files = self.file.getnames()
        self.full_files = self.file.getmembers()

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
        req = self.input_entry.get()
        command = req.split(' ')[0]
        self.input_entry.delete(0, tk.END)

        if self.cur_path != "":
            output_string = f"{self.name}@{self.host}:{self.cur_path}$"
        else:
            output_string = f"{self.name}@{self.host}:~$"
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"{output_string} {req}\n")
        self.output_text.config(state=tk.DISABLED)

        self.output_text.see(tk.END)

        if command == "ls" and len(req.split()) == 1:
            self.command_ls_cur()
        elif command == "ls" and len(req.split()) == 2:
            self.command_ls(req.split()[1])
        elif command == "ls" and len(req.split()) == 3 and len(req.split())[1] == "-l":
            self.command_ls(req.split()[1], True)
        elif command == "cd" and len(req.split()) == 2:
            code = self.command_cd(req.split()[1])
            if code == -2:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, f"Destination invalid: {req.split()[1]}\n")
                self.output_text.config(state=tk.DISABLED)
                self.output_text.see(tk.END)
        elif command == "exit":
            exit(1)
        elif command == "echo" and len(req.split()) >= 2:
            self.command_echo(req.split()[1:])

    def command_ls_cur(self):
        self.output_text.config(state=tk.NORMAL)
        for i in self.files:
            if i[:len(self.cur_path)] == self.cur_path and '/' not in i[len(self.cur_path):]:
                self.output_text.insert(tk.END, f"{i[len(self.cur_path):]}    ")

        self.output_text.insert(tk.END, "\n")
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)

    def command_ls(self, arg: str, flag: bool = False):
        if not flag:
            path = self.cur_path
            code = self.command_cd(arg)
            if code == -1:
                return
            self.command_ls_cur()
            self.cur_path = path
            return

    def command_chown(self, toassign: str, file: str):
        ind = self.find(file)
        if ind <= 0:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "Invalid path\n")
            self.output_text.config(state=tk.DISABLED)
            self.output_text.see(tk.END)
            return

        usr = ""
        group = ""
        if toassign.count(':') == 1:
            assigns = toassign.split(':')
            usr = assigns[0]
            group = assigns[1]
        else:
            usr = toassign

        if usr != "":
            self.full_files[ind].uname = usr
        if group != "":
            self.full_files[ind].gname = group

        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "Reassign successful\n")
        self.output_text.config(state=tk.DISABLED)

    def find(self, arg: str):
        if arg[0] == '/':
            if arg[-1] == '/':
                arg = arg[:-1]
            arg = arg[1:]
            for i in range(len(self.files)):
                if self.files[i] == arg:
                    return i
            return -1
        elif arg[:2] == "..":
            nodes = arg.split('/')
            path_nodes = self.cur_path.split('/')
            path_nodes.remove("")
            up_count = nodes.count("..")
            path_count = len(path_nodes)
            if up_count > path_count + 1:
                return -1
            if up_count == path_count and (up_count == len(nodes) or (up_count == len(nodes) + 1 and nodes[-1] == "")):
                return -3
            arg = '/'.join(path_nodes[:len(path_nodes) - up_count]) + '/' + '/'.join(nodes[up_count:])
            if arg[0] != '/':
                arg = '/' + arg
            return self.command_cd(arg)
        else:
            return self.command_cd('/' + self.cur_path + arg)

    def command_cd(self, arg: str):
        if arg[0] == '/':
            if arg[-1] == '/':
                arg = arg[:-1]
            arg = arg[1:]
            for i in range(len(self.files)):
                if self.files[i] == arg and self.full_files[i].isdir():
                    self.cur_path = arg + '/'
                    return i
                elif self.files[i] == arg and self.full_files[i].isfile():
                    return -2
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"Destination was not found: {arg}\n")
            self.output_text.config(state=tk.DISABLED)
            self.output_text.see(tk.END)
            return -1
        elif arg[:2] == "..":
            nodes = arg.split('/')
            path_nodes = self.cur_path.split('/')
            path_nodes.remove("")
            up_count = nodes.count("..")
            path_count = len(path_nodes)
            if up_count > path_count + 1:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, "Unable to move upwards\n")
                self.output_text.config(state=tk.DISABLED)
                return -1
            if up_count == path_count and (up_count == len(nodes) or (up_count == len(nodes) + 1 and nodes[-1] == "")):
                self.cur_path = ""
                return -3
            arg = '/'.join(path_nodes[:len(path_nodes) - up_count]) + '/' + '/'.join(nodes[up_count:])
            if arg[0] != '/':
                arg = '/' + arg
            return self.command_cd(arg)
        else:
            return self.command_cd('/' + self.cur_path + arg)

    def command_echo(self, line: list):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"{' '.join(line)}\n")
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)


def parse_toml(path:str):
    a = open(path, "rb")
    data = tomllib.load(a)
    a.close()
    return data


if __name__ == "__main__":
    mas = parse_toml("conf.toml")
    path = mas["project"]["path"]
    name = mas["project"]["usr"]
    host = mas["project"]["host"]
    start = mas["project"]["start"]
    
    app = LinuxConsole(path, name, host)
    app.mainloop()