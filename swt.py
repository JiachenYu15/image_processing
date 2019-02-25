import sys
import PIL
import pillowfight
import pytesseract

img_in = PIL.Image.open(sys.argv[1])
if_natural = sys.argv[2]
if int(if_natural):
    img_out = pillowfight.swt(img_in, output_type=pillowfight.SWT_OUTPUT_GRAYSCALE_TEXT)
    img_out.save("results/beforeT","PNG")
else:
    img_out = img_in

config = '-c tessedit_write_images=1'
img_str = pytesseract.image_to_string(img_out, lang='eng', config=config)

print(">>>>>>>>>>>>>>>>>>>>>>>>")
print(img_str)
print("<<<<<<<<<<<<<<<<<<<<<<<<")
