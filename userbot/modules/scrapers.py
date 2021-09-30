import os, re
import time
import asyncio
import emoji
import shutil
from bs4 import BeautifulSoup
from time import sleep
from html import unescape
from re import findall
from selenium import webdriver
from urllib.parse import quote_plus
from urllib.error import HTTPError
from google_trans_new import google_translator
from googletrans import LANGUAGES, Translator
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError
from urbandict import define
from requests import get
from search_engine_parser import GoogleSearch
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from gtts import gTTS
from gtts.lang import tts_langs
from emoji import get_emoji_regexp
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)
from userbot import CMD_HELP, BOTLOG, bot, BOTLOG_CHATID, YOUTUBE_API_KEY, CHROME_DRIVER, GOOGLE_CHROME_BIN
from userbot.events import register
from telethon.tl.types import DocumentAttributeAudio
from userbot.modules.upload_download import progress, humanbytes, time_formatter
from ImageDown import ImageDown
from userbot.utils import googleimagesdownload 
import base64, binascii
import random
from userbot.cmdhelp import CmdHelp
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon import events

##
CARBONLANG = "auto"
TTS_LANG = "tr"
TRT_LANG = "az"
LAN = {"Diller":
      [{"Türkçe":"tr",
       "İngilizce" : "en"}]}


import subprocess
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
import io
import glob

@register(pattern="^.tts2 (.*)", outgoing=True)
async def tts2(query):
    textx = await query.get_reply_message()
    mesj = query.pattern_match.group(1)
    parca = mesj.split(" ")[0]
    if parca == "kadın":
        cins = "female"
    else:
        cins = "male"

    message = mesj.replace(parca, "")
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await query.edit(
            "`Sözləri səsə çevirmək üçün: .tts2 oğlan/qadın Salam`")
        return

    mp3 = get(f"https://texttospeech.responsivevoice.org/v1/text:synthesize?text={message}&lang={TTS_LANG}&engine=g3&name=&pitch=0.5&rate=0.5&volume=1&key=DogeUserbot&gender={cins}").content
    with open("h.mp3", "wb") as audio:
        audio.write(mp3)
    await query.client.send_file(query.chat_id, "h.mp3", voice_note=True)
    os.remove("h.mp3")
    await query.delete()

@register(pattern="^.reddit ?(.*)", outgoing=True)
async def reddit(event):
    sub = event.pattern_match.group(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36 Avast/77.2.2153.120',
    }       

    if len(sub) < 1:
        await event.edit("`Xaiş olunur Subreddit istifadə edin. Nümunə: ``.reddit kopyamakarna`")
        return

    kaynak = get(f"https://www.reddit.com/r/{sub}/hot.json?limit=1", headers=headers).json()

    if not "kind" in kaynak:
        if kaynak["error"] == 404:
            await event.edit("`Belə bir Subreddit tapılmadı.`")
        elif kaynak["error"] == 429:
            await event.edit("`Redditdə xəta baş verir. 1 2 dəqiqə sonra yenidən yoxla.`")
        else:
            await event.edit("`Xəta baş verdi. Amma səbəbin bilmirəm`")
        return
    else:
        await event.edit("`Məlumatlar gətirilir...`")

        veri = kaynak["data"]["children"][0]["data"]
        mesaj = f"**{veri['title']}**\n⬆️{veri['score']}\n\nBy: __u/{veri['author']}__\n\n[Link](https://reddit.com{veri['permalink']})"
        try:
            resim = veri["url"]
            with open(f"reddit.jpg", 'wb') as load:
                load.write(get(resim).content)

            await event.client.send_file(event.chat_id, "reddit.jpg", caption=mesaj)
            os.remove("reddit.jpg")
        except Exception as e:
            print(e)
            await event.edit(mesaj + "\n\n`" + veri["selftext"] + "`")

@register(outgoing=True, pattern="^.xeber(?: |$)(.*)")
async def haber(event):
    TURLER = ["Gundem", "iqtisadiyyat", "cemiyyet", "maraqli", "region", "hadise"]
    cmd = event.pattern_match.group(1)
    if len(cmd) < 1:
            HABERURL = 'https://www.xezerxeber.az/news/'
    else:
        if cmd in TURLER:
            HABERURL = f'https://xezerxeber.az/news/{cmd}'
        else:
            await event.edit("`Belə bir kateqoriya yoxdur! Bunları yoxlayın: .xeber gundem/iqtisadiyyat/cemiyyet/politika/maraqli/reqion/hadise`")
            return
    await event.edit("`Xəbərlər gətirilir...`")

    haber = get(HABERURL).text
    kaynak = BeautifulSoup(haber, "lxml")
    haberdiv = kaynak.find_all("div", attrs={"class":"hblnContent"})
    i = 0
    HABERLER = ""
    while i < 3:
        HABERLER += "\n\n❗️**" + haberdiv[i].find("a").text + "**\n"
        HABERLER += haberdiv[i].find("p").text
        i += 1

    await event.edit(f"**Son dəqiqə xəbələri {cmd.title()}**" + HABERLER)

