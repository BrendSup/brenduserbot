from userbot.events import register
from userbot import CMD_HELP, bot
from userbot.cmdhelp import CmdHelp
from userbot import BREND_VERSION

@register(outgoing=True, pattern="^.qy (.*)")
async def b(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("Xahiş edirəm bir mətn verin")
    tt = event.text
    msg = tt[4:]
    kk = await event.edit("Mesajınız bütün qruplarınıza göndərilir 📢")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"**Yayım yekunlaşdı📢**\nUğurlu {done} qrup✅ \n  Uğursuz {er} qrup❌")


@register(outgoing=True, pattern=r"^\.sy(?: |$)(.*)")
async def gucast(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("Xahiş edirəm bir mətn verin")
    tt = event.text
    msg = tt[4:]
    kk = await event.edit("Mesajınız bütün əlaqələrinizə göndərilir 📢")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"**Yayım yekunlaşdı📢**\nUğurlu {done} söhbət✅ \n  Uğursuz {er} söhbət❌")



CmdHelp('yayım').add_command(
    'qy <mətn>', '', 'Verdiyiniz mətn olduğunuz bütün qruplara atılar'
).add_command(
    'sy <mətn>', '', 'Verdiyiniz mətn bütün əlaqələrinizin şəxsisinə atılar'
).add()