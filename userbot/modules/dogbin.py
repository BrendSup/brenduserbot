from requests import get, post, exceptions
import os
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.cmdhelp import CmdHelp

DOGBIN_URL = "https://del.dog/"

from userbot.language import get_value
LANG = get_value("dogbin")

@register(outgoing=True, pattern=r"^.yap[iı][sş]d[iı]r(?: |$)([\s\S]*)")
async def paste(pstl):

    dogbin_final_url = ""
    match = pstl.pattern_match.group(1).strip()
    reply_id = pstl.reply_to_msg_id

    if not match and not reply_id:
        await pstl.edit(LANG['ELON_SAYS'])
        return

    if match:
        message = match
    elif reply_id:
        message = (await pstl.get_reply_message())
        if message.media:
            downloaded_file_name = await pstl.client.download_media(
                message,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r"
            os.remove(downloaded_file_name)
        else:
            message = message.message

    await pstl.edit(LANG['PASTING'])
    resp = post(DOGBIN_URL + "documents", data=message.encode('utf-8'))

    if resp.status_code == 200:
        response = resp.json()
        key = response['key']
        dogbin_final_url = DOGBIN_URL + key

        if response['isUrl']:
            reply_text = (f"{LANG['PASTED']}\n\n"
                          f"`{LANG['URL']}` {dogbin_final_url}\n\n"
                          f"`{LANG['ORG_URL']}`\n"
                          f"`{LANG['DOGBIN_URL']}`: {DOGBIN_URL}v/{key}\n")
        else:
            reply_text = (f"`{LANG['URL_BUT_ENG']}`\n\n"
                          f"`{LANG['DOGBIN_URL']}`: {dogbin_final_url}")
    else:
        reply_text = (f"`{LANG['DOGBIN_NOT_RESPOND']}`")

    await pstl.edit(reply_text)
    if BOTLOG:
        await pstl.client.send_message(
            BOTLOG_CHATID,
            f"Dogbinə mətn yapışdırma uğurla edildi",
        )


@register(outgoing=True, pattern="^.k[oö][cç][uü]r(?: |$)(.*)")
async def get_dogbin_content(dog_url):

    textx = await dog_url.get_reply_message()
    message = dog_url.pattern_match.group(1)
    await dog_url.edit(LANG['DATA_CHECKING'])

    if textx:
        message = str(textx.message)

    format_normal = f'{DOGBIN_URL}'
    format_view = f'{DOGBIN_URL}v/'

    if message.startswith(format_view):
        message = message[len(format_view):]
    elif message.startswith(format_normal):
        message = message[len(format_normal):]
    elif message.startswith("del.dog/"):
        message = message[len("del.dog/"):]
    else:
        await dog_url.edit(LANG['UNSUPPORTED_URL'])
        return

    resp = get(f'{DOGBIN_URL}raw/{message}')

    try:
        resp.raise_for_status()
    except exceptions.HTTPError as HTTPErr:
        await dog_url.edit(
            LANG['HTTP_ERROR'] + "\n\n" + str(HTTPErr))
        return
    except exceptions.Timeout as TimeoutErr:
        await dog_url.edit(LANG['TIMEOUT'] + str(TimeoutErr))
        return
    except exceptions.TooManyRedirects as RedirectsErr:
        await dog_url.edit(
            LANG['TOO_MANY_REDIRECTS'] +
            str(RedirectsErr))
        return

    reply_text = LANG['DOGBIN_DATA'] + resp.text

    await dog_url.edit(reply_text)
    if BOTLOG:
        await dog_url.client.send_message(
            BOTLOG_CHATID,
            LANG['DOGBIN_ENDED'],
        )

CmdHelp('dogbin').add_command(
    'yapisdir və ya yapışdır', '<mətn/cavablama>', 'Dogbin istifadə edərək yapışdırılmış və ya qısaldılmış url yaratmaq (https://del.dog/)'
).add_command(
    'kocur ve ya köçür', None, 'Dogbin url məzmununu mətnə köçürər (https://del.dog/)'
).add()