@register(outgoing=True, pattern="^.karbon ?(.*)")
async def karbon(e):
    cmd = e.pattern_match.group(1)
    if os.path.exists("@BrendUserBot-Karbon.jpg"):
        os.remove("@BrendUserBot-Karbon.jpg")

    if len(cmd) < 1:
        await e.edit("İstifadə: .karbon söz")    
    yanit = await e.get_reply_message()
    if yanit:
        cmd = yanit.message
    await e.edit("`Gözləyin...`")    

    r = get(f"https://carbonnowsh.herokuapp.com/?code={cmd}")

    with open("@BrendUserBot-Karbon.jpg", 'wb') as f:
        f.write(r.content)    

    await e.client.send_file(e.chat_id, file="@BrendUserBot-Karbon.jpg", force_document=True, caption="[BrendUserBot](https://t.me/BrendUserBot) ilə yaradıldı.")
    await e.delete()

@register(outgoing=True, pattern="^.crblang (.*)")
async def setlang(prog):
    global CARBONLANG
    CARBONLANG = prog.pattern_match.group(1)
    await prog.edit(f"Karbon modulu üçün standart dil {CARBONLANG} olaraq yaddaşa yazıldı.")


@register(outgoing=True, pattern="^.carbon")
async def carbon_api(e):
    """ carbon.now.sh için bir çeşit wrapper """
    await e.edit("`Gözləyin...`")
    CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
    global CARBONLANG
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)  # Girilen metin, modüle aktarılıyor.
    code = quote_plus(pcode)  # Çözülmüş url'ye dönüştürülüyor.
    await e.edit("`Proses başladı...\nHazırlanır: 25%`")
    if os.path.isfile("./carbon.png"):
        os.remove("./carbon.png")
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {'download.default_directory': './'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    await e.edit("`Proses davam edir...\nHazırlanır: 50%`")
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': download_path
        }
    }
    command_result = driver.execute("send_command", params)
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    # driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
    # driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
    await e.edit("`Proses davam edir...\nHazırlanır: 75%`")
    # İndirme için bekleniyor
    while not os.path.isfile("./carbon.png"):
        await sleep(0.5)
    await e.edit("`Proses davam edir...\nHazırlanır: 100%`")
    file = './carbon.png'
    await e.edit("`Şəkil yüklənir...`")
    await e.client.send_file(
        e.chat_id,
        file,
        caption="Bu şəkil [Carbon](https://carbon.now.sh/about/) istifadə edilərək yaradıldı,\
        \n[Dawn Labs](https://dawnlabs.io/) proyektidir.",
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )

    os.remove('./carbon.png')
    driver.quit()
    await e.delete() 


@register(outgoing=True, pattern=r"^\.img (.*)")
async def img_sampler(event):
    """.İmg əmri üçün sorğuya uyğun şəkilləri axtarın və qaytarın."""
    await event.edit("`Şəkil axtarılır..`")
    query = event.pattern_match.group(1)
    lim = findall(r"lim=\d+", query)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
    except IndexError:
        lim = 5
    response = googleimagesdownload()

   
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory",
    }

    
    paths = response.download(arguments)
    lst = paths[0][query]
    await event.client.send_file(
        await event.client.get_input_entity(event.chat_id), lst
    )
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await event.delete()


@register(outgoing=True, pattern=r"^\.google (.*)")
async def gsearch(q_event):
    """.google əmri google`da axtarış üçündür"""
    match = q_event.pattern_match.group(1)
    page = findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    try:
        search_args = (str(match), int(page))
        gsearch = GoogleSearch()
        gresults = await gsearch.async_search(*search_args)
        msg = ""
        for i in range(5):
            try:
                title = gresults["titles"][i]
                link = gresults["links"][i]
                desc = gresults["descriptions"][i]
                msg += f"[{title}]({link})\n`{desc}`\n\n"
            except IndexError:
                break
    except BaseException as g_e:
        return await q_event.edit(f"**Xəta : ** `{g_e}`")
    await q_event.edit(
        "**Axtarış Sorğusu:**\n`" + match + "`\n\n**Nəticələr:**\n" + msg, link_preview=False
    )


