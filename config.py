import sys
import os

def r_config():
    with open ('config.txt', 'r') as f:
        data = f.read()
        
    return data

def w_config():
    with open ('config.txt', 'w') as f:
        f.write(data)

    return data
