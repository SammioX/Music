import asyncio, os, urllib.request

from os import path
from PIL import Image, ImageDraw, ImageFont

from ..config import THUMB_URL
from .errors import FFmpegReturnCodeError


async def convert(file_path: str) -> str:
    out = path.basename(file_path)
    out = out.split(".")
    out[-1] = "raw"
    out = ".".join(out)
    out = path.basename(out)
    out = path.join("raw_files", out)

    if path.isfile(out):
        return out

    proc = await asyncio.create_subprocess_shell(
        f"ffmpeg -y -i {file_path} -f s16le -ac 2 -ar 48000 -acodec pcm_s16le {out}",
        asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    await proc.communicate()

    if proc.returncode != 0:
        raise FFmpegReturnCodeError("FFmpeg did not return 0")

    return out


async def thumbnail_convert(title, views, duration):
    urllib.request.urlretrieve(THUMB_URL, "thmb.png")
    image1 = Image.open("./thmb.png")
    image2 = image1.convert("RGBA")
    image3 = Image.open("./hellbot/helper/resources/border.png")
    Image.alpha_composite(image2, image3).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./hellbot/helper/resources/Aleo-Bold.otf", 32)
    draw.text((205, 550), f"Title: {title}", (51, 215, 255), font=font)
    draw.text((205, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((205, 630), f"Views: {views}", (255, 255, 255), font=font)
    img.save("final.png")
    os.remove("temp.png")
    os.remove("thmb.png")