@register(outgoing=True, pattern=r"^.wiki (.*)")
async def wiki(wiki_q):
    """ .wiki komutu Vikipedi üzerinden bilgi çeker. """
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Belə bir məlumat tapılmadı.\n\n{error}")
        return
    except PageError as pageerror:
        await wiki_q.edit(f"Belə bir səhifə tapılmadı.\n\n{pageerror}")
        return
    result = summary(match)
    if len(result) >= 4096:
        file = open("wiki.txt", "w+")
        file.write(result)
        file.close()
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "wiki.txt",
            reply_to=wiki_q.id,
            caption="`Məlumat böyük olduğu üçün fayl formasında atılacaq...`",
        )
        if os.path.exists("wiki.txt"):
            os.remove("wiki.txt")
        return
    await wiki_q.edit("**Axtarma:**\n`" + match + "`\n\n**Tapılan:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"{match}` sözün Wikipedia sorğusu uğurla yerinə yetirildi!`")


@register(outgoing=True, pattern="^.ud (.*)")
async def urban_dict(ud_e):
    await ud_e.edit("Hazırlanır...")
    query = ud_e.pattern_match.group(1)
    try:
        define(query)
    except HTTPError:
        await ud_e.edit(f"Bağışlayın, {query} axtardım və heç bir məlumat tapmadım.")
        return
    mean = define(query)
    deflen = sum(len(i) for i in mean[0]["def"])
    exalen = sum(len(i) for i in mean[0]["example"])
    meanlen = deflen + exalen
    if int(meanlen) >= 0:
        if int(meanlen) >= 4096:
            await ud_e.edit("`Problem çox uzun olduğu üçün fayl kimi göndərirəm...`")
            file = open("urbandictionary.txt", "w+")
            file.write("Sual: " + query + "\n\nCavabı: " + mean[0]["def"] +
                       "\n\n" + "Nümunə: \n" + mean[0]["example"])
            file.close()
            await ud_e.client.send_file(
                ud_e.chat_id,
                "urbandictionary.txt",
                caption="`Problem çox uzun olduöu üçün fayl kimi göndərirəm...`")
            if os.path.exists("urbandictionary.txt"):
                os.remove("urbandictionary.txt")
            await ud_e.delete()
            return
        await ud_e.edit("Sual: **" + query + "**\n\nCavabı: **" +
                        mean[0]["def"] + "**\n\n" + "Nümunə: \n__" +
                        mean[0]["example"] + "__")
        if BOTLOG:
            await ud_e.client.send_message(
                BOTLOG_CHATID,
                query + "`UrbanDictionary sorğusu uğurla yerinə yetirildi!`")
    else:
        await ud_e.edit(query + "**üçün heç bir məlumat tapılmadı**")


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(event):
    if event.fwd_from:
        return
    ttss = event.pattern_match.group(1)
    rep_msg = None
    if event.is_reply:
        rep_msg = await event.get_reply_message()
    if len(ttss) < 1:
        if event.is_reply:
            sarki = rep_msg.text
        else:
            await event.edit("`Səsə çevirməyim üçün əmrin yanında bir mesaj yazmalısan.`")
            return

    await event.edit(f"__Mesajınız səsə çevrilir...__")
    chat = "@MrTTSbot"
    async with bot.conversation(chat) as conv:
        try:     
            await conv.send_message(f"/tomp3 {ttss}")
        except YouBlockedUserError:
            await event.reply(f"{chat} əngəlləmisən. Xaiş olunur qadağanı aç.`")
            return
        ses = await conv.wait_event(events.NewMessage(incoming=True,from_users=1678833172))
        await event.client.send_read_acknowledge(conv.chat_id)
        indir = await ses.download_media()
        voice = await asyncio.create_subprocess_shell(f"ffmpeg -i '{indir}' -c:a libopus 'MrTTSbot.ogg'")
        await voice.communicate()
        if os.path.isfile("MrTTSbot.ogg"):
            await event.client.send_file(event.chat_id, file="MrTTSbot.ogg", voice_note=True, reply_to=rep_msg)
            await event.delete()
            os.remove("MrTTSbot.ogg")
        else:
            await event.edit("`Bir xəta yanadı!`")


        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "Cümlə səsə çevirildi!")


