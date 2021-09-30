#Tercumeden istifade eleme serefsiz
#Tercumeden istifade edenin atasiyam
#Tercumeden istifade eleme ay anasi qehbe
#Tercumeni istifade eden peyserdi (qizdirsa qehbedi)
#Ekenin anasinin amciğini sapalagliyim
# @Mr_HD_20

import io
from re import match
from selenium import webdriver
from asyncio import sleep
from selenium.webdriver.chrome.options import Options
from userbot.events import register
from userbot import GOOGLE_CHROME_BIN, CHROME_DRIVER, CMD_HELP
from userbot.cmdhelp import CmdHelp

from userbot.language import get_value
LANG = get_value("screencapture")

@register(pattern=r".skrin (.*)", outgoing=True)
async def capture(url):
    await url.edit(LANG['TRYING'])
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    input_str = url.pattern_match.group(1)
    link_match = match(r'\bhttps?://.*\.\S+', input_str)
    if link_match:
        link = link_match.group()
    else:
        await url.edit(LANG['INVALID_URL'])
        return
    driver.get(link)
    height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
    )
    width = driver.execute_script(
        "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
    )
    driver.set_window_size(width + 125, height + 125)
    wait_for = height / 1000
    await url.edit(f"{LANG['TAKING']}\
    \n`{LANG['HEIGHT']}: {height} {LANG['PIXEL']}`\
    \n`{LANG['WIDTH']}: {width} {LANG['PIXEL']}`" + 
    LANG['WAIT'] % str(wait_for))
    await sleep(int(wait_for))
    im_png = driver.get_screenshot_as_png()

    driver.close()
    message_id = url.message.id
    if url.reply_to_msg_id:
        message_id = url.reply_to_msg_id
    with io.BytesIO(im_png) as out_file:
        out_file.name = "ekran_goruntusu.png"
        await url.edit(LANG['UPLOADING'])
        await url.client.send_file(url.chat_id,
                                   out_file,
                                   caption=input_str,
                                   force_document=True,
                                   reply_to=message_id)

CmdHelp('skrin').add_command(
    'skrin', '<url>', 'Göstərilən web saytından bir ekran görüntüsü alar ve göndərər.', 'skrin https://google.az'
).add()
