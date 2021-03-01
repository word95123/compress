import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

compress = 2

quantify = [[17,18,24,47,99,99,99,99],[18,21,26,66,99,99,99,99],[24,26,56,99,99,99,99,99],[47,66,99,99,99,99,99,99],
[99,99,99,99,99,99,99,99],[99,99,99,99,99,99,99,99],[99,99,99,99,99,99,99,99],[99,99,99,99,99,99,99,99]]

'''
quantify = [[16,11,10,16,24,40,51,61],[12,12,14,19,26,58,60,55],[14,13,16,24,40,57,69,56],[14,17,22,29,51,87,80,62],[18,22,37,56,68,109,103,77],[24,35,55,64,81,104,113,92]
,[49,64,78,87,103,121,120,101],[72,92,95,98,112,100,103,99]]
'''
for c in range(8):
    for s in range(8):
        quantify[c][s] = int(quantify[c][s] * (1-(compress/100)))
        if(quantify[c][s] == 0):
            quantify[c][s] = 1

def sub_dct(image):
    img = np.copy(image)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] -= 128
    return img

def add_idct(image):
    img = np.copy(image)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] += 128
    return img

def quantify_dct(image):
    img = np.copy(image)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = int(img[i][j] / quantify[i][j])
    return img

def quantify_idct(image):
    img = np.copy(image)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = int(img[i][j] * quantify[i][j])
    return img

def dct_transform(image):
    image_block = sub_dct(image)
    block_image = np.array([[0]*image_block.shape[0]]*image_block.shape[1])

    
    for i in range(0, image_block.shape[0]):
        for j in range(0, image_block.shape[1]):
            if(i == 0):
                cu = 1/math.sqrt(2)
            else:
                cu = 1.0
            if(j == 0):
                cv = 1/math.sqrt(2)
            else:
                cv = 1.0
            total = 0
            for bi in range(0, image_block.shape[0]):
                for bj in range(0, image_block.shape[1]):
                    Fuv = image_block[bi][bj] * math.cos((2*bi+1)*i*math.pi/16) * math.cos((2*bj+1)*j*math.pi/16)
                    total += Fuv

            block_image[i][j] = cu * cv * total / 4

    block_image = quantify_dct(block_image)
    return block_image

def idct_transform(image):
    image_block = quantify_idct(image)
    block_image = np.array([[0]*image_block.shape[0]]*image_block.shape[1])

    
    for i in range(0, image_block.shape[0]):
        for j in range(0, image_block.shape[1]):
            
            total = 0
            for bi in range(0, image_block.shape[0]):
                for bj in range(0, image_block.shape[1]):
                    if(bi == 0):
                        cu = 1/math.sqrt(2)
                    else:
                        cu = 1.0
                    if(bj == 0):
                        cv = 1/math.sqrt(2)
                    else:
                        cv = 1.0
                    Fuv = cu * cv * image_block[bi][bj] * math.cos((2*i+1)*bi*math.pi/16) * math.cos((2*j+1)*bj*math.pi/16)
                    total += Fuv
            block_image[i][j] =total / 4
    block_image = add_idct(block_image)
    return block_image

def dct(image, block):
    dct_image = np.array([[0]*image.shape[0]]*image.shape[1])
    image_block = np.array([[0]*block]*block)
    for i in range(0, image.shape[0], block):
        for j in range(0, image.shape[1], block):
            for bi in range(block):
                for bj in range(block):
                    image_block[bi][bj] = image[i+bi][j+bj]
            image_block = dct_transform(image_block)
            for bi in range(block):
                for bj in range(block):
                    dct_image[i+bi][j+bj] = image_block[bi][bj]
    return dct_image

def idct(image, block):
    idct_image = np.array([[0]*image.shape[0]]*image.shape[1])
    image_block = np.array([[0]*block]*block)
    for i in range(0, image.shape[0], block):
        for j in range(0, image.shape[1], block):

            for bi in range(block):
                for bj in range(block):
                    image_block[bi][bj] = image[i+bi][j+bj]
            image_block = idct_transform(image_block)
            for bi in range(block):
                for bj in range(block):
                    idct_image[i+bi][j+bj] = image_block[bi][bj]
    return idct_image



if __name__ == "__main__":
    image = cv2.imread('./other/compress/lena64.jpg',cv2.IMREAD_GRAYSCALE)
    print(image[0])
    
    image_dct = dct(image, 8)
    image_idct = idct(image_dct, 8)
    print(image_dct[0])
    print(image_idct[0])
    #cv2.imwrite('./other/compress/JEPGlena64.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 100])
    cv2.imwrite('./other/compress/JEPGlena64.jpg',image_idct)

    plt.figure(figsize=(15,5))
    plt.subplot(1,3,1)
    plt.imshow(image,cmap='gray')
    plt.subplot(1,3,2)
    plt.imshow(image_dct,cmap='gray')
    plt.subplot(1,3,3)
    plt.imshow(image_idct, cmap='gray')
    
    plt.show()
    