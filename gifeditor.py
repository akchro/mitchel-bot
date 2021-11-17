import requests
from PIL import Image, ImageDraw, ImageSequence, ImageFont
import io
import textwrap
import os
from wand.api import library
from ctypes import c_void_p, c_size_t
from wand.image import Image as wandimg


def create_gif(link, msg):
    original = requests.get(link + ".gif", stream=True)
    with open("temp.gif", "wb") as f:
        f.write(original.content)
        im = Image.open("temp.gif")
        width, height = im.size
        frames = []
        message = msg
        font_path = "./impact.ttf"
        for frame in ImageSequence.Iterator(im):
            font = ImageFont.truetype(font_path, int(width / 17))
            frame = frame.convert("RGB")

            if len(message) <= 37:
                bg = Image.new('RGB', (width, height + 60), 'white')
                bg.paste(frame, (bg.size[0] // 2 - frame.size[0] // 2, bg.size[1] - frame.size[1]))
                frame = bg
                d = ImageDraw.Draw(frame)
                w, h = d.textsize(message, font=font)
                d.multiline_text(((width - w)/2, 10), message, fill=(0, 0, 0), font=font)
            else:
                bg = Image.new('RGB', (width, height + 120), 'white')
                bg.paste(frame, (bg.size[0] // 2 - frame.size[0] // 2, bg.size[1] - frame.size[1]))
                frame = bg
                message = "\n".join(textwrap.wrap(message, 37))
                d = ImageDraw.Draw(frame)
                w, h = d.textsize(message, font=font)
                d.multiline_text(((width - w) / 2, 10), message, fill=(0, 0, 0), font=font)
            del d
            b = io.BytesIO()
            frame.save(b, format="GIF")
            frame = Image.open(b)
            frames.append(frame)
        frames[0].save("./temp.gif", save_all=True, append_images=frames[1:], optimize=True, quality=1)
    size = os.stat('temp.gif').st_size
    if size >= 20000000:
        return("Big")
    while size >= 8000000:
        compressimg = Image.open("temp.gif")
        cWidth, cHeight = compressimg.size
        library.MagickSetCompressionQuality.argtypes = [c_void_p, c_size_t]
        with wandimg(filename="temp.gif") as img:
            img.resize(width=int(cWidth*0.7), height=int(cHeight*0.7))
            library.MagickSetCompressionQuality(img.wand, 75)
            img.save(filename="temp.gif")
        size = os.stat('temp.gif').st_size
