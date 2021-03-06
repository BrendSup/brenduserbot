import datetime
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register
import os
import json
import random
import base64
import subprocess
import glob
from random import randint
from userbot.cmdhelp import CmdHelp
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import ContentTooShortError, DownloadError, ExtractorError, GeoRestrictedError, MaxDownloadsReached, PostProcessingError, UnavailableVideoError, XAttrMetadataError
from youtubesearchpython import SearchVideos
from userbot import ALIVE_NAME

from userbot.language import get_value
LANG = get_value("song")

@register(outgoing=True, pattern="^.deez(\d*|)(?: |$)(.*)")
async def deezl(event):
    if event.fwd_from:
        return
    sira = event.pattern_match.group(1)
    if sira == '':
        sira = 0
    else:
        sira = int(sira)

    sarki = event.pattern_match.group(2)
    if len(sarki) < 1:
        if event.is_reply:
            sarki = await event.get_reply_message().text
        else:
            await event.edit(LANG['GIVE_ME_SONG']) 

    await event.edit(LANG['SEARCHING'])
    chat = "@DeezerMusicBot"
    async with bot.conversation(chat) as conv:
        try:     
            mesaj = await conv.send_message(str(randint(31,62)))
            sarkilar = await conv.get_response()
            await mesaj.edit(sarki)
            sarkilar = await conv.get_response()
        except YouBlockedUserError:
            await event.reply(LANG['BLOCKED_DEEZER'])
            return
        await event.client.send_read_acknowledge(conv.chat_id)
        if sarkilar.audio:
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, LANG['UPLOADED_WITH'], file=sarkilar.message)
            await event.delete()
        elif sarkilar.buttons[0][0].text == "No results":
            await event.edit(LANG['NOT_FOUND'])
        else:
            await sarkilar.click(sira)
            sarki = await conv.wait_event(events.NewMessage(incoming=True,from_users=595898211))
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, f"`{sarkilar.buttons[sira][0].text}` | " + LANG['UPLOADED_WITH'], file=sarki.message)
            await event.delete()

a1 = base64.b64decode(
    "QUl6YVN5QXlEQnNZM1dSdEI1WVBDNmFCX3c4SkF5NlpkWE5jNkZV").decode("ascii")
a2 = base64.b64decode(
    "QUl6YVN5QkYwenhMbFlsUE1wOXh3TVFxVktDUVJxOERnZHJMWHNn").decode("ascii")
a3 = base64.b64decode(
    "QUl6YVN5RGRPS253blB3VklRX2xiSDVzWUU0Rm9YakFLSVFWMERR").decode("ascii")


@register(outgoing=True, pattern=r"^.song (.*)")
async def download_video(event):
    a = event.text
    if len(a) >= 5 and a[5] == "s":
        return
    await event.edit("????Musiqi axtar??l??r, xahi?? edir??m bir az g??zl??yin...")
    url = event.pattern_match.group(1)
    if not url:
        return await event.edit("**???Axtar???? X??tas??**\n\n?????????stifad?? qaydas??: -`.song Aslixan Bunlar`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await event.edit("?????????????????`Mahn??n?? tapa bilmir??m...`")
    type = "audio"
    await event.edit(f"`????Haz??rd??r Endirilir...`")
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
    try:
        await event.edit("????`Musiqi m??lumat??n?? ??ld?? edir??m...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await event.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await event.edit("????`Endirm?? m??zmunu ??ox q??sa idi.`")
        return
    except GeoRestrictedError:
        await event.edit("????`Oldu??unuz ??lk??nin ????b??k??sind?? bu mahn?? m??vcud deyil"
                         + " bir veb sayt m??hdudiyy??t qoyub?????????????????.`"
                         )
        return
    except MaxDownloadsReached:
        await event.edit("??????`Maksimum y??kl??m?? limitin?? ??at??d??n??z.`")
        return
    except PostProcessingError:
        await event.edit("????`Musiqini haz??rlayark??n x??ta ba?? verdi`????")
        return
    except UnavailableVideoError:
        await event.edit("?????????????????`??st??diyiniz mahn??n?? musiqi format??nda tapa bilm??dim????`")
        return
    except XAttrMetadataError as XAME:
        return await event.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await event.edit("???`Musiqini y??kl??y??rk??n x??ta ba?? verdi????`")
    except Exception as e:
        return await event.edit(f"{str(type(e)): {str(e)}}")
    dir = os.listdir()
    if f"{rip_data['id']}.mp3.jpg" in dir:
        thumb = f"{rip_data['id']}.mp3.jpg"
    elif f"{rip_data['id']}.mp3.webp" in dir:
        thumb = f"{rip_data['id']}.mp3.webp"
    else:
        thumb = None
    upteload = """
????Mahn??n?? Haz??rlay??ram????
??? ????Mahn??: {}
??? ????Kanal: {}
""".format(
        rip_data["title"], rip_data["uploader"]
    )
    await event.edit(f"`{upteload}`")
    CAPT = f"?????????????????????????????????????????????????????????\n??? ????`{rip_data['title']}`\n??? ????Kanal: `{rip_data['uploader']}`\n?????????????????????????????????????????????????????????\n??? ??????st??di: {ALIVE_NAME}\n?????????????????????????????????????????????????????????"
    await event.client.send_file(
        event.chat_id,
        f"{rip_data['id']}.mp3",
        thumb=thumb,
        supports_streaming=True,
        caption=CAPT,
        attributes=[
            DocumentAttributeAudio(
                duration=int(rip_data["duration"]),
                title=str(rip_data["title"]),
                performer=str(rip_data["uploader"]),
            )
        ],
    )
    await event.delete()
    os.remove(f"{rip_data['id']}.mp3")
    try:
        os.remove(thumb)
    except BaseException:
        pass
    

@register(outgoing=True, pattern="^.songpl ?(.*)")
async def songpl(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)

    if len(cmd) < 1:
        await event.edit(LANG['USAGE_PL'])    

    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    await event.edit(LANG['SEARCHING_PL'])
    dosya = os.getcwd() + "/playlist/" + "pl.pl"
    klasor = os.getcwd() + "/playlist/"
    sonuc = os.system(f"spotdl --playlist {cmd} --write-to=\"{dosya}\"")
    sonuc2 = os.system(f"spotdl --list {dosya} -f {klasor}")
    await event.edit(LANG['DOWNLOADED'])
    l = glob.glob(f"{klasor}/*.mp3")
    i = 0
    if len(l) >= 1:
        while i < len(l):
            await event.reply(LANG['SENDING_SONGS'] + l[i])
            await event.client.send_file(
                event.chat_id,
                l[i],
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
    else:
        await event.edit(LANG['NOT_FOUND_PL'])   
        return 
    os.system(f"rm -rf {klasor}/*.mp3")
    subprocess.check_output(f"rm -rf {klasor}/*.mp3",shell=True)
    os.system(f"rm -rf {klasor}/*.pl")
    subprocess.check_output(f"rm -rf {klasor}/*.pl",shell=True)

CmdHelp('song').add_command(
    'deez', '<mahn?? ad??/youtube/spotify/soundcloud>', 'Bir ne???? saytdan axtararaq, mahn?? atar.'
).add_command(
    'song', '<mahn?? ad??/youtube/spotify>', 'Mahn?? y??kl??y??r.'
).add_command(
    'songpl', '<spotify playlist>', 'Spotify Playlist\'ind??n mahn?? y??kl??y??r'
).add()
