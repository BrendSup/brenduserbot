# 彡𝚕𝚌𝚓𝚗🎴 , t.me/elcjn

#Modul Brend Userbot'a aiddir
#Oğurlama atanın balası
#İstifadə etmək istəyirsənsə icazə al


from telethon.tl import functions
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError)
from telethon.tl.functions.channels import GetFullChannelRequest

from userbot.events import register
from userbot.cmdhelp import CmdHelp


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("`Geçərsiz kanal/qrup`")
            return None
        except ChannelPrivateError:
            await event.reply("`Bu kanal/qrup gizlidir və ya banlanmısan`")
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`Kanal/qrup mövcüd deyil`")
            return None
        except (TypeError, ValueError):
            await event.reply("`Geçərsiz kanal/qrup`")
            return None
    return chat_info


@register(outgoing=True, pattern=r"^\.invite(?: |$)(.*)")
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        brend = await event.reply("`Başladılır...`")
    else:
        brend = await event.edit("`Başladılır...`")
    brendteam = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await brend.edit("`Təssüf ki bura üzv əlavə edilə bilmir`")
    s = 0
    f = 0
    error = 'None'

    await brend.edit("**Hazır ki vəziyyət**\n\n`İstifadəçilər dəvət edilir.......`")
    async for user in event.client.iter_participants(brendteam.full_chat.id):
        try:
            if error.startswith("Too"):
                return await brend.edit(f"**Dəvət uğursuzluqla nəticələndi**\n(`məhdudlaşma xətası ola bilər Xahiş edirəm daha sonra yenidən cəhd edin `)\n**XƏTA❌** : \n`{error}`\n\n• dəvət edildi `{s}`  \n• Uğursuz dəvətlər: `{f}`")
            await event.client(functions.channels.InviteToChannelRequest(channel=chat, users=[user.id]))
            s = s + 1
            await brend.edit(f"**Dəvət edilir...**\n\n• Əlavə olundu `{s}` \n• Uğursuz dəvətlər `{f}` \n\n**× LastError:** `{error}`")
        except Exception as e:
            error = str(e)
            f = f + 1
    return await brend.edit(f"**Dəvət Yekunlaşdı** \n\n• Uğurla nəticələnən dəvətlər `{s}` \n• Uğursuz Dəvətlər `{f}` ")

CmdHelp('invite').add_command(
    'invite', ' <istifadəçilərin götürüləcəyi qrupun linki>', 'Asanlıqla user vurmaq.'
).add()
