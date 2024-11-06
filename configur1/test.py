import pytest
import tkinter as tk
from configur1.configur1 import LinuxConsole


def test_ls1():
    app = LinuxConsole('files.tar', 'a', 'b')
    app.command_ls_cur()
    inp = app.output_text.get("1.0", tk.END)

    assert inp.split('    ')[:-1] == ['data', 'docs', 'imgs']

def test_ls2():
    app = LinuxConsole('files.tar', 'a', 'b')
    app.command_ls("docs")
    inp = app.output_text.get("1.0", tk.END)

    assert inp.split('    ')[:-1] == ['text.txt', 'ИКБО-50-23 конфигур.pdf', 'ПнЯД_практика_7.pdf']

def test_cd1():
    app = LinuxConsole('files.tar', 'a', 'b')
    app.command_cd("/imgs/space")

    assert app.cur_path == "imgs/space/"

def test_cd2():
    app = LinuxConsole('files.tar', 'a', 'b')
    app.command_cd("/imgs/space/1")
    inp = app.output_text.get("1.0", tk.END)

    assert inp == "Destination was not found: imgs/space/1\n\n"

def test_echo1():
    app = LinuxConsole('files.tar', 'a', 'b')
    text = "abcde abcde abcde"
    app.command_echo(text.split())
    inp = app.output_text.get("1.0", tk.END)

    assert inp == f"{text}\n\n"

def test_echo2():
    app = LinuxConsole('files.tar', 'a', 'b')
    text = "testing echo 123"
    app.command_echo(text.split())
    inp = app.output_text.get("1.0", tk.END)

    assert inp == f"{text}\n\n"

def test_chown1():
    app = LinuxConsole('files.tar', 'a', 'b')
    app.command_chown("Artem:abcd", "abracadabra.txt")
    inp = app.output_text.get("1.0", tk.END)

    assert inp == "Destination was not found: abracadabra.txt\nInvalid path\n\n"

def test_chown2():
    app = LinuxConsole('files.tar', 'a', 'b')
    app.command_chown("Artem:abcd", "imgs")
    inp = app.output_text.get("1.0", tk.END)

    assert inp == "Reassign successful\n\n"
