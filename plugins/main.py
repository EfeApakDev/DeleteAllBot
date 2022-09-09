import asyncio
import logging
from userbot import userbot
from pystark import Stark, Message
from pyrogram.errors import UserAlreadyParticipant, FloodWait


@Stark.cmd('temizle', description="GRUP VE KANALDAKİ TÜM MESAJLARI SİL")
async def main_func(bot: Stark, msg: Message):
    if msg.chat.type == "private":
        return
    if msg.chat.type != "channel":
        user = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
        if user.status not in ['creator', 'administrator']:
            return
        if not user.can_delete_messages:
            await msg.react(" bu yetkiye sahip değil`CanDeleteMessages`=mesaj silme!")
            return
    bot_id = (await bot.get_me()).id
    cm = await bot.get_chat_member(msg.chat.id, bot_id)
    if cm.status != "administrator":
        await msg.react("Admin Değilim beni Admin yapın!")
        return
    elif not cm.can_promote_members:
        await msg.react("Kullanıcıları terfi ettiremiyorum . ÇALIŞMAK İÇİN BU YETKİYE İHTİYACIM VAR.")
        return
    elif not cm.can_delete_messages:
        await msg.react("buradaki mesajları silemiyorum çalışmam için bu yetkiye ihtiyacım var.")
        return
    link = (await bot.get_chat(msg.chat.id)).invite_link
    try:
        await userbot.join_chat(link)
    except UserAlreadyParticipant:
        pass
    userbot_id = (await userbot.get_me()).id
    await bot.promote_chat_member(
        msg.chat.id,
        userbot_id,
        can_delete_messages=True
    )
    numbers = []
    while True:
        try:
            async for m in userbot.iter_history(msg.chat.id):
                numbers.append(m.message_id)
            break
        except FloodWait as e:
            await msg.react(f" beklemelisin : {e.x} saniye. \n\nTelegram Kısıtlamaları")
            await asyncio.sleep(e.x)
    id_lists = [numbers[i*100:(i+1)*100] for i in range((len(numbers)+100-1) // 100)]
    status = await msg.reply("Tüm Mesajları silmeye çalışıyorum...")
    for id_list in id_lists:
        while True:
            try:
                await userbot.delete_messages(msg.chat.id, id_list)
                break
            except FloodWait as e:
                await asyncio.sleep(e.x)
                Stark.log(str(e), logging.WARN)
    await msg.react("Başarılı! Her Şeyi Silindi. Daha fazla bot için @sancakbotlar'u ziyaret edin"")
    await status.delete(
    await userbot.leave_chat(msg.chat.id)
