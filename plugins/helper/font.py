from plugins.helper.fotnt_string import Fonts
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re

# Store last converted text per user
user_last_text = {}

class TextConverter:
    @staticmethod
    def to_upper(text):
        return text.upper()
    
    @staticmethod
    def to_lower(text):
        return text.lower()
    
    @staticmethod
    def to_title(text):
        return text.title()
    
    @staticmethod
    def to_sentence(text):
        sentences = re.split(r'([.!?]+)', text)
        result = []
        for i, sentence in enumerate(sentences):
            if i % 2 == 0 and sentence.strip():
                sentence = sentence.strip()
                if sentence:
                    sentence = sentence[0].upper() + sentence[1:].lower()
            result.append(sentence)
        return ''.join(result)
    
    @staticmethod
    def to_alternating(text):
        result = ""
        for i, char in enumerate(text):
            if char.isalpha():
                result += char.upper() if i % 2 == 0 else char.lower()
            else:
                result += char
        return result


@Client.on_message(filters.private & filters.command(["font"]))
async def style_buttons(c, m, cb=False):
    # Page 1 - Basic and Popular Styles
    style_buttons = [
        [
            InlineKeyboardButton("𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛", callback_data="style+typewriter"),
            InlineKeyboardButton("𝕆𝕦𝕥𝕝𝕚𝕟𝕖", callback_data="style+outline"),
        ],
        [
            InlineKeyboardButton("𝐒𝐞𝐫𝐢𝐟", callback_data="style+serif"),
            InlineKeyboardButton("𝑺𝒆𝒓𝒊𝒇", callback_data="style+bold_cool"),
        ],
        [
            InlineKeyboardButton("�S𝑒𝑟𝑖𝑓", callback_data="style+cool"),
            InlineKeyboardButton("Sᴍᴀʟʟ Cᴀᴘs", callback_data="style+small_cap"),
        ],
        [
            InlineKeyboardButton("𝓈𝒸𝓇𝒾𝓅𝓉", callback_data="style+script"),
            InlineKeyboardButton("𝓼𝓬𝓻𝓲𝓹𝓽", callback_data="style+script_bolt"),
        ],
        [
            InlineKeyboardButton("ᵗⁱⁿʸ", callback_data="style+tiny"),
            InlineKeyboardButton("ᑕOᗰIᑕ", callback_data="style+comic"),
        ],
        [
            InlineKeyboardButton("𝗦𝗮𝗻𝘀", callback_data="style+sans"),
            InlineKeyboardButton("𝙎𝙖𝙣𝙨", callback_data="style+slant_sans"),
        ],
        [
            InlineKeyboardButton("Next Page →", callback_data="page2"),
            InlineKeyboardButton("Case Options", callback_data="case_menu"),
        ]
    ]
    
    if not cb:
        if " " in m.text:
            title = m.text.split(" ", 1)[1]
            await m.reply_text(
                f"**Font Style Generator**\n\nOriginal: `{title}`\n\nChoose a style:",
                reply_markup=InlineKeyboardMarkup(style_buttons),
                reply_to_message_id=m.id,
            )
        else:
            await m.reply_text(
                "**Font Style Generator**\n\n"
                "Please provide text to style!\n"
                "Usage: `/font [your text]`\n\n"
                "Example: `/font Hello World`"
            )
    else:
        await m.answer()
        await m.message.edit_reply_markup(InlineKeyboardMarkup(style_buttons))


@Client.on_callback_query(filters.regex("^case_menu"))
async def case_menu(c, m):
    case_buttons = [
        [
            InlineKeyboardButton("UPPERCASE", callback_data="case+upper"),
            InlineKeyboardButton("lowercase", callback_data="case+lower"),
        ],
        [
            InlineKeyboardButton("Title Case", callback_data="case+title"),
            InlineKeyboardButton("Sentence case", callback_data="case+sentence"),
        ],
        [
            InlineKeyboardButton("aLtErNaTiNg", callback_data="case+alternating"),
        ],
        [
            InlineKeyboardButton("← Back", callback_data="page1"),
        ]
    ]
    
    await m.answer()
    await m.message.edit_text(
        f"**Case Conversion**\n\n"
        f"Original: `{m.message.reply_to_message.text.split(None, 1)[1]}`\n\n"
        f"Choose conversion:",
        reply_markup=InlineKeyboardMarkup(case_buttons)
    )


