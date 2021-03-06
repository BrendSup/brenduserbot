from userbot.events import register
from userbot import CMD_HELP, bot, LOGS, CLEAN_WELCOME, BOTLOG_CHATID
from telethon.events import ChatAction
from userbot.cmdhelp import CmdHelp

@bot.on(ChatAction)
async def goodbye_to_chat(event):
    try:
        from userbot.modules.sql_helper.goodbye_sql import get_current_goodbye_settings
        from userbot.modules.sql_helper.goodbye_sql import update_previous_goodbye
    except:
        return
    cws = get_current_goodbye_settings(event.chat_id)
    if cws:
        """user_added=False,
        user_joined=False,
        user_left=True,
        user_kicked=True"""
        if (event.user_left
                or event.user_kicked) and not (await event.get_user()).bot:
            if CLEAN_WELCOME:
                try:
                    await event.client.delete_messages(event.chat_id,
                                                       cws.previous_goodbye)
                except Exception as e:
                    LOGS.warn(str(e))
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await event.client.get_me()

            title = chat.title if chat.title else "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "[{}](tg://user?id={})".format(a_user.first_name,
                                                     a_user.id)
            my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
            first = a_user.first_name
            last = a_user.last_name
            if last:
                fullname = f"{first} {last}"
            else:
                fullname = first
            username = f"@{a_user.username}" if a_user.username else mention
            userid = a_user.id
            my_first = me.first_name
            my_last = me.last_name
            if my_last:
                my_fullname = f"{my_first} {my_last}"
            else:
                my_fullname = my_first
            my_username = f"@{me.username}" if me.username else my_mention
            file_media = None
            current_saved_goodbye_message = None
            if cws and cws.f_mesg_id:
                msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                        ids=int(cws.f_mesg_id))
                file_media = msg_o.media
                current_saved_goodbye_message = msg_o.message
            elif cws and cws.reply:
                current_saved_goodbye_message = cws.reply
            current_message = await event.reply(
                current_saved_goodbye_message.format(mention=mention,
                                                     title=title,
                                                     count=count,
                                                     first=first,
                                                     last=last,
                                                     fullname=fullname,
                                                     username=username,
                                                     userid=userid,
                                                     my_first=my_first,
                                                     my_last=my_last,
                                                     my_fullname=my_fullname,
                                                     my_username=my_username,
                                                     my_mention=my_mention),
                file=file_media)
            update_previous_goodbye(event.chat_id, current_message.id)


@register(outgoing=True, pattern=r"^.setgoodbye(?: |$)(.*)")
async def save_goodbye(event):
    try:
        from userbot.modules.sql_helper.goodbye_sql import add_goodbye_setting
    except:
        await event.edit("`SQL olmayan rejimd?? i??l??yir!`")
        return
    msg = await event.get_reply_message()
    string = event.pattern_match.group(1)
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#SA??OLLA??MA_QEYD??\
            \nQRUP ID: {event.chat_id}\
            \nA??a????dak?? mesaj s??hb??t ??????n yeni bir sa??olla??ma qeydi kimi qeyd edildi, xai?? edirik silm??yin!!"
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(
                "`Qar????lama qeydini qeyd etm??k ??????n BOTLOG_CHATID ayarlanmal??d??r.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Sa??olla??ma mesaj?? bu s??hb??t ??????n {} `"
    if add_goodbye_setting(event.chat_id, 0, string, msg_id) is True:
        await event.edit(success.format('qeyd olundu'))
    else:
        await event.edit(success.format('yenil??ndi'))


@register(outgoing=True, pattern="^.checkgoodbye$")
async def show_goodbye(event):
    try:
        from userbot.modules.sql_helper.goodbye_sql import get_current_goodbye_settings
    except:
        await event.edit("`SQL rejimd??n k??narda i??l??yir!`")
        return
    cws = get_current_goodbye_settings(event.chat_id)
    if not cws:
        await event.edit("`Burada he?? bir sa??olla??ma mesaj?? qeyd olunmay??b.`")
        return
    elif cws and cws.f_mesg_id:
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                ids=int(cws.f_mesg_id))
        await event.edit(
            "`Haz??rda bu qeydl?? ????xanlar?? /ban olunanlara cavab verir??m..`")
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws and cws.reply:
        await event.edit(
            "`Haz??rda bu qeydl?? ????xan /ban olunanlara cavab verir??m..`")
        await event.reply(cws.reply)


@register(outgoing=True, pattern="^.rmgoodbye$")
async def del_goodbye(event):
    try:
        from userbot.modules.sql_helper.goodbye_sql import rm_goodbye_setting
    except:
        await event.edit("`SQL d?????? modda i??l??yir!`")
        return
    if rm_goodbye_setting(event.chat_id) is True:
        await event.edit("`Yola salma mesaj?? bu s??hb??t ??????n silindi.`")
    else:
        await event.edit("`Burada yola salma qeydi varm??? ?`")

CmdHelp('goodbye').add_command(
    'setgoodbye', '<cavab mesaj??> v?? ya .setgoodbye il?? mesaj?? cavabland??r??n', 'Mesaj?? s??hb??t?? qeyd etdiyiniz qeyd olaraq saxlay??r.'
).add_command(
    'checkgoodbye', None, 'S??hb??t qeydinin olub olmad??????n?? yoxlay??n.'
).add_command(
    'rmgoodbye', None, 'Cari s??hb??t ??????n qeyd etdiyinizi silir.'
).add()
