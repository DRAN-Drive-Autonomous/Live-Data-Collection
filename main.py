import cv2
import numpy as np
from PIL import ImageGrab
import time
import pandas as pd
import os
from grabScreen import grab_screen
from getKeys import key_check

W = [1,0,0,0,0,0,0,0,0,0]
A = [0,1,0,0,0,0,0,0,0,0]
S = [0,0,1,0,0,0,0,0,0,0]
D = [0,0,0,1,0,0,0,0,0,0]
WA = [0,0,0,0,1,0,0,0,0,0]
WD = [0,0,0,0,0,1,0,0,0,0]
SA = [0,0,0,0,0,0,1,0,0,0]
SD = [0,0,0,0,0,0,0,1,0,0]
SPACE = [0,0,0,0,0,0,0,0,1,0]
NOKEY = [0,0,0,0,0,0,0,0,0,1]

# keys will be one-hot encoded as [W, A, S, D, WA, WD, SA, SD, Space, NoKey]
filename = "./dataset/labels/keys.csv"

if os.path.exists(filename):
    df = pd.read_csv(filename)
    data = df.to_dict('list')
    print("Data found")
    print(len(data["filename"]))
else:
    data = {"filename":[], "keys":[], "W": [], "A":[], "S":[], "D":[], "WA":[], "WD":[], "SA":[], "SD":[], "Space":[], "NoKey":[]}

def keysToOutput(keys):
    output = [0,0,0,0,0,0,0,0,0,0]
    if 'W' in keys and 'A' in keys:
        output = WA
    elif 'W' in keys and 'D' in keys:
        output = WD
    elif 'S' in keys and 'A' in keys:
        output = SA
    elif 'S' in keys and 'D' in keys:
        output = SD
    elif 'W' in keys:
        output = W
    elif 'A' in keys:
        output = A
    elif 'S' in keys:
        output = S
    elif 'D' in keys:
        output = D
    elif ' ' in keys:
        output = SPACE
    else:
        output = NOKEY
    return output

def writeData(count, output):
    data["filename"].append(f"{count:07d}.png")
    data["keys"].append(output)
    data["W"].append(output[0])
    data["A"].append(output[1])
    data["S"].append(output[2])
    data["D"].append(output[3])
    data["WA"].append(output[4])
    data["WD"].append(output[5])
    data["SA"].append(output[6])
    data["SD"].append(output[7])
    data["Space"].append(output[8])
    data["NoKey"].append(output[9])

def countdown(num):
    for i in list(range(num))[::-1]:
        print(i+1)
        time.sleep(1)
    print("Go")

def main():
    count = len(data["filename"]) + 1
    print("Count Start Value:", count)
    countdown(10)
    last_time = time.time()
    timeL = []
    paused = False
    while True:
        if not paused:
            screen = grab_screen(region=(0,40,800,630))
            keys = key_check()
            output = keysToOutput(keys)
            writeData(count, output)
            cv2.imwrite(f"./dataset/images/{count:07d}.png",cv2.cvtColor(screen, cv2.COLOR_RGB2BGR))
            timeL.append(time.time()-last_time)
            last_time = time.time()
            cv2.imshow('window2',cv2.cvtColor(screen, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                df = pd.DataFrame(data)
                df.to_csv(filename, mode="w", header=True, index=False)
                break
            if count % 100 == 0:
                df = pd.DataFrame(data)
                df.to_csv(filename, mode="w", header=True, index=False)
                print("Data Saved")
            count += 1

        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print("Unpaused")
            else:
                paused = True
                print("Paused")
            time.sleep(1)
    print("FPS:", len(timeL) / sum(timeL))

if __name__ == "__main__":
    main()
