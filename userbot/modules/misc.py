from random import randint
from asyncio import sleep
from os import execl
import sys
import io
import sys
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp

from userbot.language import get_value
LANG = get_value("misc")

@register(outgoing=True, pattern="^.resend")
async def resend(event):
    await event.delete()
    m = await event.get_reply_message()
    if not m:
        event.edit(LANG['REPLY_TO_FILE'])
        return
    await event.respond(m)

@register(outgoing=True, pattern="^.random")
async def randomise(items):
    
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            LANG['NEED_MUCH_DATA_FOR_RANDOM']
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit(f"**{LANG['QUERY']}: **\n`" + items.text[8:] + f"`\n**{LANG['RESULT']}: **\n`" +
                     itemo[index] + "`")


@register(outgoing=True, pattern="^.yuxu( [0-9]+)?$")
async def sleepybot(time):

    if " " not in time.pattern_match.group(1):
        await time.reply(LANG['SLEEP_DESC'])
    else:
        counter = int(time.pattern_match.group(1))
        await time.edit(LANG['SLEEPING'])
        await sleep(2)
        if BOTLOG:
            await time.client.send_message(
                BOTLOG_CHATID,
                "Botu" + str(counter) + "saniyə yatızdırın.",
            )
        await sleep(counter)
        await time.edit(LANG['GOODMORNIN_YALL'])


@register(outgoing=True, pattern="^.sondur$")
async def shutdown(event):

    await event.client.send_file(event.chat_id, 'https://www.winhistory.de/more/winstart/mp3/winxpshutdown.mp3', caption=LANG['GOODBYE_MFRS'], voice_note=True)
    await event.delete()

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SONDUR \n"
                                        "Bot Söndü.")
    try:
        await bot.disconnect()
    except:
        pass


@register(outgoing=True, pattern="^.restart$")
async def restart(event):
    await event.edit(LANG['RESTARTING'])
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                        "Bot yenidən başladıldı.")

    try:
        await bot.disconnect()
    except:
        pass

    execl(sys.executable, sys.executable, *sys.argv)


@register(outgoing=True, pattern="^.support$")
async def bot_support(wannahelp):
    
    await wannahelp.edit(LANG['SUPPORT_GROUP'])


@register(outgoing=True, pattern="^.creator$")
async def creator(e):
    await e.edit(LANG['CREATOR'])


@register(outgoing=True, pattern="^.sahib$")
async def reedme(e):
    await e.edit(LANG['CREATOR'])

@register(outgoing=True, pattern="^.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(' ', 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    
    await wannasee.edit(LANG['REPO'])

@register(outgoing=True, pattern="^.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit(
            "`Həll edilən mesaj üçün userbot loglarını yoxla!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Həll olunan mesaj`")

CmdHelp('misc').add_command(
    'random', '<seçim1> <seçim2> ... <seçimN>', 'Seçim siyahısından random bir seçim edər', 'random brend uniborg userge'
).add_command(
    'yuxu', '<zaman>', 'Brend də bir insandır və o da yorulur. Hərdən biraz yatsın.', 'sleep 30'
).add_command(
    'sondur', None, 'Nostaljik bir şekildə botunuzu söndürün.'
).add_command(
    'repo', None, 'Brend botunun GitHub\'daki reposuna giden bir bağlantı.'
).add_command(
    'sahib', None, 'Bu gözəl botun sahibinin kim olduğunu deyir.'
).add_command(
    'creator', None, 'Bu gözəl botu kimin yaratdığını öyrənin :-)'
).add_command(
    'repeat', '<say> <metn>', 'Bir mətni müəyyən sayda təkrarlayır. Spam əmri ile qarışdırma!'
).add_command(
    'restart', None, 'Botu yenidən başladır.'
).add_command(
    'resend', None, 'Bir medyanı yenidən göndərir.'
).add_command(
    'raw', '<cavab>', 'Cavablandırılan mesaj haqqında məlumat verir.'
).add()
