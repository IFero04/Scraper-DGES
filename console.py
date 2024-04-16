import os
import time

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def add_dot_every_second(string):
    for _ in range(5): 
        string += "."
        print(string, end="\r")
        time.sleep(1)
