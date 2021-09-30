# ᴇʟçɪɴ ⥌ 🇯🇵

from telethon.tl.types import InputMediaDice
from userbot.events import register
from userbot.cmdhelp import CmdHelp


@register(outgoing=True, pattern="^.zer(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice(''))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice(''))
        except BaseException:
            pass


@register(outgoing=True, pattern="^.ox(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice('🎯'))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice('🎯'))
        except BaseException:
            pass


@register(outgoing=True, pattern="^.basket(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice('🏀'))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice('🏀'))
        except BaseException:
            pass


CmdHelp('sgames').add_command(
    'zer', '', 'Random zər atar və beləliklə qarşılıqlı şəkildə bir nəfərlə zər oynaya bilərsiz.'
).add_command(
    'ox', '', ' Ox ata bilərsiz' , 'dostlarınızla kimin hədəfi daha dəqiq vuracağımı müyyən edin.'
).add_command(
    'basket', '', 'Basket ataraq , kimin daha dəqiq olacağımı müyyən edin.'
).add()