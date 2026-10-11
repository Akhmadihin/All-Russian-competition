import train

i = -1

train.init()

while True:
    i += 1
    print(train.left(i))
    
    answer = input()
    
    print(train.right(i, answer))
    
  