@Client.on_callback_query(filters.regex("^case"))
async def case_convert(c, m):
    await m.answer()
    cmd, case_type = m.data.split("+")
    
    r, oldtxt = m.message.reply_to_message.text.split(None, 1)
    
    if case_type == "upper":
        new_text = TextConverter.to_upper(oldtxt)
        case_name = "UPPERCASE"
    elif case_type == "lower":
        new_text = TextConverter.to_lower(oldtxt)
        case_name = "lowercase"
    elif case_type == "title":
        new_text = TextConverter.to_title(oldtxt)
        case_name = "Title Case"
    elif case_type == "sentence":
        new_text = TextConverter.to_sentence(oldtxt)
        case_name = "Sentence case"
    elif case_type == "alternating":
        new_text = TextConverter.to_alternating(oldtxt)
        case_name = "aLtErNaTiNg CaSe"
    
    user_last_text[m.from_user.id] = new_text
    
    copy_button = [
        [
            InlineKeyboardButton("Show Text", callback_data="copy_current"),
        ],
        [
            InlineKeyboardButton("More Cases", callback_data="case_menu"),
            InlineKeyboardButton("Font Styles", callback_data="page1"),
        ]
    ]
    
    try:
        await m.message.edit_text(
            f"**{case_name}**\n\n"
            f"Original: `{oldtxt}`\n"
            f"Result: `{new_text}`\n\n"
            f"Tap 'Show Text' to display for copying",
            reply_markup=InlineKeyboardMarkup(copy_button)
        )
    except Exception as e:
        print(f"Error in case conversion: {e}")


@Client.on_callback_query(filters.regex("^page2"))
async def page2(c, m):
    page2_buttons = [
        [
            InlineKeyboardButton("𝘚𝘢𝘯𝘀", callback_data="style+slant"),
            InlineKeyboardButton("𝖲𝖺𝗇𝗌", callback_data="style+sim"),
        ],
        [
            InlineKeyboardButton("Ⓒ︎Ⓘ︎Ⓡ︎Ⓒ︎Ⓛ︎Ⓔ︎Ⓢ︎", callback_data="style+circles"),
            InlineKeyboardButton("🅒︎🅘︎🅡︎🅒︎🅛︎🅔︎🅢︎", callback_data="style+circle_dark"),
        ],
        [
            InlineKeyboardButton("𝔊𝔬𝔱𝔥𝔦𝔠", callback_data="style+gothic"),
            InlineKeyboardButton("𝕲𝖔𝖙𝖍𝖎𝖈", callback_data="style+gothic_bolt"),
        ],
        [
            InlineKeyboardButton("C͜͡l͜͡o͜͡u͜͡d͜͡s͜͡", callback_data="style+cloud"),
            InlineKeyboardButton("H̆̈ă̈p̆̈p̆̈y̆̈", callback_data="style+happy"),
        ],
        [
            InlineKeyboardButton("S̑̈ȃ̈d̑̈", callback_data="style+sad"),
            InlineKeyboardButton("🇸 🇵 🇪 🇨 🇮 🇦 🇱", callback_data="style+special"),
        ],
        [
            InlineKeyboardButton("🅂🅀🅄🄰🅁🄴🅂", callback_data="style+squares"),
            InlineKeyboardButton("🆂︎🆀︎🆄︎🅰︎🆁︎🅴︎🆂︎", callback_data="style+squares_bold"),
        ],
        [
            InlineKeyboardButton("← Page 1", callback_data="page1"),
            InlineKeyboardButton("Next Page →", callback_data="page3"),
        ]
    ]
    
    await m.answer()
    await m.message.edit_text(
        f"**Font Styles - Page 2**\n\n"
        f"Original: `{m.message.reply_to_message.text.split(None, 1)[1]}`\n\n"
        f"Choose a style:",
        reply_markup=InlineKeyboardMarkup(page2_buttons)
    )


