#Brend Userbot

#Plugini ekme oglum
#Bura niyə baxırsanki?

from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import uname
from shutil import which
from os import remove
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from telethon import version
from platform import python_version
from userbot.cmdhelp import CmdHelp
from userbot import CMD_HELP, ALIVE_NAME, BREND_VERSION, ALIVE_LOGO, bot, UPSTREAM_REPO_URL, HUSU, WHITELIST
from userbot.language import get_value
LANG = get_value("alives")



# ================== SABİT ===================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================

@register(outgoing=True, pattern="^.alives$")
async def amireallyalive(alive):
    img = ALIVE_LOGO
    caption = ("`"
              "╔═════════════════\n"
              f"║▻ {LANG['ALIVE1']}󠀁󠀁󠀁󠀁󠀁󠀁󠀁󠀁󠀁󠀁\n"
              f"║\n"
              f"║▻ {LANG['ALIVE2']}\n"
              f"║▻ 👤 {DEFAULTUSER}\n"
              f"║▻ {LANG['ALIVE3']}: {python_version()}\n"
              f"║▻ {LANG['ALIVE4']}: {BREND_VERSION}\n"
              f"║▻ {LANG['ALIVE5']}: {len(CMD_HELP)}\n"
              f"║▻ {LANG['ALIVE6']}\n"
               f"╚═════════════════\n"
              "`")
    await bot.send_file(alive.chat_id, img, caption=caption)
    await alive.delete()
                           
@register(incoming=True, from_users=WHITELIST, pattern="^.yoxla$")
async def brendhusu(husu):
    if husu.fwd_from:
        return
    if husu.is_reply:
        reply = await husu.get_reply_message()
        replytext = reply.text
        reply_user = await husu.client.get_entity(reply.from_id)
        ren = reply_user.id
        if husu.sender_id == 1081850094:
            sahibim = "⚡"
        else:
            sahibim = "⚡"
        if ren == HUSU:
            Version = str(BREND_VERSION.replace("v","")) 
            await husu.reply(f"**{sahibim} {ALIVE_NAME} {LANG['ALIVE7']}**...\n\n🌐**Brend Version:** {BREND_VERSION}")
        else:
            return
    else:
        return
                           
CmdHelp('alives').add_command(
    'alives', None, 'GIF-li alive mesaj;.'
).add_command
