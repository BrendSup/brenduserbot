# 彡𝚕𝚌𝚓𝚗🎴 , t.me/elcjn
# modulu ogurlayan o peti petito


from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from telethon.tl.types import ChatAdminRights
from userbot.cmdhelp import CmdHelp
from userbot.events import register

NO_ADMIN = "`Admin deyilsiniz :(`"


async def get_call(event):
    geez = await event.client(getchat(event.chat_id))
    vcky = await event.client(getvc(geez.full_chat.call))
    return vcky.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i: i + n]


@register(outgoing=True, pattern=r"^\.bvc$", groups_only=True)
async def _(e):
    chat = await e.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await e.edit(NO_ADMIN)
    new_rights = ChatAdminRights(invite_users=True)
    try:
        await e.client(startvc(e.chat_id))
        await e.edit("`Səsli Söhbət başladılır...`")
    except Exception as ex:
        await e.edit(f"`{str(ex)}`")


@register(outgoing=True, pattern=r"^\.svc$", groups_only=True)
async def _(e):
    chat = await e.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await e.edit(NO_ADMIN)
    new_rights = ChatAdminRights(invite_users=True)
    try:
        await e.client(stopvc(await get_call(e)))
        await e.edit("`Səsi Söhbət sonlandırılır...`")
    except Exception as ex:
        await e.edit(f"`{str(ex)}`")


@register(outgoing=True, pattern=r"^\.dvc", groups_only=True)
async def _(e):
    await e.edit("`İstifadəçilər səsli söhbətə dəvət edilir...`")
    users = []
    z = 0
    async for x in e.client.iter_participants(e.chat_id):
        if not x.bot:
            users.append(x.id)
    hmm = list(user_list(users, 6))
    for p in hmm:
        try:
            await e.client(invitetovc(call=await get_call(e), users=p))
            z += 6
        except BaseException:
            pass
    await e.edit(f"`{z} nəfər istifadəçi səsli söhbətə çağırılır`")

CmdHelp('calls').add_command(
    'bvc', '', 'Səsli söhbət başladar.'
).add_command(
    'svc', '', 'Səsli söhbəti sonlandırar.'
).add_command(
    'dvc', '', 'Userləri səsliyə dəvət edər'
).add()
