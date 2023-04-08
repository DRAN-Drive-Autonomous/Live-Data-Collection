import cv2
import numpy as np
from PIL import ImageGrab
import time
import pandas as pd
import os
import colorama
from grabScreen import grab_screen
from getKeys import key_check

directoryname = './dataset'

filename = os.path.join(directoryname, "labels/keys.csv")

greenTerminal = colorama.Fore.GREEN
redTerminal = colorama.Fore.RED
cyanTerminal = colorama.Fore.CYAN
yellowTerminal = colorama.Fore.YELLOW

if os.path.exists(filename):
    df = pd.read_csv(filename)
    data = df.to_dict('list')
    print("Data found")
    print(len(data["filename"]))
else:
    data = {"filename": [], "Throttle Value": [], "Throttle State": [], "Steering Value": [], "Steering State": []}


def keysToOutput(keys):
    output = []
    if "W" in keys:
        output.append(1)
        output.append(1)
    elif "S" in keys:
        output.append(0)
        output.append(1)
    else:
        output.append(0.5)
        output.append(0)

    if "A" in keys:
        output.append(1)
        output.append(1)
    elif "D" in keys:
        output.append(0)
        output.append(1)
    else:
        output.append(0.5)
        output.append(0)

    return output


def getRadar(image):
    img = image.copy()
    startX = 28
    startY = 873
    endX = 300
    endY = 1045

    img = img[startY:endY, startX:endX]

    for j, y in enumerate(img):
        for i, x in enumerate(y):
            if x[0] == 243 and x[1] == 84 and x[2] == 168:
                img[j][i] = 255
            else:
                img[j][i] = 0

    img = cv2.resize(img, (128, 128))
    return img


def getSpeed(image):
    img = image.copy()
    startX = 125
    startY = 843
    endX = 173
    endY = 869

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = img[startY:endY, startX:endX]

    img = cv2.resize(img, (128, 128))
    for j, y in enumerate(img):
        for i, x in enumerate(y):
            if x > 150:
                img[j][i] = 255
            else:
                img[j][i] = 0

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def mergeImages(img1, img2, img3):
    startX = 20
    startY = 839
    endX = 300
    endY = 1060
    img1[startY:endY, startX:endX] = [0, 0, 0]
    img1 = cv2.resize(img1, (256, 256))
    finalImg = np.zeros((384, 256, 3), dtype="uint8")
    finalImg[:256, :, :] = img1
    finalImg[256:384, :128, :] = img2
    finalImg[256:384, 128:, :] = img3
    return finalImg


def writeData(count, output):
    data["filename"].append(f"{count:07d}.png")
    # data["keys"].append(output)
    data["Throttle Value"].append(output[0])
    data["Throttle State"].append(output[1])
    data["Steering Value"].append(output[2])
    data["Steering State"].append(output[3])


def countdown(num):
    for i in list(range(num))[::-1]:
        value = '0' + str(i + 1)
        value = value[-2:]
        print(yellowTerminal + f"\r{value}", end="")
        time.sleep(1)
    print(greenTerminal + "\nGo")


def main():
    print("GTA-V Dataset Creator\nPress T to pause/play\nPress Q to quit\n\n")
    count = len(data["filename"]) + 1
    print("Count Start Value:", count)
    countdown(10)
    last_time = time.time()
    timeL = []
    paused = True
    print(redTerminal + "Paused")
    while True:
        if not paused:
            screen = grab_screen(region=(0, 0, 1920, 1080))

            keys = key_check()
            output = keysToOutput(keys)
            writeData(count, output)

            img = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
            img1 = getRadar(img)
            img2 = getSpeed(img)
            finalImg = mergeImages(img, img1, img2)
            cv2.imwrite(os.path.join(directoryname, f"images/{count:07d}.png"), finalImg)

            timeL.append(time.time() - last_time)
            last_time = time.time()

            if count % 100 == 0:
                df = pd.DataFrame(data)
                df.to_csv(filename, mode="w", header=True, index=False)
                fps = len(timeL) / sum(timeL)
                print(cyanTerminal + f"Data Saved till {count}. FPS: {fps}")
            count += 1

        keys = key_check()

        if 'Q' in keys:
            # cv2.destroyAllWindows()
            df = pd.DataFrame(data)
            df.to_csv(filename, mode="w", header=True, index=False)
            fps = len(timeL) / sum(timeL)
            print(cyanTerminal + f"Data Saved till {count}. FPS: {fps}")
            break

        if 'T' in keys:
            if paused:
                paused = False
                print(greenTerminal + "Played")
            else:
                paused = True
                print(redTerminal + "Paused")
            time.sleep(1)
    print(colorama.Fore.RESET)


if __name__ == "__main__":
    main()
