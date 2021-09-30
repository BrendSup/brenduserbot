import os
import lyricsgenius
import asyncio

from userbot.events import register
from userbot import CMD_HELP
from userbot.cmdhelp import CmdHelp
from userbot.language import get_value
LANG = get_value("lyrics")

GENIUS = "MN180acpxZY2YjgsCuJLoI27C63CcqFQAaPsKnWEKiphEUdkQzU7VuaFbt6A2sbF"

@register(outgoing=True, pattern="^.lyrics(?: |$)(.*)")
async def lyrics(lyric):
    if r"-" in lyric.text:
        pass
    else:
        await lyric.edit(LANG['WRONG_TYPE'])
        return

    if GENIUS is None:
        await lyric.edit(
            LANG['GENIUS_NOT_FOUND'])
        return
    else:
        genius = lyricsgenius.Genius(GENIUS)
        try:
            args = lyric.text.split('.lyrics')[1].split('-')
            artist = args[0].strip(' ')
            song = args[1].strip(' ')
        except:
            await lyric.edit(LANG['GIVE_INFO'])
            return

    if len(args) < 1:
        await lyric.edit(LANG['GIVE_INFO'])
        return

    await lyric.edit(LANG['SEARCHING'].format(artist, song))

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if songs is None:
        await lyric.edit(LANG['NOT_FOUND'].format(artist, song))
        return
    if len(songs.lyrics) > 4096:
        await lyric.edit(LANG['TOO_LONG'])
        with open("lyrics.txt", "w+") as f:
            f.write(f"{LANG['LYRICS']} \n{artist} - {song}\n\n{songs.lyrics}")
        await lyric.client.send_file(
            lyric.chat_id,
            "lyrics.txt",
            reply_to=lyric.id,
        )
        os.remove("lyrics.txt")
    else:
        await lyric.edit(f"{LANG['LYRICS']} \n`{artist} - {song}`\n\n```{songs.lyrics}```")
    return

@register(outgoing=True, pattern="^.singer(?: |$)(.*)")
async def singer(lyric):
    if r"-" in lyric.text:
        pass
    else:
        await lyric.edit(LANG['WRONG_TYPE'])
        return

    if GENIUS is None:
        await lyric.edit(
            LANG['GENIUS_NOT_FOUND'])
        return
    else:
        genius = lyricsgenius.Genius(GENIUS)
        try:
            args = lyric.text.split('.singer')[1].split('-')
            artist = args[0].strip(' ')
            song = args[1].strip(' ')
        except:
            await lyric.edit(LANG['GIVE_INFO'])
            return

    if len(args) < 1:
        await lyric.edit(LANG['GIVE_INFO'])
        return

    await lyric.edit(LANG['SEARCHING'].format(artist, song))

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if songs is None:
        await lyric.edit(LANG['NOT_FOUND'].format(artist, song))
        return
    await lyric.edit(LANG['SINGER_LYRICS'].format(artist, song))
    await asyncio.sleep(1)

    split = songs.lyrics.splitlines()
    i = 0
    while i < len(split):
        try:
            if split[i] != None:
                await lyric.edit(split[i])
                await asyncio.sleep(2)
            i += 1
        except:
            i += 1
    await lyric.edit(LANG['SINGER_ENDED'])

    return

            

CMD_HELP.update({
    "lyrics":
    "İstifadəsi: .`lyrics <Musiqiçi adı> - <musiqi adı>`\n"
    "Qeyd: ""-"" önəmlidi!",
    "singer":
    "Mahnı, istifadə: .`singer <Musiqiçi adı> - <musiqi adı>`\n"
    "Qeyd: ""-"" önəmlidi!"

})

CmdHelp('lyrics').add_command(
    'lyrics', ' <Musiqiçi adı> - <musiqi adı>', 'Sözləri gətirir.', 'lyrics Sistem M6qqan - cənnət'
).add_command(
    'singer', ' <Musiqiçi adı> - <musiqi adı>', 'Sözləri gətirir.', 'lyrics Sistem M6qqan - cənnət'
).add()
