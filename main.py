import os
import numpy as np
import pandas as pd

from PIL import Image
import skimage.io as skiio
import skimage.color as skicol
import skimage.morphology as skimor
import matplotlib.pyplot as plt
import pytesseract

img = skiio.imread("fix.jpg")
img = Image.fromarray(img)
tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
text = pytesseract.image_to_string(img, lang="eng", config=tessdata_dir_config)
print(text)
plt.imshow(img)
plt.show()


def get_specific_color_mask(img, color, tol):
    green_img = np.zeros(shape=img.shape, dtype=np.int16)
    green_img[:, :] = color
    diff_img = np.abs(img.astype(np.int16) - green_img)
    diff_img = np.add.reduce(diff_img, axis=2)
    return (diff_img < tol).astype(np.uint8)



# Get image
img = skiio.imread("20170713224721.png")
img = skiio.imread("20170714154517.jpg")
if img.shape[2] == 4:
    img = img[:, :, 0:3]
plt.imshow(img, cmap="gray")
plt.show()
# img = (skicol.rgb2gray(img) * 4095).astype(np.uint16)
# plt.imshow(img, cmap="gray_r")
# plt.show()

# Get green record marks
green_mask = get_specific_color_mask(img, [59, 188, 44], 77)
green_mask = skimor.dilation(green_mask)
green_mask = skimor.label(green_mask)
# plt.imshow(green_mask, cmap="gray")
# plt.show()

# Get white mask and lines
white_mask = get_specific_color_mask(img, [255, 255, 255], 10)
for idx in range(0, 1):
    white_mask = skimor.erosion(white_mask)
# plt.imshow(white_mask, cmap="gray")
# plt.show()
is_white_lines = np.add.reduce(white_mask, axis=1)
# plt.subplot(121)
# plt.plot(is_white_lines)
is_white_lines = ((white_mask.shape[1] - is_white_lines) < 40).astype(np.uint8)
# plt.subplot(122)
# plt.plot(is_white_lines)
# plt.show()

# Separate into records
lsRecordImg, lsRecordWhiteLine, lsRecordMask = [], [], []
rowWhite0, rowWhite1, rowWhite2 = 0, 0, 0
for idx in np.unique(green_mask):
    if idx != 0:
        x = np.nonzero(green_mask == idx)
        rows, cols = np.nonzero(green_mask == idx)
        row, col = rows[0], cols[0]
        while True:
            if is_white_lines[row] == 0:
                row -= 1
            else:
                rowWhite2 = row - 3
                break
        if idx != 1:
            while True:
                if is_white_lines[row] == 1:
                    row -= 1
                else:
                    rowWhite1 = row + 4
                    break
            recordImg = img[rowWhite0:rowWhite1, :]
            lsRecordImg.append(recordImg)
            lsRecordWhiteLine.append(is_white_lines[rowWhite0:rowWhite1])
            lsRecordMask.append(white_mask[rowWhite0:rowWhite1, :])
            # plt.imshow(recordImg, cmap="gray")
            # plt.show()
        rowWhite0 = rowWhite2

# Analyze each record
with open("out.txt", "wb") as fout:
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'

    for recordImg, recordWl, recordMask in zip(lsRecordImg, lsRecordWhiteLine, lsRecordMask):
        lineImg = get_specific_color_mask(recordImg[:, 70:], [255, 255, 255], 100)
        # lineImg = recordImg[:,:]
        # # plt.imshow(lineImg)
        # # plt.show()
        # subimgPil = Image.fromarray(lineImg)
        # text = pytesseract.image_to_string(subimgPil, lang="eng", config=tessdata_dir_config)
        # # print(text)
        # fout.write(text.encode("utf8"))
        # fout.write("\n\n".encode("utf8"))

        # plt.imshow(recordImg, cmap="gray")
        # plt.imshow(recordMask, cmap="gray")
        # plt.show()
        # Get each lines
        startIdx, endIdx = 0, 0
        idxLine = 0
        isWl0 = 1
        for idx, isWl in enumerate(recordWl):
            if isWl0 == 1 and isWl == 0:
                startIdx = idx
            if isWl0 == 0 and isWl == 1:
                endIdx = idx
                lineImg = recordImg[(startIdx-3):(endIdx+4), 70:]
                # lineImg = get_specific_color_mask(lineImg, [255, 255, 255], 100)
                subimgPil = Image.fromarray(lineImg)
                text = pytesseract.image_to_string(subimgPil, lang="eng", config=tessdata_dir_config)
                print(text.encode("utf8"))
                fout.write(text.encode("utf8"))
                fout.write("\n".encode("utf8"))
                # print(text.encode("utf8").decode("utf8"))
                # plt.imshow(lineImg, cmap="gray")
                # plt.show()
                idxLine += 1
            isWl0 = isWl
        fout.write("\n".encode("utf8"))