@Client.on_callback_query(filters.regex("^page3"))
async def page3(c, m):
    page3_buttons = [
        [
            InlineKeyboardButton("ꪖꪀᦔꪖꪶꪊᥴ𝓲ꪖ", callback_data="style+andalucia"),
            InlineKeyboardButton("爪卂几ᘜ卂", callback_data="style+manga"),
        ],
        [
            InlineKeyboardButton("S̾t̾i̾n̾k̾y̾", callback_data="style+stinky"),
            InlineKeyboardButton("B̥ͦu̥ͦb̥ͦb̥ͦl̥ͦe̥ͦs̥ͦ", callback_data="style+bubbles"),
        ],
        [
            InlineKeyboardButton("U͟n͟d͟e͟r͟l͟i͟n͟e͟", callback_data="style+underline"),
            InlineKeyboardButton("꒒ꍏꀷꌩꌃꀎꁅ", callback_data="style+ladybug"),
        ],
        [
            InlineKeyboardButton("R҉a҉y҉s҉", callback_data="style+rays"),
            InlineKeyboardButton("B҈i҈r҈d҈s҈", callback_data="style+birds"),
        ],
        [
            InlineKeyboardButton("S̸l̸a̸s̸h̸", callback_data="style+slash"),
            InlineKeyboardButton("s⃠t⃠o⃠p⃠", callback_data="style+stop"),
        ],
        [
            InlineKeyboardButton("S̺͆k̺͆y̺͆l̺͆i̺͆n̺͆e̺͆", callback_data="style+skyline"),
            InlineKeyboardButton("A͎r͎r͎o͎w͎s͎", callback_data="style+arrows"),
        ],
        [
            InlineKeyboardButton("ዪሀክቿነ", callback_data="style+qvnes"),
            InlineKeyboardButton("S̶t̶r̶i̶k̶e̶", callback_data="style+strike"),
        ],
        [
            InlineKeyboardButton("F༙r༙o༙z༙e༙n༙", callback_data="style+frozen"),
        ],
        [
            InlineKeyboardButton("← Page 2", callback_data="page2"),
            InlineKeyboardButton("Case Options", callback_data="case_menu"),
        ]
    ]
    
    await m.answer()
    await m.message.edit_text(
        f"**Font Styles - Page 3**\n\n"
        f"Original: `{m.message.reply_to_message.text.split(None, 1)[1]}`\n\n"
        f"Choose a style:",
        reply_markup=InlineKeyboardMarkup(page3_buttons)
    )


@Client.on_callback_query(filters.regex("^page1"))
async def page1(c, m):
    await style_buttons(c, m, cb=True)


@Client.on_callback_query(filters.regex("^back_to_main"))
async def back_to_main(c, m):
    await style_buttons(c, m, cb=True)


