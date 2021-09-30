# ᴇʟçɪɴ ⥌ 🇯🇵

from telethon.tl import functions, types
from userbot.events import register
from userbot.cmdhelp import CmdHelp


@register(outgoing=True, pattern="^.yarat (q|k)(?: |$)(.*)")
async def telegraphs(grop):
    if grop.text[0].isalpha() or grop.text[0] in ("/", "#", "@", "!"):
        return
    if grop.fwd_from:
        return
    type_of_group = grop.pattern_match.group(1)
    group_name = grop.pattern_match.group(2)
    if type_of_group == "b":
        try:
            result = await grop.client(
                functions.messages.CreateChatRequest(  
                    users=["@EmiliaHikariBot"],
                    
                    title=group_name,
                )
            )
            created_chat_id = result.chats[0].id
            await grop.client(
                functions.messages.DeleteChatUserRequest(
                    chat_id=created_chat_id, user_id="@EmiliaHikariBot"
                )
            )
            result = await grop.client(
                functions.messages.ExportChatInviteRequest(peer=created_chat_id,)
            )
            await grop.edit(
                "[ʙʀᴇɴᴅ ᴜꜱᴇʀʙᴏᴛ⚡️](t.me/BrendUserBot) tərəfindən `{}` ` uğurla yaradıldı`. `Toxunaraq` [{}]({}) `  qoşulun`".format(
                    group_name, group_name, result.link
                )
            )
        except Exception as e:  
            await grop.edit(str(e))
    elif type_of_group in ["q","k"]:
        try:
            r = await grop.client(
                functions.channels.CreateChannelRequest(
                    title=group_name,
                    about="`Bu kanala xoş gəldin`",
                    megagroup=False if type_of_group == "k" else True,
                )
            )
            created_chat_id = r.chats[0].id
            result = await grop.client(
                functions.messages.ExportChatInviteRequest(peer=created_chat_id,)
            )
            await grop.edit(
                "[ʙʀᴇɴᴅ ᴜꜱᴇʀʙᴏᴛ⚡️](t.me/BrendUserBot) tərəfindən `{}` ` uğurla yaradıldı`. `toxunaraq` [{}]({}) ` qoşul` ".format(
                    group_name, group_name, result.link
                )
            )
        except Exception as e:  
            await grop.edit(str(e))

CmdHelp('yarat').add_command(
    'yarat', '<q/k>,<ad>', 'Cəmi bir əmrlə qrup və ya kanal yaradın qrup yaratmaq üçün .yarat q <ad> , kanal yaratmaq üçün .yarat k <ad> yazın.'
).add()