@register(outgoing=True, pattern="^.imdb (.*)")
async def imdb(e):
    try:
        movie_name = e.pattern_match.group(1)
        remove_space = movie_name.split(' ')
        final_name = '+'.join(remove_space)
        page = get("https://www.imdb.com/find?ref_=nv_sr_fn&q=" + final_name +
                   "&s=all")
        lnk = str(page.status_code)
        soup = BeautifulSoup(page.content, 'lxml')
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext('td').findNext('td').text
        mov_link = "http://www.imdb.com/" + \
            odds[0].findNext('td').findNext('td').a['href']
        page1 = get(mov_link)
        soup = BeautifulSoup(page1.content, 'lxml')
        if soup.find('div', 'poster'):
            poster = soup.find('div', 'poster').img['src']
        else:
            poster = ''
        if soup.find('div', 'title_wrapper'):
            pg = soup.find('div', 'title_wrapper').findNext('div').text
            mov_details = re.sub(r'\s+', ' ', pg)
        else:
            mov_details = ''
        credits = soup.findAll('div', 'credit_summary_item')
        if len(credits) == 1:
            director = credits[0].a.text
            writer = 'Not available'
            stars = 'Not available'
        elif len(credits) > 2:
            director = credits[0].a.text
            writer = credits[1].a.text
            actors = []
            for x in credits[2].findAll('a'):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + ',' + actors[1] + ',' + actors[2]
        else:
            director = credits[0].a.text
            writer = 'Not available'
            actors = []
            for x in credits[1].findAll('a'):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + ',' + actors[1] + ',' + actors[2]
        if soup.find('div', "inline canwrap"):
            story_line = soup.find('div',
                                   "inline canwrap").findAll('p')[0].text
        else:
            story_line = 'Not available'
        info = soup.findAll('div', "txt-block")
        if info:
            mov_country = []
            mov_language = []
            for node in info:
                a = node.findAll('a')
                for i in a:
                    if "country_of_origin" in i['href']:
                        mov_country.append(i.text)
                    elif "primary_language" in i['href']:
                        mov_language.append(i.text)
        if soup.findAll('div', "ratingValue"):
            for r in soup.findAll('div', "ratingValue"):
                mov_rating = r.strong['title']
        else:
            mov_rating = 'Not available'
        await e.edit('<a href=' + poster + '>&#8203;</a>'
                     '<b>Başlıq : </b><code>' + mov_title + '</code>\n<code>' +
                     mov_details + '</code>\n<b>Reyting : </b><code>' +
                     mov_rating + '</code>\n<b>Ölkə : </b><code>' +
                     mov_country[0] + '</code>\n<b>Dil : </b><code>' +
                     mov_language[0] + '</code>\n<b>Direktor : </b><code>' +
                     director + '</code>\n<b>Yazıcı : </b><code>' + writer +
                     '</code>\n<b>Ulduzlar : </b><code>' + stars +
                     '</code>\n<b>IMDB Url : </b>' + mov_link +
                     '\n<b>Mövzu : </b>' + story_line,
                     link_preview=True,
                     parse_mode='HTML')
    except IndexError:
        await e.edit("Kino adını düz yazdığınızdan əmin olun.")


