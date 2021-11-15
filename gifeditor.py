import requests
from PIL import Image, ImageDraw, ImageSequence, ImageFont
import io
import textwrap


def create_gif(link, msg):
    original = requests.get(link, stream=True)
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
                bg.paste(frame, (bg.size[0] // 2 - frame.size[0] // 2, bg.size[1] // 2 - frame.size[1] // 2))
                frame = bg
                d = ImageDraw.Draw(frame)
                d.rectangle((0, 0, width, 60), fill=(255, 255, 255))
                d.multiline_text((int(20), 20), message, fill=(0, 0, 0), font=font)
            else:
                bg = Image.new('RGB', (width, height + 120), 'white')
                bg.paste(frame, (bg.size[0] // 2 - frame.size[0] // 2, bg.size[1] // 2 - frame.size[1] // 2))
                frame = bg
                message = "\n".join(textwrap.wrap(message, 37))
                d = ImageDraw.Draw(frame)
                d.rectangle((0, 0, width, 120), fill=(255, 255, 255))
                d.multiline_text((int(20), 20), message, fill=(0, 0, 0), font=font)
            del d
            b = io.BytesIO()
            frame.save(b, format="GIF")
            frame = Image.open(b)
            frames.append(frame)
        frames[0].save("./temp.gif", save_all=True, append_images=frames[1:], optimize=True, quality=1)
