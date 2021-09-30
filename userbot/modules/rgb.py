#Tercumeden istifade eleme serefsiz
#Tercumeden istifade edenin atasiyam
#Tercumeden istifade eleme ay anasi qehbe
#Tercumeni istifade eden peyserdi (qizdirsa qehbedi)
#Ekenin anasinin amciğini sapalagliyim
# @Mr_HD_20

import io
import os
import random
import textwrap

from PIL import Image, ImageChops, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterDocument
from userbot.events import register 
from userbot import CMD_HELP, bot
from userbot.cmdhelp import CmdHelp

from userbot.language import get_value
LANG = get_value("rgb")

@register(outgoing=True, pattern="^.rgb(?: |$)(.*)")
async def sticklet(event):
    R = random.randint(0,256)
    G = random.randint(0,256)
    B = random.randint(0,256)

    sticktext = event.pattern_match.group(1).strip()

    if len(sticktext) < 1:
        await event.edit(LANG['NEED_TEXT'])
        return

    await event.edit(LANG['CONVERTING'])

    sticktext = textwrap.wrap(sticktext, width=10)

    sticktext = '\n'.join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = await get_font_file(event.client, "@FontArsiv")

    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 10
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512-width)/2,(512-height)/2), sticktext, font=font, fill=(R, G, B))

    image_stream = io.BytesIO()
    image_stream.name = "@resim.webp"

    def trim(im):
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        return im.crop(bbox) if bbox else im

    image = trim(image)
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    await event.delete()

    await event.client.send_file(event.chat_id, image_stream, reply_to=event.message.reply_to_msg_id)

    try:
        os.remove(FONT_FILE)
    except:
        pass


async def get_font_file(client, channel_id):

    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,

        limit=None
    )

    font_file_message = random.choice(font_file_message_s)

    return await client.download_media(font_file_message)

CmdHelp('rgb').add_command(
    'rbg', '<cavab>', 'Mətninizi RGB stikerinə çevirin.'
).add()
