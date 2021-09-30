import os
import qrcode
import barcode
from barcode.writer import ImageWriter
from urllib3 import PoolManager
from bs4 import BeautifulSoup
from userbot import CMD_HELP
from userbot.events import register
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("qrcode")

# ████████████████████████████████ #

@register(pattern=r"^.decode$", outgoing=True)
async def parseqr(qr_e):
    """ .decode əmr QR kodunu alır/fotoşəkildən Barkod məzmunu cavab verdi """
    downloaded_file_name = await qr_e.client.download_media(
        await qr_e.get_reply_message())

    files = {'f': open(downloaded_file_name, 'rb').read()}
    t_response = None

    try:
        http = PoolManager()
        t_response = http.request(
            'POST', "https://zxing.org/w/decode", fields=files)
        t_response = t_response.data
        http.clear()
    except:
        pass

    os.remove(downloaded_file_name)
    if not t_response:
        await qr_e.edit(LANG['ERROR'])
        return
    soup = BeautifulSoup(t_response, "html.parser")
    qr_contents = soup.find_all("pre")[0].text
    await qr_e.edit(qr_contents)


@register(pattern=r".barcode(?: |$)([\s\S]*)", outgoing=True)
async def barcode_read(event):
    """ .barcode Əmr olunan məzmunu ehtiva edən barkod yaradır. """
    await event.edit(LANG['TRYING'])
    input_str = event.pattern_match.group(1)
    message = f"{LANG['USAGE']} `.barcode <{LANG['TEXT']}>`"
    reply_msg_id = event.message.id
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message)
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        event.edit("SÖZDİZİMİ: `.barcode <söz>`")
        return

    bar_code_type = "code128"
    try:
        bar_code_mode_f = barcode.get(bar_code_type,
                                      message,
                                      writer=ImageWriter())
        filename = bar_code_mode_f.save(bar_code_type)
        await event.client.send_file(event.chat_id,
                                     filename,
                                     reply_to=reply_msg_id)
        os.remove(filename)
    except Exception as e:
        await event.edit(str(e))
        return
    await event.delete()


@register(pattern=r".makeqr(?: |$)([\s\S]*)", outgoing=True)
async def make_qr(makeqr):
    input_str = makeqr.pattern_match.group(1)
    message = f"{LANG['USAGE']}: `.makeqr <{LANG['TEXT']}>`"
    reply_msg_id = None
    if input_str:
        message = input_str
    elif makeqr.reply_to_msg_id:
        previous_message = await makeqr.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await makeqr.client.download_media(
                previous_message)
            m_list = None
            with open(downloaded_file_name, "rb") as file:
                m_list = file.readlines()
            message = ""
            for media in m_list:
                message += media.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("img_file.webp", "PNG")
    await makeqr.client.send_file(makeqr.chat_id,
                                  "img_file.webp",
                                  reply_to=reply_msg_id)
    os.remove("img_file.webp")
    await makeqr.delete()

CmdHelp('qrcode').add_command(
    'barcode', '<daxil>', 'Verilən məzmundan barkod hazırlayın.', 'barcode www.google.com'
).add_command(
    'decode', '<yanıtlama>', 'Barkod və ya QRKod kodunu açmaq üçün.'
).add_command(
    'makeqr', '<daxil>', 'Təqdim olunan məzmundan QR kodu hazırlayın.', 'makeqr www.google.com'
).add()
