class script(object):
    START_TXT = """𝑯𝒆𝒚 {}, {}
    
🚀 𝑴𝒆𝒆𝒕 𝒚𝒐𝒖𝒓 𝒑𝒆𝒓𝒔𝒐𝒏𝒂𝒍 𝑴𝒐𝒗𝒊𝒆 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕!  𝑨𝒅𝒅 𝒎𝒆 𝒕𝒐 𝒚𝒐𝒖𝒓 𝒈𝒓𝒐𝒖𝒑 𝒂𝒏𝒅 𝒘𝒂𝒕𝒄𝒉 𝒕𝒉𝒆 𝒎𝒂𝒈𝒊𝒄 𝒉𝒂𝒑𝒑𝒆𝒏. 𝑰’𝒍𝒍 𝒊𝒏𝒔𝒕𝒂𝒏𝒕𝒍𝒚 𝒅𝒆𝒍𝒊𝒗𝒆𝒓 𝒎𝒐𝒗𝒊𝒆𝒔 𝒐𝒓 𝒔𝒆𝒓𝒊𝒆𝒔 — 𝒏𝒐 𝒅𝒆𝒍𝒂𝒚𝒔, 𝒏𝒐 𝒔𝒆𝒂𝒓𝒄𝒉𝒊𝒏𝒈! 💥  𝑮𝒓𝒐𝒖𝒑 𝒐𝒓 𝑷𝑴? 𝑰’𝒗𝒆 𝒈𝒐𝒕 𝒚𝒐𝒖 𝒄𝒐𝒗𝒆𝒓𝒆𝒅. 😎

𝑷𝒐𝒘𝒆𝒓𝒆𝒅 𝒃𝒚: <a href="https://t.me/hd_cinema_updates">𝑯𝑫 𝑪𝒊𝒏𝒆𝒎𝒂</a>"""

    HELP_TXT = """<b>𝑻𝒂𝒑 𝒕𝒉𝒆 𝒃𝒖𝒕𝒕𝒐𝒏𝒔 𝒃𝒆𝒍𝒐𝒘 𝒕𝒐 𝒗𝒊𝒆𝒘 𝒉𝒆𝒍𝒑𝒇𝒖𝒍 𝒅𝒐𝒄𝒖𝒎𝒆𝒏𝒕𝒂𝒕𝒊𝒐𝒏 𝒇𝒐𝒓 𝒆𝒂𝒄𝒉 𝒎𝒐𝒅𝒖𝒍𝒆, 𝒊𝒏𝒄𝒍𝒖𝒅𝒊𝒏𝒈 𝒉𝒐𝒘 𝒕𝒐 𝒖𝒔𝒆 𝒕𝒉𝒆𝒎.........</b>"""

    TELE_TXT = """<b>/telegraph – 𝑱𝒖𝒔𝒕 𝒔𝒆𝒏𝒅 𝒎𝒆 𝒂 𝒑𝒉𝒐𝒕𝒐 𝒐𝒓 𝒗𝒊𝒅𝒆𝒐 𝒖𝒏𝒅𝒆𝒓 5𝑴𝑩 𝒂𝒏𝒅 𝑰’𝒍𝒍 𝒖𝒑𝒍𝒐𝒂𝒅 𝒊𝒕 𝒕𝒐 𝑻𝒆𝒍𝒆𝒈𝒓𝒂𝒑𝒉 𝒇𝒐𝒓 𝒚𝒐𝒖!

𝑵𝒐𝒕𝒆: 𝑻𝒉𝒊𝒔 𝒄𝒐𝒎𝒎𝒂𝒏𝒅 𝒘𝒐𝒓𝒌𝒔 𝒊𝒏 𝒃𝒐𝒕𝒉 𝒈𝒓𝒐𝒖𝒑𝒔 𝒂𝒏𝒅 𝒑𝒓𝒊𝒗𝒂𝒕𝒆 𝒄𝒉𝒂𝒕 𝒘𝒊𝒕𝒉 𝒕𝒉𝒆 𝒃𝒐𝒕.</b>"""

    FORCESUB_TEXT = """<b>
𝑯𝒆𝒚 𝒕𝒉𝒆𝒓𝒆! 😊
𝑻𝒐 𝒈𝒆𝒕 𝒕𝒉𝒆 𝒎𝒐𝒗𝒊𝒆 𝒚𝒐𝒖 𝒂𝒔𝒌𝒆𝒅 𝒇𝒐𝒓, 𝒋𝒖𝒔𝒕 𝒎𝒂𝒌𝒆 𝒔𝒖𝒓𝒆 𝒚𝒐𝒖’𝒗𝒆 𝒋𝒐𝒊𝒏𝒆𝒅 𝒐𝒖𝒓 𝒐𝒇𝒇𝒊𝒄𝒊𝒂𝒍 𝒄𝒉𝒂𝒏𝒏𝒆𝒍.

👉 𝑻𝒂𝒑 𝒕𝒉𝒆 “𝑱𝒐𝒊𝒏 𝑼𝒑𝒅𝒂𝒕𝒆 𝑪𝒉𝒂𝒏𝒏𝒆𝒍” 𝒃𝒖𝒕𝒕𝒐𝒏 𝒃𝒆𝒍𝒐𝒘, 𝒕𝒉𝒆𝒏 𝒉𝒊𝒕 “𝑹𝒆𝒒𝒖𝒆𝒔𝒕 𝒕𝒐 𝑱𝒐𝒊𝒏”.
𝑶𝒏𝒄𝒆 𝒚𝒐𝒖'𝒓𝒆 𝒊𝒏, 𝒄𝒐𝒎𝒆 𝒃𝒂𝒄𝒌 𝒂𝒏𝒅 𝒑𝒓𝒆𝒔𝒔 “𝑻𝒓𝒚 𝑨𝒈𝒂𝒊𝒏” 𝒕𝒐 𝒖𝒏𝒍𝒐𝒄𝒌 𝒚𝒐𝒖𝒓 𝒎𝒐𝒗𝒊𝒆. 🎬

𝑰𝒕’𝒔 𝒒𝒖𝒊𝒄𝒌 𝒂𝒏𝒅 𝒆𝒂𝒔𝒚!
    </b>"""

    TTS_TXT = """
<b>👉 𝐉𝐮𝐬𝐭 𝐬𝐞𝐧𝐝 /tts 𝐭𝐨 𝐭𝐫𝐲 𝐨𝐮𝐭 𝐭𝐡𝐢𝐬 𝐜𝐨𝐨𝐥 𝐭𝐞𝐱𝐭-𝐭𝐨-𝐬𝐩𝐞𝐞𝐜𝐡 𝐟𝐞𝐚𝐭𝐮𝐫𝐞! 🔊</b>"""

    DISCLAIMER_TXT = """
    <b>📌 DISCLAIMER</b>

    <b>This is an open-source project developed for educational and informational purposes only.</b>

    All files indexed by this bot are either <u>freely available on the internet</u> or <u>uploaded by third parties</u>. This bot only helps users by making such content easier to search and access — it does <u>not host or store any content</u> on its own servers.

    <u>We fully respect all copyright laws</u> and work in compliance with <b>DMCA</b> and <b>EUCD</b> regulations. If you believe any file indexed by this bot violates your rights or intellectual property, please <u>contact us immediately</u> to request removal.

    <u>This bot does not promote piracy</u>. It is strictly prohibited to <u>download, reproduce, stream, or share</u> any content without proper authorization from the original copyright holder.

    <b>Note:</b> This bot is only indexing files that are already publicly available on <b>Telegram</b> and does <u>not claim ownership</u> over any of the content.

    🔧 <b>Maintained by:</b> <a href='https://t.me/JISSHU_BOTS'>Jisshu Bots</a>"""

    ABOUT_TEXT = """<blockquote><b>‣ ᴍʏ ɴᴀᴍᴇ : Jisshu filter bot
‣ ᴄʀᴇᴀᴛᴏʀ : <a href='https://t.me/JISSHU_BOTS'>Jisshu Bots &lt;/&gt;</a>
‣ ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ
‣ ʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ
‣ ᴅᴀᴛᴀ ʙᴀsᴇ : ᴍᴏɴɢᴏ ᴅʙ
‣ ʜᴏsᴛᴇᴅ ᴏɴ  :  ᴡᴇʙ
‣ ʙᴜɪʟᴅ sᴛᴀᴛᴜs : V-4.1 [sᴛᴀʙʟᴇ]</b></blockquote>"""

    SUPPORT_GRP_MOVIE_TEXT = """<b>ʜᴇʏ {}

ɪ ғᴏᴜɴᴅ {} ʀᴇsᴜʟᴛs 🎁,
ʙᴜᴛ ɪ ᴄᴀɴ'ᴛ sᴇɴᴅ ʜᴇʀᴇ 🤞🏻
ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ʀᴇǫᴜᴇsᴛ ɢʀᴏᴜᴘ ᴛᴏ ɢᴇᴛ ✨</b>"""

    CHANNELS = """
<u>ᴏᴜʀ ᴀʟʟ ɢʀᴏᴜᴘꜱ ᴀɴᴅ ᴄʜᴀɴɴᴇʟꜱ</u> 

▫ ᴀʟʟ ʟᴀᴛᴇꜱᴛ ᴀɴᴅ ᴏʟᴅ ᴍᴏᴠɪᴇꜱ & ꜱᴇʀɪᴇꜱ.
▫ ᴀʟʟ ʟᴀɴɢᴜᴀɢᴇꜱ ᴍᴏᴠɪᴇꜱ ᴀᴠᴀɪʟᴀʙʟᴇ.
▫ ᴀʟᴡᴀʏꜱ ᴀᴅᴍɪɴ ꜱᴜᴘᴘᴏʀᴛ.
▫ 𝟸𝟺x𝟽 ꜱᴇʀᴠɪᴄᴇꜱ ᴀᴠᴀɪʟᴀʙʟᴇ."""

    JISSHUPREMIUM_TXT = """
𝑬𝒏𝒋𝒐𝒚𝒊𝒏𝒈 𝒕𝒉𝒆 𝒃𝒐𝒕? 𝑾𝒂𝒏𝒕 𝒕𝒐 𝒓𝒆𝒎𝒐𝒗𝒆 𝒂𝒅𝒔?

𝒀𝒐𝒖 𝒄𝒂𝒏 𝒈𝒆𝒕 𝒐𝒖𝒓 𝒑𝒓𝒆𝒎𝒊𝒖𝒎 𝒔𝒆𝒓𝒗𝒊𝒄𝒆 𝒃𝒚:
🔹 𝑩𝒖𝒚𝒊𝒏𝒈 𝑷𝒓𝒆𝒎𝒊𝒖𝒎
𝒐𝒓
🔹 𝑺𝒉𝒂𝒓𝒊𝒏𝒈 𝒕𝒉𝒆 𝒃𝒐𝒕 𝒘𝒊𝒕𝒉 𝒚𝒐𝒖𝒓 𝒇𝒓𝒊𝒆𝒏𝒅𝒔 𝒕𝒐 𝒖𝒏𝒍𝒐𝒄𝒌 𝒊𝒕 𝒇𝒐𝒓 𝒇𝒓𝒆𝒆!

𝑻𝒉𝒂𝒏𝒌𝒔 𝒇𝒐𝒓 𝒔𝒖𝒑𝒑𝒐𝒓𝒕𝒊𝒏𝒈 𝒖𝒔! 💖"""

    LOGO = """
sᴛᴀʀᴛɪɴɢ....
sᴜᴄᴄᴇssғᴜʟʟʏ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ"""

    RESTART_TXT = """
<b>Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ !
>> {}

📅 Dᴀᴛᴇ : <code>{}</code>
⏰ Tɪᴍᴇ : <code>{}</code>
🌐 Tɪᴍᴇᴢᴏɴᴇ : <code>Asia/Kolkata</code>
🛠️ Bᴜɪʟᴅ Sᴛᴀᴛᴜs: <code>v-3.1.2 [ Sᴛᴀʙʟᴇ ]</code>

If there is an error, ask in the support group @Jisshu_support</b>"""

    STATUS_TXT = """<b><u>♻️ ʙᴏᴛ ᴅᴀᴛᴀʙᴀsᴇ </u>

» ᴛᴏᴛᴀʟ ᴜsᴇʀs - <code>{}</code>
» ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘs - <code>{}</code>
» ᴜsᴇᴅ sᴛᴏʀᴀɢᴇ - <code>{} / {}</code>

<u>📁 ꜰɪʟᴇs ᴅᴀᴛᴀʙᴀsᴇ </u>

» ᴛᴏᴛᴀʟ ꜰɪʟᴇs - <code>{}</code>
» ᴜsᴇᴅ sᴛᴏʀᴀɢᴇ - <code>{} / {}</code>

<u>🤖 ʙᴏᴛ ᴅᴇᴛᴀɪʟs </u>

» ᴜᴘᴛɪᴍᴇ - <code>{}</code>
» ʀᴀᴍ - <code>{}%</code>
» ᴄᴘᴜ - <code>{}%</code></b>"""

    NEW_USER_TXT = """<b>#New_User {}

≈ ɪᴅ:- <code>{}</code>
≈ ɴᴀᴍᴇ:- {}</b>"""

    NEW_GROUP_TXT = """#New_Group {}

Group name - {}
Id - <code>{}</code>
Group username - @{}
Group link - {}
Total members - <code>{}</code>
User - {}"""

    REQUEST_TXT = """<b>📜 ᴜꜱᴇʀ - {}
📇 ɪᴅ - <code>{}</code>

🎁 ʀᴇǫᴜᴇꜱᴛ ᴍꜱɢ - <code>{}</code></b>"""

    IMDB_TEMPLATE_TXT = """
<b>ʜᴇʏ {message.from_user.mention}, ʜᴇʀᴇ ɪꜱ ᴛʜᴇ ʀᴇꜱᴜʟᴛꜱ ꜰᴏʀ ʏᴏᴜʀ ǫᴜᴇʀʏ {search}.

🍿 Title: {title}
🎃 Genres: {genres}
📆 Year: {release_date}
⭐ Rating: {rating} / 10</b>
"""

    FILE_CAPTION = """<b>{file_name}</b>"""

    ALRT_TXT = """ᴡʜᴀᴛ ᴀʀᴇ ʏᴏᴜ sᴇᴀʀᴄʜɪɴɢ !?"""

    OLD_ALRT_TXT = """ʏᴏᴜ ᴀʀᴇ ᴜsɪɴɢ ᴍʏ ᴏʟᴅ ᴍᴇssᴀɢᴇs..sᴇɴᴅ ᴀ ɴᴇᴡ ʀᴇǫᴜᴇsᴛ.."""

    NO_RESULT_TXT = """<b>ᴛʜɪs ᴍᴇssᴀɢᴇ ɪs ɴᴏᴛ ʀᴇʟᴇᴀsᴇᴅ ᴏʀ ᴀᴅᴅᴇᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ 🙄</b>"""

    I_CUDNT = """🤧 𝗛𝗲𝗹𝗹𝗼 {}

𝗜 𝗰𝗼𝘂𝗹𝗱𝗻'𝘁 𝗳𝗶𝗻𝗱 𝗮𝗻𝘆 𝗺𝗼𝘃𝗶𝗲 𝗼𝗿 𝘀𝗲𝗿𝗶𝗲𝘀 𝗶𝗻 𝘁𝗵𝗮𝘁 𝗻𝗮𝗺𝗲.. 😐"""

    I_CUD_NT = """😑 𝗛𝗲𝗹𝗹𝗼 {}

𝗜 𝗰𝗼𝘂𝗹𝗱𝗻'𝘁 𝗳𝗶𝗻𝗱 𝗮𝗻𝘆𝘁𝗵𝗶𝗻𝗴 𝗿𝗲𝗹𝗮𝘁𝗲𝗱 𝘁𝗼 𝘁𝗵𝗮𝘁 😞... 𝗰𝗵𝗲𝗰𝗸 𝘆𝗼𝘂𝗿 𝘀𝗽𝗲𝗹𝗹𝗶𝗻𝗴."""

    CUDNT_FND = """🤧 𝗛𝗲𝗹𝗹𝗼 {}

𝗜 𝗰𝗼𝘂𝗹𝗱𝗻'𝘁 𝗳𝗶𝗻𝗱 𝗮𝗻𝘆𝘁𝗵𝗶𝗻𝗴 𝗿𝗲𝗹𝗮𝘁𝗲𝗱 𝘁𝗼 𝘁𝗵𝗮𝘁 𝗱𝗶𝗱 𝘆𝗼𝘂 𝗺𝗲𝗮𝗻 𝗮𝗻𝘆 𝗼𝗻𝗲 𝗼𝗳 𝘁𝗵𝗲𝘀𝗲 ?? 👇"""

    FONT_TXT = """<b>ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴍᴏᴅᴇ ᴛᴏ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ꜰᴏɴᴛs sᴛʏʟᴇ, ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ʟɪᴋᴇ ᴛʜɪs ꜰᴏʀᴍᴀᴛ

<code>/font hi how are you</code></b>"""

    SPECIAL_TXT = """ Here Is My Some Special Features Broh ! """

    EARN_TEXT = """<b><i><blockquote>💸 ʜᴏᴡ ᴛᴏ ᴇᴀʀɴ ᴍᴏɴᴇʏ ʙʏ ᴛʜɪs ʙᴏᴛ - </blockquote>

1:- ʏᴏᴜ ᴍᴜꜱᴛ ʜᴀᴠᴇ ᴀᴛʟᴇᴀꜱᴛ ᴏɴᴇ ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴍɪɴɪᴍᴜᴍ 100 ᴍᴇᴍʙᴇʀꜱ.

2:- ᴍᴀᴋᴇ ᴛʜɪs <a href=https://t.me/{}</a> ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ.

3:- ᴄʀᴇᴀᴛᴇ ᴀᴄᴄᴏᴜɴᴛ ᴏɴ ᴀɴʏ sʜᴏʀᴛɴᴇʀ ʟɪᴋᴇ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴜsᴇ ᴛʜɪs ʙᴇsᴛ sʜᴏʀᴛɴᴇʀ <a href=https://linkmonetizer.in/ref/jisshu>Best Shortner</a>.

4:- ᴛʜᴇɴ sᴇᴛ ʏᴏᴜʀ sʜᴏʀᴛɴᴇʀ ᴅᴇᴛᴀɪʟs ʙʏ ᴛʜɪs ꜰᴏʀᴍᴀᴛ 👇

<code>/set_verify linkmonetizer.in fcee6bbc628cfc61229a2d808e1b0ee3315a0f5e</code>

<code>/set_verify_2 linkmonetizer.in fcee6bbc628cfc61229a2d808e1b0ee3315a0f5e</code>

<code>/set_verify_3 linkmonetizer.in fcee6bbc628cfc61229a2d808e1b0ee3315a0f5e</code>

<code>/set_tutorial https://t.me/Jisshu_developer</code>

<code>/set_tutorial_2 https://t.me/Jisshu_developer</code>

<code>/set_tutorial_3 https://t.me/Jisshu_developer</code>

<code>/set_time_2 300</code>

<code>/set_time_3 300</code>

<code>/set_fsub -100*******</code>

<code>/set_log -100*******</code>

ʏᴏᴜ ᴄᴀɴ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀʟʟ ᴅᴇᴛᴀɪʟs ʙʏ /details ᴄᴏᴍᴍᴀɴᴅ

💯 ɴᴏᴛᴇ - ᴛʜɪs ʙᴏᴛ ɪs ꜰʀᴇᴇ ᴛᴏ ᴀʟʟ, ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘs ᴀɴᴅ ᴇᴀʀɴ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏɴᴇʏ.</i></b>"""

    VERIFICATION_TEXT = """<b>👋 ʜᴇʏ {} {},

📌 <u>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ ᴛᴏᴅᴀʏ, ᴘʟᴇᴀꜱᴇ ᴄʟɪᴄᴋ ᴏɴ ᴠᴇʀɪғʏ & ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇꜱꜱ ғᴏʀ ᴛɪʟʟ ɴᴇxᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ</u>

#ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ:- 1/3 ✓

ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴅɪʀᴇᴄᴛ ғɪʟᴇꜱ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴꜱ ᴛʜᴇɴ ʙᴜʏ ʙᴏᴛ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ 😊

💶 sᴇɴᴅ /plan ᴛᴏ ʙᴜʏ sᴜʙsᴄʀɪᴘᴛɪᴏɴ</b>"""

    VERIFY_COMPLETE_TEXT = """<b>👋 ʜᴇʏ {},

ʏᴏᴜ ʜᴀᴠᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴛʜᴇ 1st ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ✓

ɴᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ɴᴇxᴛ <code>{}</code></b>"""

    SECOND_VERIFICATION_TEXT = """<b>👋 ʜᴇʏ {} {},

📌 <u>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪꜰɪᴇᴅ, ᴛᴀᴘ ᴏɴ ᴛʜᴇ ᴠᴇʀɪꜰʏ ʟɪɴᴋ ᴀɴᴅ ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ᴛɪʟʟ ɴᴇxᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ</u>

#ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ:- 2/3

ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴅɪʀᴇᴄᴛ ғɪʟᴇꜱ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴꜱ ᴛʜᴇɴ ʙᴜʏ ʙᴏᴛ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ 😊

💶 sᴇɴᴅ /plan ᴛᴏ ʙᴜʏ sᴜʙsᴄʀɪᴘᴛɪᴏɴ</b>"""

    SECOND_VERIFY_COMPLETE_TEXT = """<b>👋 ʜᴇʏ {},

ʏᴏᴜ ʜᴀᴠᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴛʜᴇ 2nd ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ✓

ɴᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ɴᴇxᴛ <code>{}</code></b>"""

    THIRDT_VERIFICATION_TEXT = """<b>👋 ʜᴇʏ {},
    
📌 <u>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪꜰɪᴇᴅ ᴛᴏᴅᴀʏ, ᴛᴀᴘ ᴏɴ ᴛʜᴇ ᴠᴇʀɪꜰʏ ʟɪɴᴋ & ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ɴᴇxᴛ ꜰᴜʟʟ ᴅᴀʏ.</u>

#ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ:- 3/3

ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴅɪʀᴇᴄᴛ ꜰɪʟᴇs ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴛᴀᴋᴇ ᴘʀᴇᴍɪᴜᴍ sᴇʀᴠɪᴄᴇ (ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪꜰʏ)</b>"""

    THIRDT_VERIFY_COMPLETE_TEXT = """<b>👋 ʜᴇʏ {},
    
ʏᴏᴜ ʜᴀᴠᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴛʜᴇ 3rd ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ✓

ɴᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ɴᴇxᴛ ꜰᴜʟʟ ᴅᴀʏ </b>"""

    VERIFIED_LOG_TEXT = """<b><u>☄ є∂ιтн ᴜsᴇʀ ᴠᴇʀɪꜰɪᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ ☄</u>

⚡️ ɴᴀᴍᴇ:- {} [ <code>{}</code> ] 
📆 ᴅᴀᴛᴇ:- <code>{} </code></b>

#edith_verified_{}_completed"""

    MOVIES_UPDATE_TXT = """<b>#𝑵𝒆𝒘_𝑭𝒊𝒍𝒆_𝑨𝒅𝒅𝒆𝒅 ✅
**🍿 Title:** {title}
**🎃 Genres:** {genres}
**📆 Year:** {year}
**⭐ Rating:** {rating} / 10
</b>"""

    PREPLANS_TXT = """<b>👋 ʜᴇʏ {},

<blockquote>🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ ʙᴇɴɪꜰɪᴛꜱ:</blockquote>

❏ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋꜱ
❏ ɢᴇᴛ ᴅɪʀᴇᴄᴛ ғɪʟᴇs   
❏ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ 
❏ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ                         
❏ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs                           
❏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs ᴀɴᴅ sᴇʀɪᴇs                                                                        
❏ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ                              
❏ ʀᴇǫᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 𝟷ʜ [ ɪꜰ ᴀᴠᴀɪʟᴀʙʟᴇ ]

⛽️ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ: /myplan
</b>"""

    PREPLANSS_TXT = """<b>👋 ʜᴇʏ {}
    
<blockquote>🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ ʙᴇɴɪꜰɪᴛꜱ:</blockquote>

❏ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋꜱ
❏ ɢᴇᴛ ᴅɪʀᴇᴄᴛ ғɪʟᴇs   
❏ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ 
❏ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ                         
❏ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs                           
❏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs ᴀɴᴅ sᴇʀɪᴇs                                                                        
❏ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ                              
❏ ʀᴇǫᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 𝟷ʜ [ ɪꜰ ᴀᴠᴀɪʟᴀʙʟᴇ ]

⛽️ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ: /myplan
</b>"""

    OTHER_TXT = """<b>👋 ʜᴇʏ {},
    
🎁 <u>ᴏᴛʜᴇʀ ᴘʟᴀɴ</u>
⏰ ᴄᴜꜱᴛᴏᴍɪꜱᴇᴅ ᴅᴀʏꜱ
💸 ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴅᴀʏꜱ ʏᴏᴜ ᴄʜᴏᴏꜱᴇ

🏆 ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴀ ɴᴇᴡ ᴘʟᴀɴ ᴀᴘᴀʀᴛ ꜰʀᴏᴍ ᴛʜᴇ ɢɪᴠᴇɴ ᴘʟᴀɴ, ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴛᴀʟᴋ ᴛᴏ ᴏᴜʀ <a href='https://telegram.dog/JisshuDeveloperBot'>ᴏᴡɴᴇʀ</a> ᴅɪʀᴇᴄᴛʟʏ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴏɴ ᴛʜᴇ ᴄᴏɴᴛᴀᴄᴛ ʙᴜᴛᴛᴏɴ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ.
    
👨‍💻 ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴏᴡɴᴇʀ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ᴏᴛʜᴇʀ ᴘʟᴀɴ.

➛ ᴜꜱᴇ /plan ᴛᴏ ꜱᴇᴇ ᴀʟʟ ᴏᴜʀ ᴘʟᴀɴꜱ ᴀᴛ ᴏɴᴄᴇ.
➛ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ ʙʏ ᴜꜱɪɴɢ : /myplan</b>"""

    FREE_TXT = """<b>👋 ʜᴇʏ {}
    
<blockquote>🎖️ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ :</blockquote>

 ❏ 𝟶𝟷𝟻₹    ➠    𝟶𝟷 ᴡᴇᴇᴋꜱ
 ❏ 𝟶𝟹𝟿₹    ➠    𝟶𝟷 ᴍᴏɴᴛʜ
 ❏ 𝟶𝟽𝟻₹    ➠    𝟶𝟸 ᴍᴏɴᴛʜ
 ❏ 𝟷𝟷𝟶₹    ➠    𝟶𝟹 ᴍᴏɴᴛʜ
 ❏ 𝟷𝟿𝟿₹    ➠    𝟶𝟼 ᴍᴏɴᴛʜ
 ❏ 𝟹𝟼𝟶₹    ➠    𝟷𝟸 ᴍᴏɴᴛʜ

🆔 ᴜᴘɪ ɪᴅ ➩ <code>jishan@fam</code> [ᴛᴀᴘ ᴛᴏ ᴄᴏᴘʏ]
 
⛽️ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ: /myplan

🏷️ <a href='https://telegram.dog/JisshuDeveloperBot'>ᴘʀᴇᴍɪᴜᴍ ᴘʀᴏᴏꜰ</a>

‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ.
‼️ ɢɪᴠᴇ ᴜꜱ ꜱᴏᴍᴇᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴘʀᴇᴍɪᴜᴍ ʟɪꜱᴛ.
</b>"""

    ADMIN_CMD_TXT_TO1 = """<b><blockquote>
--------------Index File--------------
➩ /index - Index all files
--------------Leave Link--------------
➩ /leave {group ID} - Leave the specified group
-------------Send Message-------------
➩ /send {user name} - Use this command as a reply to any message
----------------Ban User---------------
➩ /ban {user name} - Ban user 
➩ /unban {user name} - Unban user
--------------Broadcast--------------
➩ /broadcast - Broadcast a message to all users
➩ /grp_broadcast - Broadcast a message to all connected groups
-------------------------------------------
/ads - IB
</blockquote></b>"""

    ADMIN_CMD_TXT = """<b><blockquote>
-------------User Premium------------
➩ /add_premium {user ID} {Times} - Add a premium user
➩ /remove_premium {user ID} - Remove a premium user
➩ /add_redeem - Generate a redeem code
➩ /premium_users - List all premium users
➩ /refresh - Refresh free trial for users
-------------Update Channel----------
➩ /set_muc {channel ID} - Set the movies update channel
--------------PM Search--------------
➩ /pm_search_on - Enable PM search
➩ /pm_search_off - Disable PM search
--------------Index File--------------
➩ /index - Index all files
--------------Leave Link--------------
➩ /leave {group ID} - Leave the specified group
--------------Broadcast--------------
➩ /broadcast - /grp_broadcast
--------------Set Ads----------------
➩ /set_ads {ads name}#{Times}#{photo URL} - <a href="https://t.me/Jisshu_developer/11">Explain</a>
➩ /del_ads - Delete ads
-------------Top Trending------------
➩ /setlist {Mirzapur, Money Heist} - <a href="https://t.me/Jisshu_developer/10">Explain</a>
➩ /clearlist - Clear all lists
</blockquote></b>"""

    GROUP_TEXT = """<b><blockquote>
 --------------Set Verify-------------
/set_verify {{website link}} {{website api}}
/set_verify_2 {{website link}} {{website api}}
/set_verify_3 {{website link}} {{website api}}
-------------Set Verify Time-----------
/set_time_2 {{seconds}} Sᴇᴛ ᴛʜᴇ sᴇᴄᴏɴᴅ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴛɪᴍᴇ
/set_time_3 {{seconds}} Sᴇᴛ ᴛʜᴇ ᴛʜɪʀᴅ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴛɪᴍᴇ
--------------Verify On Off------------
/verifyoff - off verification <a href="https://telegram.dog/JisshuDeveloperBot">Cᴏɴᴛᴀᴄᴛ</a> ᴛʜᴇ ʙᴏᴛ ᴀᴅᴍɪɴ ғᴏʀ ᴀ ᴠᴇʀɪғʏ.ᴏғғ
/verifyon - on verification 
------------Set File Caption-----------
/set_caption - set coustom file caption 
-----------Set Imdb Template-----------
/set_template - set IMDb template <a href="https://t.me/Jisshu_developer/8">Example</a>
--------------Set Tutorial-------------
/set_tutorial - set verification tutorial 
-------------Set Log Channel-----------
--> ᴀᴅᴅ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ʙʏ ᴛʜɪs ꜰᴏʀᴍᴀᴛ & ᴍᴀᴋᴇ sᴜʀᴇ ʙᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ʟᴏɢ ᴄʜᴀɴɴᴇʟ 👇

/set_log {{log channel id}}
---------------------------------------
ʏᴏᴜ ᴄᴀɴ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀʟʟ ᴅᴇᴛᴀɪʟs 
ʙʏ /details ᴄᴏᴍᴍᴀɴᴅ
</blockquote>
Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴀɴᴅ ᴜsᴇ ᴀʟʟ ғᴇᴀᴛᴜʀᴇs😇</b>"""

    ALLADMINCMD_TXT = """<b><blockquote expandable>
-------------User Premium------------
➩ /add_premium {user ID} {Times} - Add a premium user
➩ /remove_premium {user ID} - Remove a premium user
➩ /add_redeem - Generate a redeem code
➩ /premium_users - List all premium users
➩ /refresh - Refresh free trial for users
-------------Update Channel----------
➩ /set_muc {channel ID} - Set the movies update channel
--------------PM Search--------------
➩ /pm_search_on - Enable PM search
➩ /pm_search_off - Disable PM search
--------------Verify ID--------------
➩ /verifyon - on verification 
➩ /verifyoff - off verification only for group
--------------Set Ads----------------
➩ /set_ads {ads name}#{Times}#{photo URL} - <a href="https://t.me/Jisshu_developer/11">Explain</a>
➩ /del_ads - Delete ads
-------------Top Trending------------
➩ /setlist {Mirzapur, Money Heist} - <a href="https://t.me/Jisshu_developer/10">Explain</a>
➩ /clearlist - Clear all lists
--------------Index File--------------
➩ /index - Index all files
--------------Leave Link--------------
➩ /leave {group ID} - Leave the specified group
-------------Send Message-------------
➩ /send {user-name} - Use this command as a reply to any message
----------------Ban User---------------
➩ /ban {user-name} - Ban user 
➩ /unban {user-name} - Unban user
--------------Broadcast--------------
➩ /broadcast - Broadcast a message to all users
➩ /grp_broadcast - Broadcast a message to all connected groups
-------------------------------------------
/ads - to set advertisement
/reset_group - reset to default
/movie_update_off - update off
/movie_update_on - Movie Update on</blockquote></b>"""

    SOURCE_TXT = """<b>
ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ʜᴇʀᴇ ◉› :<blockquote><a href="https://t.me/JISSHU_BOTS/685">&lt;Click Here&gt;</a></blockquote>

ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : @jisshu_bots
</b>"""
    GROUP_C_TEXT = """<b><blockquote>
 --------------Set Verify-------------
/set_verify {website link} {website api}
/set_verify_2 {website link} {website api}
/set_verify_3 {website link} {website api}
-------------Set Verify Time-----------
/set_time_2 {seconds} Sᴇᴛ ᴛʜᴇ sᴇᴄᴏɴᴅ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴛɪᴍᴇ
/set_time_3 {seconds} Sᴇᴛ ᴛʜᴇ ᴛʜɪʀᴅ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴛɪᴍᴇ
--------------Verify On Off------------
/verifyoff {verify.off code} - off verification <a href="https://telegram.dog/JisshuDeveloperBot">Cᴏɴᴛᴀᴄᴛ</a> ᴛʜᴇ ʙᴏᴛ ᴀᴅᴍɪɴ ғᴏʀ ᴀ ᴠᴇʀɪғʏ.ᴏғғ ᴄᴏᴅᴇ
/verifyon - on verification 
------------Set File Caption-----------
/set_caption - set coustom file caption 
-----------Set Imdb Template-----------
/set_template - set IMDb template <a href="https://t.me/Jisshu_developer/8">Example</a>
--------------Set Tutorial-------------
/set_tutorial {tutorial link} - set 1 verification tutorial 
/set_tutorial_2 {tutorial link} - set 2 verification tutorial 
/set_tutorial_3 {tutorial link} - set 3 verification tutorial 
-------------Set Log Channel-----------
--> ᴀᴅᴅ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ʙʏ ᴛʜɪs ꜰᴏʀᴍᴀᴛ & ᴍᴀᴋᴇ sᴜʀᴇ ʙᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ʟᴏɢ ᴄʜᴀɴɴᴇʟ 👇

/set_log {log channel id}
---------------------------------------
ʏᴏᴜ ᴄᴀɴ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀʟʟ ᴅᴇᴛᴀɪʟs 
ʙʏ /details ᴄᴏᴍᴍᴀɴᴅ
</blockquote>
Iғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ᴅᴏᴜʙᴛs ᴘʟᴇᴀsᴇ <a href="https://telegram.dog/JisshuDeveloperBot">ᴄᴏɴᴛᴀᴄᴛ</a> ᴍʏ <a href="https://telegram.dog/im_jisshu">Z I Ƨ Ή Λ П ♡</a></b>"""
