from subprocess import PIPE
from subprocess import run as runapp
import pybase64
from userbot import CMD_HELP
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.hash (.*)")
async def gethash(hash_q):

    hashtxt_ = hash_q.pattern_match.group(1)
    hashtxt = open("hashdis.txt", "w+")
    hashtxt.write(hashtxt_)
    hashtxt.close()
    md5 = runapp(["md5sum", "hashdis.txt"], stdout=PIPE)
    md5 = md5.stdout.decode()
    sha1 = runapp(["sha1sum", "hashdis.txt"], stdout=PIPE)
    sha1 = sha1.stdout.decode()
    sha256 = runapp(["sha256sum", "hashdis.txt"], stdout=PIPE)
    sha256 = sha256.stdout.decode()
    sha512 = runapp(["sha512sum", "hashdis.txt"], stdout=PIPE)
    runapp(["rm", "hashdis.txt"], stdout=PIPE)
    sha512 = sha512.stdout.decode()
    ans = ("Text: `" + hashtxt_ + "`\nMD5: `" + md5 + "`SHA1: `" + sha1 +
           "`SHA256: `" + sha256 + "`SHA512: `" + sha512[:-1] + "`")
    if len(ans) > 4096:
        hashfile = open("hashes.txt", "w+")
        hashfile.write(ans)
        hashfile.close()
        await hash_q.client.send_file(
            hash_q.chat_id,
            "hashes.txt",
            reply_to=hash_q.id,
            caption="`Çox böyük, əvəzinə mətn faylı göndərir. `")
        runapp(["rm", "hashes.txt"], stdout=PIPE)
    else:
        await hash_q.reply(ans)


@register(outgoing=True, pattern="^.base64 (en|de) (.*)")
async def endecrypt(query):

    if query.pattern_match.group(1) == "en":
        lething = str(
            pybase64.b64encode(bytes(query.pattern_match.group(2),
                                     "utf-8")))[2:]
        await query.reply("Encoded: `" + lething[:-1] + "`")
    else:
        lething = str(
            pybase64.b64decode(bytes(query.pattern_match.group(2), "utf-8"),
                               validate=True))[2:]
        await query.reply("Decoded: `" + lething[:-1] + "`")

CmdHelp('hash').add_command(
    'base64', None, 'Verilən sətrin base64 kodlamasını tapın'
).add_command(
    'hash', None, 'Bir txt faylı yazıldıqda md5, sha1, sha256, sha512 sətirlərini tapın.'
).add()
