import cv2
import numpy as np
import pandas as pd
import os

pathRoot = "./dataset/images/"

keysPath = "./dataset/labels/keys.csv"

keysDF = pd.read_csv(keysPath)

keysDF = keysDF.to_dict('list')

currentCount = len(keysDF["filename"])

print(f"Count -> {currentCount}")

def imageForm(imgCam, imgRadar, imgSpeed, count):
    finalImg = np.zeros((384, 256, 3), dtype="uint8")
    finalImg[:256, :, :] = imgCam
    finalImg[256:384, :128, :] = imgRadar
    finalImg[256:384, 128:, :] = imgSpeed
    cv2.imwrite(os.path.join(pathRoot, f"{count:07d}.png"), finalImg)
    return

def flippingCam(imgCam, imgRadar, imgSpeed, count):
    temp = imgCam.copy()
    flipped_image = cv2.flip(temp, 1)
    imageForm(flipped_image, imgRadar, imgSpeed, count)
    return

def flippingRad(imgCam, imgRadar, imgSpeed, count):
    temp = imgRadar.copy()
    flipped_image = cv2.flip(temp, 1)
    imageForm(imgCam, flipped_image, imgSpeed, count)
    return

def incBrightness(imgCam, imgRadar, imgSpeed, count):
    temp = imgCam.copy()
    beta = np.random.randint(low=10, high=50)
    image2 = cv2.convertScaleAbs(temp, alpha=1, beta=beta)
    imageForm(image2, imgRadar, imgSpeed, count)
    return

def decBrightness(imgCam, imgRadar, imgSpeed, count):
    temp = imgCam.copy()
    beta = np.random.randint(low=-50, high=-10)
    image2 = cv2.convertScaleAbs(temp, alpha=1, beta=beta)
    imageForm(image2, imgRadar, imgSpeed, count)
    return

def incContrast(imgCam, imgRadar, imgSpeed, count):
    temp = imgCam.copy()
    alpha = (np.random.randint(low=100, high=200))/100
    image2 = cv2.convertScaleAbs(temp, alpha=alpha, beta=0)
    imageForm(image2, imgRadar, imgSpeed, count)
    return

def decContrast(imgCam, imgRadar, imgSpeed, count):
    temp = imgCam.copy()
    alpha = (np.random.randint(low=25, high=100))/100
    image2 = cv2.convertScaleAbs(temp, alpha=alpha, beta=0)
    imageForm(image2, imgRadar, imgSpeed, count)
    return

def noising(imgCam, imgRadar, imgSpeed, count):
    temp = imgCam.copy()
    noise_mean = 0
    noise_stddev = np.random.randint(low=100, high=200)/100
    height, width, channels = temp.shape
    noise = np.random.normal(noise_mean, noise_stddev, (height, width, channels)).astype(np.uint8)
    noisy_image = cv2.add(temp, noise)
    imageForm(noisy_image, imgRadar, imgSpeed, count)
    return

def blurring(imgCam, imgRadar, imgSpeed, count):
    temp = imgCam.copy()
    randVal = ((np.random.randint(low=1, high=4))*2)+1
    kernel_size = (randVal, randVal)
    blurred_image = cv2.GaussianBlur(temp, kernel_size, 0)
    imageForm(blurred_image, imgRadar, imgSpeed, count)
    return

def writeData(count, output):
    keysDF["filename"].append(f"{count:07d}.png")
    # data["keys"].append(output)
    keysDF["Throttle Value"].append(output[0])
    keysDF["Throttle State"].append(output[1])
    keysDF["Steering Value"].append(output[2])
    keysDF["Steering State"].append(output[3])


for ind in range(len(keysDF["filename"])):
    steeringFlag = keysDF["Steering State"][ind]
    throttleVal = keysDF["Throttle Value"][ind]
    filename = keysDF["filename"][ind]
    throttleFlag = keysDF["Throttle State"][ind]
    steeringVal = keysDF["Steering Value"][ind]
    
    # print(f"Augmentation for {filename}")

    if (steeringFlag == 1 or throttleVal == 0):
        print(f"Augmentation for {filename}")
        imgPath = os.path.join(pathRoot, filename)
        img = cv2.imread(imgPath)

        imgCamera = img.copy()
        imgRadar = img.copy()
        imgSpeed = img.copy()

        imgCamera = imgCamera[:256, :, :]
        imgRadar = imgRadar[256:384, :128, :]
        imgSpeed = imgSpeed[256:384, 128:, :]

        currentCount += 1
        flippingCam(imgCamera, imgRadar, imgSpeed, currentCount)
        writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])
        
        currentCount += 1
        flippingRad(imgCamera, imgRadar, imgSpeed, currentCount)
        steeringValN = (steeringVal+1)%2
        if (steeringValN == 1.5):
            steeringValN = 0.5
        writeData(currentCount, [throttleVal, throttleFlag, steeringValN, steeringFlag])

        currentCount += 1
        incBrightness(imgCamera, imgRadar, imgSpeed, currentCount)
        writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])

        currentCount += 1
        decBrightness(imgCamera, imgRadar, imgSpeed, currentCount)
        writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])

        currentCount += 1
        incContrast(imgCamera, imgRadar, imgSpeed, currentCount)
        writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])

        currentCount += 1
        decContrast(imgCamera, imgRadar, imgSpeed, currentCount)
        writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])

        temp = np.random.randint(low=0, high=2)
        if (temp == 1):
            currentCount += 1
            incBrightness(imgCamera, imgRadar, imgSpeed, currentCount)
            writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])
        else:
            currentCount += 1
            decBrightness(imgCamera, imgRadar, imgSpeed, currentCount)
            writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])

        temp = np.random.randint(low=0, high=2)
        if (temp == 1):
            currentCount += 1
            decContrast(imgCamera, imgRadar, imgSpeed, currentCount)
            writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])
        else:
            currentCount += 1
            incContrast(imgCamera, imgRadar, imgSpeed, currentCount)
            writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])
        
        # currentCount += 1
        # noising(imgCamera, imgRadar, imgSpeed, currentCount)
        # writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])

        currentCount += 1
        blurring(imgCamera, imgRadar, imgSpeed, currentCount)
        writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])
    # else:
    #     temp = np.random.randint(low=0, high=2)
    #     if (temp == 1):
    #         currentCount += 1
    #         incBrightness(imgCamera, imgRadar, imgSpeed, currentCount)
    #         writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])
    #     else:
    #         currentCount += 1
    #         decBrightness(imgCamera, imgRadar, imgSpeed, currentCount)
    #         writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])

    #     temp = np.random.randint(low=0, high=2)
    #     if (temp == 1):
    #         currentCount += 1
    #         decContrast(imgCamera, imgRadar, imgSpeed, currentCount)
    #         writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])
    #     else:
    #         currentCount += 1
    #         incContrast(imgCamera, imgRadar, imgSpeed, currentCount)
    #         writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])
    
    # currentCount += 1
    # noising(imgCamera, imgRadar, imgSpeed, currentCount)
    # writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])

    # currentCount += 1
    # blurring(imgCamera, imgRadar, imgSpeed, currentCount)
    # writeData(currentCount, [throttleVal, throttleFlag, steeringVal, steeringFlag])

keysDF = pd.DataFrame(keysDF)
keysDF.to_csv(keysPath, mode="w", header=True, index=False)