@Client.on_callback_query(filters.regex("^style"))
async def style(c, m):
    await m.answer()
    cmd, style = m.data.split("+")

    style_mapping = {
        "typewriter": Fonts.typewriter,
        "outline": Fonts.outline,
        "serif": Fonts.serief,
        "bold_cool": Fonts.bold_cool,
        "cool": Fonts.cool,
        "small_cap": Fonts.smallcap,
        "script": Fonts.script,
        "script_bolt": Fonts.bold_script,
        "tiny": Fonts.tiny,
        "comic": Fonts.comic,
        "sans": Fonts.san,
        "slant_sans": Fonts.slant_san,
        "slant": Fonts.slant,
        "sim": Fonts.sim,
        "circles": Fonts.circles,
        "circle_dark": Fonts.dark_circle,
        "gothic": Fonts.gothic,
        "gothic_bolt": Fonts.bold_gothic,
        "cloud": Fonts.cloud,
        "happy": Fonts.happy,
        "sad": Fonts.sad,
        "special": Fonts.special,
        "squares": Fonts.square,
        "squares_bold": Fonts.dark_square,
        "andalucia": Fonts.andalucia,
        "manga": Fonts.manga,
        "stinky": Fonts.stinky,
        "bubbles": Fonts.bubbles,
        "underline": Fonts.underline,
        "ladybug": Fonts.ladybug,
        "rays": Fonts.rays,
        "birds": Fonts.birds,
        "slash": Fonts.slash,
        "stop": Fonts.stop,
        "skyline": Fonts.skyline,
        "arrows": Fonts.arrows,
        "qvnes": Fonts.rvnes,
        "strike": Fonts.strike,
        "frozen": Fonts.frozen
    }

    cls = style_mapping.get(style)
    if not cls:
        await m.answer("Style not found!", show_alert=True)
        return

    r, oldtxt = m.message.reply_to_message.text.split(None, 1)
    new_text = cls(oldtxt)
    
    user_last_text[m.from_user.id] = new_text
    
    # Simple result buttons
    result_buttons = [
        [
            InlineKeyboardButton("Show Text", callback_data="copy_current"),
        ],
        [
            InlineKeyboardButton("Try Another", callback_data="page1"),
            InlineKeyboardButton("More Styles", callback_data="page2"),
        ],
        [
            InlineKeyboardButton("Case Options", callback_data="case_menu"),
        ]
    ]
    
    # Get clean style name
    style_names = {
        "typewriter": "Typewriter",
        "outline": "Outline", 
        "serif": "Serif",
        "bold_cool": "Bold Serif",
        "cool": "Cool Serif",
        "small_cap": "Small Caps",
        "script": "Script",
        "script_bolt": "Bold Script",
        "tiny": "Tiny",
        "comic": "Comic",
        "sans": "Sans",
        "slant_sans": "Slant Sans",
        "slant": "Slant",
        "sim": "Sim Sans",
        "circles": "Circles",
        "circle_dark": "Dark Circles",
        "gothic": "Gothic",
        "gothic_bolt": "Bold Gothic",
        "cloud": "Clouds",
        "happy": "Happy",
        "sad": "Sad"
    }
    
    style_display = style_names.get(style, style.replace("_", " ").title())
    
    try:
        await m.message.edit_text(
            f"**{style_display} Style**\n\n"
            f"Original: `{oldtxt}`\n"
            f"Result: `{new_text}`\n\n"
            f"Tap 'Show Text' to display for copying",
            reply_markup=InlineKeyboardMarkup(result_buttons)
        )
    except Exception as e:
        print(f"Error in style conversion: {e}")


@Client.on_callback_query(filters.regex("^copy"))
async def copy_text(c, m):
    user_id = m.from_user.id
    
    if m.data == "copy_current":
        if user_id in user_last_text:
            text_to_copy = user_last_text[user_id]
            
            # Create back button
            back_button = [
                [InlineKeyboardButton("← Back", callback_data="page1")]
            ]
            
            # Show the text in a copyable format
            await m.message.edit_text(
                f"**Copy this text:**\n\n"
                f"`{text_to_copy}`\n\n"
                f"**Instructions:**\n"
                f"1. Tap and hold the text above\n"
                f"2. Select 'Copy' from the menu\n"
                f"3. Paste wherever you want to use it",
                reply_markup=InlineKeyboardMarkup(back_button)
            )
            
            # Also send as a separate message for easier copying
            await m.message.reply_text(
                f"{text_to_copy}",
                quote=False
            )
            
            await m.answer("Text displayed for copying!")
        else:
            await m.answer("No text found to copy!", show_alert=True)
    else:
        await m.answer("Invalid copy request!", show_alert=True)