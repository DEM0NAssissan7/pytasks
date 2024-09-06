#!/bin/python3

from enum import Enum

import subprocess
import os
from sys import argv

# Ensure the program has root permissions
def needsroot():
    if os.getuid() != 0:
        print("This program must be run as root.")
        exit()

# General functions
def prompt(message, default):
    yes_no_prompt = "[Y/n]"
    _default = True
    if default == False:
        yes_no_prompt = "[y/N]"
        _default = False
    i = input(message + " " + yes_no_prompt + ": ").lower()

    if i == "":
        return _default

    if i == "y" or i == "yes":
        return True

    if i == "n" or i == "no":
        return False

def new_section(title):
    longline = "<------------------------------>"
    print("\n" + longline)
    print(title)
    print(longline + "\n")

def finished_section(title):
    longline = "------>"
    print("\n" + longline + " Finished task '" + title + "'\n")


# Tasks
tasks = []
prerun_script = ""
shell_exec = "/bin/sh"

def prerun(script):
    global prerun_script
    prerun_script = script

system_needs_reboot=False
class Task:
    name="Task"
    script="echo Task"
    selected=True
    reboot=False
    def __init__(self, name, script, *args, **kwargs):
        self.name = name
        self.script = script
        self.reboot = kwargs.get("reboot", False)
        self.selected = kwargs.get("selected", False)
        tasks.append(self)

    def run(self):
        new_section("Running task '" + self.name + "'...")
        subprocess.run(prerun_script + self.script, shell=True, executable=shell_exec)
        finished_section(self.name)
        # If a service needs to reboot, we prompt the user at the end to reboot if they want
        global system_needs_reboot
        system_needs_reboot = system_needs_reboot or self.reboot
    
    def get_selected_status(self):
        if self.selected == True:
            return "X"
        if self.selected == False:
            return " "
    
    def enable(self):
        self.selected = True
    
    def disable(self):
        self.selected = False
    
    def toggle(self):
        if self.selected == True:
            self.disable()
        elif self.selected == False:
            self.enable()
        return self.selected

# User task selection
def show_tasks():
    i = 0
    for task in tasks:
        i = i + 1
        print("[" + task.get_selected_status() + "] ("+str(i)+"): " + task.name)

def show_prompt_info():
    os.system("clear")
    print()
    print("Tasks:")
    show_tasks()
    print()
    print("Enter number (e.g '1' or '2') to toggle selection")
    print()
    print("You may specify multiple tasks separated by a space (e.g. '1 2 5 6')")
    print()
    print("To enable all tasks, input 'e'")
    print("To disable all tasks, input 'd'")
    print()
    print("To QUIT, input 'q'")
    print()

def prompt_task_selection():
    show_prompt_info()
    while True:
        i = input("Selection (or type 'i' to begin installation): ").lower()
        if "e" in i:
            for task in tasks:
                task.enable()
            show_prompt_info()
        elif "d" in i:
            for task in tasks:
                task.disable()
            show_prompt_info()
        elif "q" in i:
            quit_program()
            break
        elif "i" in i:
            break
        else:
            i = i.split(" ")
            try:
                for num in i:
                    tasks[int(num) - 1].toggle()
                show_prompt_info()
            except:
                continue

def run_selected_tasks():
    for task in tasks:
        if task.selected == True:
            task.run()

def finalize():
    for i in range(5):
        print()
    new_section("Tasks completed!")
    if system_needs_reboot == True:
        prompt_reboot()

def quit_program():
    for i in range(5):
        print()
    print("Exiting...")
    exit()
    
def prompt_reboot():
    # os.system("clear")
    i = prompt("To finalize the installation, would you like to restart your computer?", "n")
    if i == True:
        os.system("systemctl reboot")
        


# The last thing that runs in the config
def run_tasks():
    prompt_task_selection()
    # After user made selection
    run_selected_tasks()
    finalize()
    quit_program()