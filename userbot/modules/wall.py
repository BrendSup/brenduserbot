#Plugini əkən bizə ata desin
#T.me/Guliyev909
#T.me/BrendUserBot
import asyncio
import os
from asyncio.exceptions import TimeoutError

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register
from userbot import BREND_VERSION
from userbot.cmdhelp import CmdHelp
#Noldu pasinyan

@register(outgoing=True, pattern=r"^\.wall(?: |$)(.*)")
async def _(event):
    try:
        query = event.pattern_match.group(1)
        await event.edit("`Şəkil seçilir....`")
        async with bot.conversation("@userbotindobot") as conv:
            try:
                query1 = await conv.send_message(f"/wall {query}")
                asyncio.sleep(6)
                r1 = await conv.get_response()
                r2 = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await event.reply("@userbotindobot start et")
            else:
                img = await event.client.download_media(r1)
                img2 = await event.client.download_media(r2)
                await event.edit("`Göndədirəm....`")
                p = await event.client.send_file(
                    event.chat_id,
                    img,
                    force_document=False,
                    caption="@BrendUserbot istədiyiniz şəkli seçdi",
                    reply_to=event.reply_to_msg_id,
                )
                await event.client.send_file(
                    event.chat_id,
                    img2,
                    force_document=True,
                    caption=f"{query}",
                    reply_to=p,
                )
                await event.client.delete_messages(
                    conv.chat_id, [r1.id, r2.id, query1.id]
                )
        await event.delete()
        os.system("rm *.png *.jpg")
    except TimeoutError:
        return await event.edit("`@userbotindobot cavab vermədi..`")


Help = CmdHelp('wall')
Help.add_command('wall', None, '.wall <söz> yazaraq şəkil yükləyin. Bu bir kino və s. ola bilər')
Help.add_info('@Guliyev909` tərəfindən düzəldilmişdir`')
Help.add()
