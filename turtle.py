import os
import random
import time

def matrix_rain():
    columns = 80
    drops = [0] * columns
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@$%&*"
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    try:
        while True:
            line = ""
            for i in range(columns):
                if random.random() < 0.05:
                    drops[i] = random.randint(5, 15)
                
                if drops[i] > 0:
                    line += random.choice(chars)
                    drops[i] -= 1
                else:
                    line += " "
            
            print("\033[32m" + line + "\033[0m")
            time.sleep(0.04)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    matrix_rain()