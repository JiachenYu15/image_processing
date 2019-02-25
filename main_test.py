import sys
import cv2
import PIL
import pillowfight
import pytesseract
import numpy as np
    

def main(argv):

    img = cv2.imread(sys.argv[1])
    cv2.imwrite("results/ori.png",img)
    #Binarization
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Line Detection
    #th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    threshed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,11,10)

    cv2.imwrite("results/bin.png",threshed)
    threshed = cv2.fastNlMeansDenoising(threshed,None,27,30)
    cv2.imwrite("results/nr.png",threshed)
    hist = cv2.reduce(threshed, 1, cv2.REDUCE_AVG).reshape(-1)

    th = 2
    H, W = img.shape[:2]
    uppers = [y for y in range(H-1) if hist[y]<=th and hist[y+1]>th]
    lowers = [y for y in range(H-1) if hist[y]>th and hist[y+1]<=th]

    #Rotation
    rotated = cv2.cvtColor(threshed, cv2.COLOR_GRAY2BGR)
    '''
    for y in uppers:
        cv2.line(rotated, (0, y), (W, y), (255,0,0), 1)

    for y in lowers:
        cv2.line(rotated, (0, y), (W, y), (0,255,0), 1)
    '''
    cv2.imwrite("results/result.png", rotated)

    subfiles = []
    #crop the image
    for upper,lower in zip(uppers,lowers):
        crop_image = rotated[upper:lower, 0:W]
        crop_name = "results/" + str(upper) + "_" + str(lower)+ ".png"
        subfiles.append(crop_name)
        cv2.imwrite(crop_name, crop_image)
'''

    for subfile in subfiles:

        img_in = PIL.Image.open(subfile)
        if_natural = sys.argv[2]
        if int(if_natural):
            img_out = pillowfight.swt(img_in, output_type=pillowfight.SWT_OUTPUT_GRAYSCALE_TEXT)
            #img_out.save("results/beforeT","PNG")
        else:
            img_out = img_in

        config = '-c tessedit_write_images=1'
        img_str = pytesseract.image_to_string(img_out, lang='eng', config=config)

        print(">>>>>>>>>>>>>>>>>>>>>>>>")
        print(img_str)
        print("<<<<<<<<<<<<<<<<<<<<<<<<")

    #cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    #cv2.imshow('image', threshed)
    #cv2.waitKey(0)
'''
if __name__ == "__main__":
    main(sys.argv[1:])
 
