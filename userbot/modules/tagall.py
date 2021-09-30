# Eken bize ata desin



import random
import asyncio
from userbot.events import register
from userbot import CMD_HELP, bot
from userbot import BREND_VERSION
from telethon.tl.types import ChannelParticipantsAdmins as cp
from time import sleep
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.tag(?: |$)(.*)")
async def _(tag):

	if tag.pattern_match.group(1):
		seasons = tag.pattern_match.group(1)
	else:
		seasons = ""

	chat = await tag.get_input_chat()
	a_=0
	await tag.delete()
	async for i in bot.iter_participants(chat):
		if a_ == 500:
			break
		a_+=5
		await tag.client.send_message(tag.chat_id, "[{}](tg://user?id={}) {}".format(i.first_name, i.id, seasons))
		sleep(0.5)
		
		
@register(outgoing=True, pattern="^.admins(?: |$)(.*)")
async def _(tagadmin):
	
	if tagadmin.pattern_match.group(1):
		seasons = tagadmin.pattern_match.group(1)
	else:
		seasons = ""

	chat = await tagadmin.get_input_chat()
	a_=0
	await tagadmin.delete()
	async for i in bot.iter_participants(chat, filter=cp):
		if a_ == 500:
			break
		a_+=5
		await tagadmin.client.send_message(tagadmin.chat_id, "[{}](tg://user?id={}) {}".format(i.first_name, i.id, seasons))
		sleep(0.5)


@register(outgoing=True, pattern="^.all$")
async def _(event):
    if event.fwd_from:
        return
    mentions = "@all"
    chat = await event.get_input_chat()
    leng = 0
    async for x in bot.iter_participants(chat):
        if leng < 4092:
            mentions += f"[\u2063](tg://user?id={x.id})"
            leng += 1
    await event.reply(mentions)
    await event.delete()

emoji = "❤️ 🧡 💛 💚 💙 💜 🤍 🖤 🤎 💔" \
        "😍 😁 😂 🤓 😎 🧐 🤩 😴".split(" ")


class FlagContainer:
    is_active = False


#eken peyserdi
#eken bize bir basa ata desin
@register(outgoing=True, pattern="^.etag.*")
async def b(event):
    if event.fwd_from or FlagContainer.is_active:
        return
    try:
        FlagContainer.is_active = True

        text = None
        args = event.message.text.split(" ", 1)
        if len(args) > 1:
            text = args[1]

        chat = await event.get_input_chat()
        await event.delete()

        tags = list(map(lambda m: f"[{random.choice(emoji)}](tg://user?id={m.id})", await event.client.get_participants(chat)))
        current_pack = []
        async for participant in event.client.iter_participants(chat):
            if not FlagContainer.is_active:
                break

            current_pack.append(participant)

            if len(current_pack) == 5:
                tags = list(map(lambda m: f"[{random.choice(emoji)}](tg://user?id={m.id})", current_pack))
                current_pack = []

                if text:
                    tags.append(text)

                await event.client.send_message(event.chat_id, " ".join(tags))
                await asyncio.sleep(0.5)
    finally:
        FlagContainer.is_active = False

@register(outgoing=True, pattern="^.stoptag")
async def m_fb(event):
    if event.fwd_from or not FlagContainer.is_active:
        return

    await event.delete()
    FlagContainer.is_active = False

# ekme serefsiz


CmdHelp('tagall').add_command(
    'tag', '<səbəb>', 'Qrupdakı userləri tək-tək tağ edər'
).add_command(
    'admins', '', 'Qrupdakı adminləri tək-tək tag edər'
).add_command(
    'etag', '', 'Qrupdakı userləri emojilərlə tag edər.'
).add_command(
    'all', '', 'Qrupdakı userləri tək bir mesajda tag edər.'
).add_command(
    'stoptag', '', 'etag prosesini saxlayar.'
).add()
