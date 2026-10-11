import os
import sys

def r_word():
    try:
        left_list = []
        right_list = []
        with open('word.txt', 'r') as file:
                for line in file:
                    line = line.strip()
                    if '-' in line:
                        left, right = line.split('-', 1)
                        left_list.append(left.strip())
                        right_list.append(right.strip())
                        
                return left_list, right_list
    
    except:
          return 0
                    
def w_word(data):
    try:
        with open('word.txt', 'w') as file:
            for item in data:
                file.write(str(item), + '\n')
    except:
        return 0