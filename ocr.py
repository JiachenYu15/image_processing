from PIL import Image
import sys
import pillowfight
import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = 'eng'
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'
# Note that languages are NOT sorted in any way. Please refer
# to the system locale settings for the default language
# to use.
img_in = PIL.Image.open(sys.argv[1])
img_out = pillowfight.swt(img_in, output_type=pillowfight.SWT_OUTPUT_BW_TEXT)
txt = tool.image_to_string(
    Image.open(sys.argv[1]),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)
print(">>>>>>>>>>>>>>")
print(txt)
print("<<<<<<<<<<<<<<")
