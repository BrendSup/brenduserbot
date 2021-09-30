import asyncio
from getpass import getuser
from os import remove
from sys import executable
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.cmdhelp import CmdHelp

from userbot.language import get_value
LANG = get_value("evaluators")

@register(outgoing=True, pattern="^.eval(?: |$)(.*)")
async def evaluate(query):

    if query.is_channel and not query.is_group:
        await query.edit(LANG['FORBIDDEN_IN_CHANNEL'])
        return

    if query.pattern_match.group(1):
        expression = query.pattern_match.group(1)
    else:
        await query.edit(LANG['NEED_CODE'])
        return

    if (expression in ("userbot.session", "config.env")) or (expression == 'env'):
        await query.edit(LANG['WARNING'])
        return

    try:
        evaluation = str(eval(expression))
        if evaluation:
            if isinstance(evaluation, str):
                if len(evaluation) >= 4096:
                    file = open("brend.txt", "w+")
                    file.write(evaluation)
                    file.close()
                    await query.client.send_file(
                        query.chat_id,
                        "brend.txt",
                        reply_to=query.id,
                        caption=LANG['BIG_FILE'],
                    )
                    remove("brend.txt")
                    return
                await query.edit(f"**{LANG['QUERY']}: **\n`"
                                 f"{expression}"
                                 f"`\n**{LANG['RESULT']}: **\n`"
                                 f"{evaluation}"
                                 "`")
        else:
            await query.edit(f"**{LANG['QUERY']}: **\n`"
                             f"{expression}"
                             f"`\n**{LANG['result']}: **\n`{LANG['EMPTY_RESULT']}`")
    except Exception as err:
        await query.edit(f"**{LANG['QUERY']}: **\n`"
                         f"{expression}"
                         f"`\n**{LANG['ERROR']}: **\n"
                         f"`{err}`")

    if BOTLOG:
        await query.client.send_message(
            BOTLOG_CHATID,
            f"Eval sorğusu {expression} uğurla icra edilmişdir")


@register(outgoing=True, pattern=r"^.exec(?: |$)([\s\S]*)")
async def run(run_q):

    code = run_q.pattern_match.group(1)

    if run_q.is_channel and not run_q.is_group:
        await run_q.edit(LANG['FORBIDDEN_IN_CHANNEL'])
        return

    if not code:
        await run_q.edit(LANG['NEED_CODE'])
        return

    if (code in ("userbot.session", "config.env")) or code is 'env':
        await run_q.edit(LANG['WARNING'])
        return

    if len(code.splitlines()) <= 5:
        codepre = code
    else:
        clines = code.splitlines()
        codepre = clines[0] + "\n" + clines[1] + "\n" + clines[2] + \
            "\n" + clines[3] + "..."

    command = "".join(f"\n {l}" for l in code.split("\n.strip()"))
    process = await asyncio.create_subprocess_exec(
        executable,
        '-c',
        command.strip(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) \
        + str(stderr.decode().strip())

    if result:
        if len(result) > 4096:
            file = open("brend.txt", "w+")
            file.write(result)
            file.close()
            await run_q.client.send_file(
                run_q.chat_id,
                "brend.txt",
                reply_to=run_q.id,
                caption=LANG['BIG_FILE'],
            )
            remove("brend.txt")
            return
        await run_q.edit(f"**{LANG['QUERY']}: **\n`"
                         f"{codepre}"
                         f"`\n**{LANG['RESULT']}: **\n`"
                         f"{result}"
                         "`")
    else:
        await run_q.edit(f"**{LANG['QUERY']}: **\n`"
                         f"{codepre}"
                         f"`\n**{LANG['RESULT']}: **\n`{LANG['EMPTY_RESULT']}`")

    if BOTLOG:
        await run_q.client.send_message(
            BOTLOG_CHATID,
            "Exec sorgusu " + codepre + " uğurla icra edilmişdir")


@register(outgoing=True, pattern="^.term(?: |$)(.*)")
async def terminal_runner(term):

    curruser = getuser()
    command = term.pattern_match.group(1)
    try:
        from os import geteuid
        uid = geteuid()
    except ImportError:
        uid = "Bu deyil rəis!"

    if term.is_channel and not term.is_group:
        await term.edit(LANG['FORBIDDEN_IN_CHANNEL'])
        return

    if not command:
        await term.edit(LANG['NEED_CODE'])
        return

    if command in ("userbot.session", "config.env", "env"):
        await term.edit(LANG['WARNING'])
        return

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) \
        + str(stderr.decode().strip())

    if len(result) > 4096:
        output = open("brend.txt", "w+")
        output.write(result)
        output.close()
        await term.client.send_file(
            term.chat_id,
            "brend.txt",
            reply_to=term.id,
            caption=LANG['BIG_FILE'],
        )
        remove("brend.txt")
        return

    if uid == 0:
        await term.edit("`" f"{curruser}:~# {command}" f"\n{result}" "`")
    else:
        await term.edit("`" f"{curruser}:~$ {command}" f"\n{result}" "`")

    if BOTLOG:
        await term.client.send_message(
            BOTLOG_CHATID,
            "Terminal Əmri " + command + " müvəffəqiyyətlə başa çatdırıldı",
        )

CmdHelp('evaluators').add_command(
    'eval', '<əməliyyat>', 'Mini ifadələri qiymətləndirin.', 'eval 2+3'
).add_command(
    'exec', '<python kodu>', 'Kiçik pyton əmrlərini icra edin.', 'exec print(\"BrendUserbottan Salamlar!\")'
).add_command(
    'term', '<əməliyyat>', 'Serverinizdə bash əmrlərini və skriptlərini işə salın.', 'term ls'
).add()
