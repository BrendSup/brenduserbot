from . import LANGUAGE, LOGS, bot, PLUGIN_CHANNEL_ID
from userbot import language
from json import loads, JSONDecodeError
from os import path, remove
from telethon.tl.types import InputMessagesFilterDocument

pchannel = bot.get_entity(PLUGIN_CHANNEL_ID)
LOGS.info("Dil faylı yüklənir...")
LANGUAGE_JSON = None

for dil in bot.iter_messages(pchannel, filter=InputMessagesFilterDocument):
    if ((len(dil.file.name.split(".")) >= 2) and (dil.file.name.split(".")[1] == "brendjson")):
        if path.isfile(f"./userbot/language/{dil.file.name}"):
            try:
                LANGUAGE_JSON = loads(open(f"./userbot/language/{dil.file.name}", "r").read())
            except JSONDecodeError:
                dil.delete()
                remove(f"./userbot/language/{dil.file.name}")

                if path.isfile("./userbot/language/AZ.brendjson"):
                    LOGS.warn("Standart dil faylı istifadə olunur...")
                    LANGUAGE_JSON = loads(open(f"./userbot/language/AZ.brendjson", "r").read())
                else:
                    raise Exception("Belə fayl yoxdur")
        else:
            try:
                DOSYA = dil.download_media(file="./userbot/language/")
                LANGUAGE_JSON = loads(open(DOSYA, "r").read())
            except JSONDecodeError:
                dil.delete()
                if path.isfile("./userbot/language/AZ.brendjson"):
                    LOGS.warn("Standart dil faylı istifadə olunur...")
                    LANGUAGE_JSON = loads(open(f"./userbot/language/AZ.brendjson", "r").read())
                else:
                    raise Exception("Belə fayl yoxdur")
        break

if LANGUAGE_JSON == None:
    if path.isfile(f"./userbot/language/{LANGUAGE}.brendjson"):
        try:
            LANGUAGE_JSON = loads(open(f"./userbot/language/{LANGUAGE}.brendjson", "r").read())
        except JSONDecodeError:
            raise Exception("Belə fayl yoxdur")
    else:
        if path.isfile("./userbot/language/DEFAULT.brendjson"):
            LOGS.warn("Varsayılan dil dosyası kullanılıyor...")
            LANGUAGE_JSON = loads(open(f"./userbot/language/AZ.brendjson", "r").read())
        else:
            raise Exception(f"{LANGUAGE} faylı tapılmadı")

LOGS.info(f"{LANGUAGE_JSON['LANGUAGE']} dili yükləndi.")

def get_value (plugin = None, value = None):
    global LANGUAGE_JSON

    if LANGUAGE_JSON == None:
        raise Exception("Zəhmət olmasa əvvəlcə dil faylını yükləyin")
    else:
        if not plugin == None or value == None:
            Plugin = LANGUAGE_JSON.get("STRINGS").get(plugin)
            if Plugin == None:
                raise Exception("Xətalı Fayl")
            else:
                String = LANGUAGE_JSON.get("STRINGS").get(plugin).get(value)
                if String == None:
                    return Plugin
                else:
                    return String
        else:
            raise Exception("Yanlış plagin və ya string")