@register(outgoing=True, pattern=r"^\.trt(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if "trim" in event.raw_text:

        return
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "az"
    elif "-" in input_str:
        lan, text = input_str.split("-")
    else:
        await event.edit("**.trt** mesajlara cavab verərkən işləyir")
        return
    text = emoji.demojize(text.strip())
    lan = lan.strip()
    translator = Translator()
    try:
        translated = translator.translate(text, dest=lan)
        after_tr_text = translated.text
        output_str = """🌐Bu dildən `{}`\n🇦🇿Bu dilə çevrildi
\nMətn: {}""".format(
            translated.src, after_tr_text
        )
        await event.edit(output_str)
    except Exception as exc:
        await event.edit(str(exc))

@register(outgoing=True, pattern="^.yt (.*)")
async def _(event):
    try:
      from youtube_search import YoutubeSearch
    except:
      os.system("pip install youtube_search")
    from youtube_search import YoutubeSearch
    if event.fwd_from:
        return
    fin = event.pattern_match.group(1)
    stark_result = await event.edit("`Proses başladılır...`")
    results = YoutubeSearch(f"{fin}", max_results=5).to_dict()
    noob = "<b>YOUTUBE Axtarışı</b> \n\n"
    for moon in results:
      ytsorgusu = moon["id"]
      kek = f"https://www.youtube.com/watch?v={ytsorgusu}"
      stark_name = moon["title"]
      stark_chnnl = moon["channel"]
      total_stark = moon["duration"]
      stark_views = moon["views"]
      noob += (
        f"<b><u>Başlıq</u></b> ➠ <code>{stark_name}</code> \n"
        f"<b><u>Link</u></b> ➠  {kek} \n"
        f"<b><u>Kanal</u></b> ➠ <code>{stark_chnnl}</code> \n"
        f"<b><u>Video müddəti</u></b> ➠ <code>{total_stark}</code> \n"
        f"<b><u>İzlənmə</u></b> ➠ <code>{stark_views}</code> \n\n"
        )
      await stark_result.edit(noob, parse_mode="HTML")

@register(outgoing=True, pattern=r".rip(a|v) (.*)")
async def download_video(v_url):
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()

    await v_url.edit("`Hazırlanır...`")

    if type == "a":
        opts = {
            'format':
            'bestaudio',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'writethumbnail':
            True,
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl':
            '%(id)s.mp3',
            'quiet':
            True,
            'logtostderr':
            False
        }
        video = False
        song = True

    elif type == "v":
        opts = {
            'format':
            'best',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl':
            '%(id)s.mp4',
            'logtostderr':
            False,
            'quiet':
            True
        }
        song = False
        video = True

    try:
        await v_url.edit("`Lazımlı fayllar yüklənir...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await v_url.edit("`Yükləmək istədiyiniz fayl çox kiçikdir`")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "`Təsüf edirəmki məlumat verə bilməyəcəyəm. Səbəb: Ölkə qadağanı `")
        return
    except MaxDownloadsReached:
        await v_url.edit("`Limitin doldu :(`")
        return
    except PostProcessingError:
        await v_url.edit("`İstək sırasında 1 xəta əmələ gəldi.`")
        return
    except UnavailableVideoError:
        await v_url.edit("`Error UnavialableVideoError |//\\| Bu mesajı görürsənsə, çox güman ki, istifadəçi botunda _youtube_ modulu sıradan çıxdı.")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("`Lazımlı məlumatlar yüklənərkən xəta baş verdi.`")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await v_url.edit(f"`Musiqi yüklənir:`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(duration=int(rip_data['duration']),
                                       title=str(rip_data['title']),
                                       performer=str(rip_data['uploader']))
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Son toxunuşlar...",
                         f"{rip_data['title']}.mp3")))
        os.remove(f"{rip_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await v_url.edit(f"`Musiqi yüklənməyə hazırlanır:`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=rip_data['title'],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Son toxunuşlar...",
                         f"{rip_data['title']}.mp4")))
        os.remove(f"{rip_data['id']}.mp4")
        await v_url.delete()


def deEmojify(inputString):
    return get_emoji_regexp().sub(u'', inputString)

CmdHelp('scrapers').add_command(
    'img', '<rəqəm> <söz>', 'Googleda sürətli bir fotoşəkil axtarır, bir dəyər göstərməsəniz , nümunə: img10 dağ siçanı'
).add_command(
    'carbon', '<söz>', 'carbon.now.sh saytdan istifadə edərək mesajınıza karbon editi tətbiq edir..'
).add_command(
    'crblang', '<dil>', 'Carbon üçün parametrlər.'
).add_command(
    'karbon', '<söz>', 'Carbon ilə eynidir. Amma daha sürətlidir.'
).add_command(
    'google', '<söz>', 'Googledən axtarış edir.'
).add_command(
    'wiki', '<söz>', 'wikipediadan axtarış edir'
).add_command(
    'ud', '<terim>', 'Urban Dictionary axtarışının asan yolu.'
).add_command(
    'tts', '<söz>', 'Sözü səsə çevirin.'
).add_command(
    'lang', '<dil>', 'tts və trt üçün standart dil seçin.'
).add_command(
    'tts2', '<oğlan/qadın> <söz>', 'Mətni səsə çevirir.', 'tts2 oğlan salam'
).add_command(
    'trt', '<söz>', 'Asand tərcümə modulu.'
).add_command(
    'yt', '<söz>', 'Youtube üzərində axtarış edər.'
).add_command(
    'haber', '<Gundem/iqtisadiyyat/cemiyyet/maraqli/region/hadise>', 'Xəbərlər.'
).add_command(
    'imdb', '<Kino adı>', 'kino haqqında məlumat verir.'
).add_command(
    'ripa', '<url>', 'Youtube və başqa saytdan musiqi yükləmək üçündür.'
).add_command(
    'ripv', '<url>', 'Youtube və başqa saytdan video yükləmək üçündür.'
).add_info(
    '[Rip əmrini dəstəkləyən saytların siyahısı](https://ytdl-org.github.io/youtube-dl/supportedsites.html)'
).add()
