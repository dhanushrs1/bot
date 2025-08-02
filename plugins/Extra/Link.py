import asyncio
import secrets
import re
import os
import time
import json
import aiohttp
from datetime import datetime
from typing import Optional, Dict, Any
from pyrogram import Client, filters, ContinuePropagation
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from info import ADMINS, REDIRECT_CHANNEL, OMDB_API_KEY, DATABASE_URI
from utils import list_to_str
from database.ia_filterdb import get_search_results
from plugins.pm_filter import auto_filter

# MongoDB Configuration
MONGO_DB_NAME = "PermanentLinksDB"
LINKS_COLLECTION = "query_links"

# MongoDB Client
mongo_client = AsyncIOMotorClient(DATABASE_URI)
db = mongo_client[MONGO_DB_NAME]
links_collection = db[LINKS_COLLECTION]

# Configuration
IMDB_API_URL = "https://imdbapi-beige.vercel.app/" 
REDIRECT_URL = "https://files.hdcinema.fun/"
LINK_ID_PREFIX = "hdcnm_"

# UI Configuration
QUALITY_OPTIONS = [
    {"name": "4K UHD", "priority": 1},
    {"name": "BluRay", "priority": 2},
    {"name": "WebDL", "priority": 3},
    {"name": "WEBRip", "priority": 4},
    {"name": "HDRip", "priority": 5},
    {"name": "DVDRip", "priority": 6}
]

# Global Cache
PREVIEW_CACHE = {}
ADMIN_STATES = {}

# MongoDB Helper Functions
class LinkDatabase:
    @staticmethod
    async def create_indexes():
        """Create database indexes for better performance."""
        try:
            await links_collection.create_index("link_id", unique=True)
            await links_collection.create_index("created_at")
            await links_collection.create_index("admin_id")
            print("MongoDB indexes created successfully")
        except Exception as e:
            print(f"Index creation warning: {e}")

    @staticmethod
    async def save_link(link_data: Dict[str, Any]) -> bool:
        """Save permanent link to MongoDB."""
        try:
            link_data["created_at"] = datetime.utcnow()
            await links_collection.insert_one(link_data)
            return True
        except DuplicateKeyError:
            print(f"Duplicate link_id: {link_data.get('link_id')}")
            return False
        except Exception as e:
            print(f"Error saving link: {e}")
            return False

    @staticmethod
    async def get_link(link_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve link data from MongoDB."""
        try:
            result = await links_collection.find_one({"link_id": link_id})
            return result
        except Exception as e:
            print(f"Error retrieving link: {e}")
            return None

    @staticmethod
    async def update_link(link_id: str, update_data: Dict[str, Any]) -> bool:
        """Update existing link data."""
        try:
            update_data["updated_at"] = datetime.utcnow()
            result = await links_collection.update_one(
                {"link_id": link_id}, 
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating link: {e}")
            return False

    @staticmethod
    async def get_stats() -> Dict[str, Any]:
        """Get database statistics."""
        try:
            total_links = await links_collection.count_documents({})
            today = datetime.utcnow().date()
            today_links = await links_collection.count_documents({
                "created_at": {"$gte": datetime.combine(today, datetime.min.time())}
            })
            
            return {
                "total_links": total_links,
                "today_links": today_links,
                "database_status": "Connected"
            }
        except Exception as e:
            return {
                "total_links": 0,
                "today_links": 0,
                "database_status": f"Error: {e}"
            }

# UI Manager
class UIManager:
    @staticmethod
    def create_movie_caption(**kwargs) -> str:
        """Generate movie caption."""
        title = kwargs.get("title", "Unknown Title")
        year = kwargs.get("year", "N/A")
        genre = kwargs.get("genres", "N/A")
        rating = kwargs.get("rating", "N/A")
        runtime = kwargs.get("runtime", "N/A")
        language = kwargs.get("language", "N/A")
        quality = kwargs.get("quality", "")

        # Title with proper spacing
        caption_parts = [f"🎬 **{title}**", ""]
        
        # Movie details with emojis
        if year != "N/A":
            caption_parts.append(f"📅 **Year:** {year}")
        if language != "N/A":
            caption_parts.append(f"🌍 **Language:** {language}")
        if rating not in ["N/A", "0", None]:
            caption_parts.append(f"⭐ **Rating:** {rating}/10")
        if runtime != "N/A":
            caption_parts.append(f"⏱️ **Runtime:** {runtime}")
        if genre != "N/A":
            caption_parts.append(f"🎭 **Genre:** {genre}")
        if quality:
            caption_parts.append(f"📺 **Quality:** {quality}")
        
        caption_parts.extend(["", "📂 **Click below to access files**"])
        
        return "\n".join(caption_parts)

    @staticmethod
    def create_preview_keyboard(preview_id: str) -> InlineKeyboardMarkup:
        """Create modern preview keyboard."""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("✓ Confirm & Post", callback_data=f"confirm#{preview_id}")],
            [
                InlineKeyboardButton("📸 Edit Poster", callback_data=f"edit#poster#{preview_id}"),
                InlineKeyboardButton("📝 Edit Details", callback_data=f"edit#details#{preview_id}")
            ],
            [
                InlineKeyboardButton("🌐 Language", callback_data=f"edit#language#{preview_id}"),
                InlineKeyboardButton("🎬 Quality", callback_data=f"edit#quality#{preview_id}")
            ],
            [
                InlineKeyboardButton("✏️ Custom Caption", callback_data=f"edit#caption#{preview_id}"),
                InlineKeyboardButton("✗ Cancel", callback_data=f"cancel#{preview_id}")
            ]
        ])

    @staticmethod
    def create_quality_keyboard(preview_id: str) -> InlineKeyboardMarkup:
        """Create quality selection keyboard."""
        buttons = []
        qualities = sorted(QUALITY_OPTIONS, key=lambda x: x["priority"])
        
        for i in range(0, len(qualities), 2):
            row = []
            for j in range(2):
                if i + j < len(qualities):
                    quality = qualities[i + j]
                    row.append(InlineKeyboardButton(
                        quality['name'], 
                        callback_data=f"quality#{preview_id}#{quality['name']}"
                    ))
            buttons.append(row)
        
        buttons.append([InlineKeyboardButton("← Back", callback_data=f"back#{preview_id}")])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def create_final_keyboard(link: str) -> InlineKeyboardMarkup:
        """Create final download button."""
        return InlineKeyboardMarkup([[
            InlineKeyboardButton("🎬 Get Movie Files", url=link)
        ]])

# API Functions
async def fetch_movie_data(query: str) -> Optional[Dict[str, Any]]:
    """Fetch movie data from API."""
    if not IMDB_API_URL:
        return None
        
    try:
        timeout = aiohttp.ClientTimeout(total=8)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{IMDB_API_URL}search", params={'query': query}) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                return None
    except Exception as e:
        print(f"API Error: {e}")
        return None

def process_languages(language_input: str) -> str:
    """Process and format language strings."""
    if not language_input or language_input == "N/A":
        return "N/A"
    
    if isinstance(language_input, list):
        return " + ".join(language_input)
    
    languages = re.split(r'[,|+&]', str(language_input))
    languages = [lang.strip().title() for lang in languages if lang.strip()]
    
    return " + ".join(languages) if languages else "N/A"

async def validate_image_url(url: str) -> bool:
    """Validate image URL accessibility."""
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.head(url) as response:
                content_type = response.headers.get('content-type', '').lower()
                return response.status == 200 and content_type.startswith('image/')
    except:
        return False

# Main Commands
@Client.on_message(filters.command("createlink") & filters.user(ADMINS))
async def create_permanent_link(client, message):
    """Create permanent link command."""
    if len(message.command) < 2:
        usage_msg = "**Usage Instructions**\n\nCommand: `/createlink <movie name>`\n\nExample: `/createlink Avengers Endgame 2019`"
        return await message.reply(usage_msg)

    search_query = message.text.split(" ", 1)[1].strip()
    progress_msg = await message.reply(f"Searching for: **{search_query}**")
    
    try:
        # Check database for files
        files, _, _ = await get_search_results(search_query, max_results=1)
        if not files:
            return await progress_msg.edit_text(f"No files found for: **{search_query}**")

        # Fetch movie data
        await progress_msg.edit_text("Fetching movie information...")
        movie_data = await fetch_movie_data(search_query) or {}
        
        # Generate unique link
        await progress_msg.edit_text("Creating permanent link...")
        unique_id = secrets.token_hex(6)
        link_id = f"{LINK_ID_PREFIX}{unique_id}"
        
        # Prepare link data for MongoDB
        link_data = {
            "link_id": link_id,
            "search_query": search_query,
            "admin_id": message.from_user.id,
            "movie_data": movie_data,
            "status": "active"
        }
        
        # Save to MongoDB
        if not await LinkDatabase.save_link(link_data):
            return await progress_msg.edit_text("Failed to save link to database")
        
        permanent_link = f"{REDIRECT_URL}?id={link_id}"
        
        # Prepare preview data
        movie_data.setdefault("title", search_query.title())
        movie_data.setdefault("language", "N/A")
        movie_data["language"] = process_languages(movie_data.get("language", "N/A"))
        
        caption = UIManager.create_movie_caption(**movie_data)
        
        preview_id = secrets.token_hex(8)
        PREVIEW_CACHE[preview_id] = {
            "link_id": link_id,
            "poster": movie_data.get("poster"),
            "caption": caption,
            "permanent_link": permanent_link,
            "admin_id": message.from_user.id,
            "movie_data": movie_data,
            "search_query": search_query,
            "created_at": time.time()
        }
        
        await progress_msg.delete()
        await send_preview(client, message.from_user.id, preview_id)
        
    except Exception as e:
        await progress_msg.edit_text(f"System Error: {str(e)}")

async def send_preview(client, user_id: int, preview_id: str, delete_previous: bool = False):
    """Send preview message."""
    preview_data = PREVIEW_CACHE.get(preview_id)
    if not preview_data:
        return

    # Delete previous message if exists
    if delete_previous and "message_id" in preview_data:
        try:
            await client.delete_messages(user_id, preview_data["message_id"])
        except:
            pass

    preview_caption = f"👁️ **PREVIEW MODE**\n\n{preview_data['caption']}"
    preview_info = f"\n\n📊 **Link Info:**\n🔍 Query: `{preview_data['search_query']}`\n🔗 ID: `{preview_data['link_id']}`"
    
    full_caption = preview_caption + preview_info
    keyboard = UIManager.create_preview_keyboard(preview_id)

    try:
        poster = preview_data.get("poster")
        if poster and await validate_image_url(poster):
            sent_message = await client.send_photo(
                user_id, photo=poster, caption=full_caption, reply_markup=keyboard
            )
        else:
            sent_message = await client.send_message(
                user_id, text=full_caption, reply_markup=keyboard, disable_web_page_preview=True
            )
        
        preview_data["message_id"] = sent_message.id
        
    except Exception as e:
        await client.send_message(
            user_id, 
            text=f"⚠️ **Preview Error**\n\n{full_caption}",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

# Callback Handlers
@Client.on_callback_query(filters.regex(r"^(confirm|cancel)#"))
async def handle_confirm_cancel(client, query):
    """Handle confirm and cancel actions."""
    if query.from_user.id not in ADMINS:
        return await query.answer("Unauthorized", show_alert=True)
    
    try:
        action, preview_id = query.data.split("#")
        preview_data = PREVIEW_CACHE.get(preview_id)
        
        if not preview_data or preview_data["admin_id"] != query.from_user.id:
            return await query.answer("Preview expired", show_alert=True)

        if action == "confirm":
            # Post to channel
            is_photo = bool(query.message.photo)
            edit_func = query.message.edit_caption if is_photo else query.message.edit_text
            
            await edit_func("Publishing to channel...")
            
            try:
                final_keyboard = UIManager.create_final_keyboard(preview_data["permanent_link"])
                poster = preview_data.get("poster")
                
                if poster and await validate_image_url(poster):
                    sent_message = await client.send_photo(
                        REDIRECT_CHANNEL, 
                        photo=poster, 
                        caption=preview_data["caption"], 
                        reply_markup=final_keyboard
                    )
                else:
                    sent_message = await client.send_message(
                        REDIRECT_CHANNEL, 
                        text=preview_data["caption"], 
                        reply_markup=final_keyboard, 
                        disable_web_page_preview=True
                    )
                
                # Update link in database
                await LinkDatabase.update_link(preview_data["link_id"], {
                    "channel_message_id": sent_message.id,
                    "channel_post_link": sent_message.link,
                    "status": "published"
                })
                
                success_msg = f"✅ **Published Successfully!**\n\n🔗 [View Post]({sent_message.link})\n📱 Message ID: `{sent_message.id}`"
                await edit_func(success_msg)
                
            except Exception as e:
                await edit_func(f"Publishing Failed: {str(e)}")
            finally:
                if preview_id in PREVIEW_CACHE:
                    del PREVIEW_CACHE[preview_id]
                    
        elif action == "cancel":
            if preview_id in PREVIEW_CACHE:
                del PREVIEW_CACHE[preview_id]
            await query.message.delete()
            await query.answer("Preview cancelled", show_alert=True)
            
    except Exception as e:
        await query.answer(f"Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex(r"^quality#"))
async def handle_quality_selection(client, query):
    """Handle quality selection."""
    if query.from_user.id not in ADMINS:
        return await query.answer("Unauthorized", show_alert=True)
    
    try:
        _, preview_id, quality = query.data.split("#")
        preview_data = PREVIEW_CACHE.get(preview_id)
        
        if not preview_data:
            return await query.answer("Preview expired", show_alert=True)
        
        preview_data["movie_data"]["quality"] = quality
        preview_data["caption"] = UIManager.create_movie_caption(**preview_data["movie_data"])
        
        await query.answer(f"Quality set to: {quality}", show_alert=True)
        await send_preview(client, query.from_user.id, preview_id, delete_previous=True)
        
    except Exception as e:
        await query.answer(f"Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex(r"^back#"))
async def handle_back_button(client, query):
    """Handle back button."""
    if query.from_user.id not in ADMINS:
        return await query.answer("Unauthorized", show_alert=True)
    
    try:
        _, preview_id = query.data.split("#")
        await send_preview(client, query.from_user.id, preview_id, delete_previous=True)
    except Exception as e:
        await query.answer(f"Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex(r"^edit#"))
async def handle_edit_request(client, query):
    """Handle edit requests."""
    if query.from_user.id not in ADMINS:
        return await query.answer("Unauthorized", show_alert=True)
    
    try:
        _, edit_type, preview_id = query.data.split("#")
        
        if preview_id not in PREVIEW_CACHE:
            return await query.answer("Preview expired", show_alert=True)
        
        if edit_type == "quality":
            keyboard = UIManager.create_quality_keyboard(preview_id)
            is_photo = bool(query.message.photo)
            edit_func = query.message.edit_caption if is_photo else query.message.edit_text
            
            await edit_func("Select Quality\n\nChoose quality for this movie:", reply_markup=keyboard)
            return
        
        # Store edit state
        ADMIN_STATES[query.from_user.id] = {
            "type": edit_type,
            "preview_id": preview_id,
            "started_at": time.time()
        }
        
        prompts = {
            "poster": "**Send new poster URL**\n*Must start with http:// or https://*",
            "details": "**Send details in format:**\n`Title | Year | Rating | Genre | Runtime`",
            "language": "**Send languages:**\n*Examples: English, Hindi + Tamil, English + French*",
            "caption": "**Send complete new caption**"
        }
        
        await query.message.reply_text(f"**Edit {edit_type.title()}**\n\n{prompts.get(edit_type, 'Send your input:')}")
        await query.answer(f"Edit mode: {edit_type}")
        
    except Exception as e:
        await query.answer(f"Error: {str(e)}", show_alert=True)

# Admin Input Handler
def admin_input_filter(_, __, message):
    """Filter for admin input during edit mode."""
    if not (message.from_user and message.from_user.id in ADMINS):
        return False
    
    admin_id = message.from_user.id
    if admin_id not in ADMIN_STATES:
        return False
    
    # Check timeout (5 minutes)
    if time.time() - ADMIN_STATES[admin_id].get("started_at", 0) > 300:
        del ADMIN_STATES[admin_id]
        return False
    
    return not message.text.startswith('/')

@Client.on_message(filters.private & filters.text & filters.create(admin_input_filter))
async def handle_admin_input(client, message: Message):
    """Handle admin input for editing."""
    admin_id = message.from_user.id
    state = ADMIN_STATES[admin_id]
    preview_id = state["preview_id"]
    edit_type = state["type"]
    
    if preview_id not in PREVIEW_CACHE:
        del ADMIN_STATES[admin_id]
        return await message.reply("**Session Expired**\n\nPreview data expired. Create new link.")
    
    preview_data = PREVIEW_CACHE[preview_id]
    user_input = message.text.strip()
    
    try:
        if edit_type == "poster":
            if user_input.startswith(("http://", "https://")):
                if await validate_image_url(user_input):
                    preview_data["poster"] = user_input
                    await message.reply("**Poster Updated!**")
                else:
                    return await message.reply("**Invalid URL**\n\nURL is not accessible or not an image")
            else:
                return await message.reply("**Invalid Format**\n\nURL must start with http:// or https://")
                
        elif edit_type == "language":
            processed_language = process_languages(user_input)
            preview_data["movie_data"]["language"] = processed_language
            preview_data["caption"] = UIManager.create_movie_caption(**preview_data["movie_data"])
            await message.reply(f"**Language Updated!**\n\nSet to: **{processed_language}**")
            
        elif edit_type == "caption":
            if len(user_input) < 10:
                return await message.reply("**Too Short**\n\nCaption must be at least 10 characters")
            preview_data["caption"] = user_input
            await message.reply("**Caption Updated!**")
            
        elif edit_type == "details":
            parts = [p.strip() for p in user_input.split("|")]
            if len(parts) != 5:
                return await message.reply("**Invalid Format**\n\nUse: Title | Year | Rating | Genre | Runtime")
            
            preview_data["movie_data"].update({
                "title": parts[0] or "Unknown Title",
                "year": parts[1] or "N/A",
                "rating": parts[2] or "N/A",
                "genres": parts[3] or "N/A",
                "runtime": parts[4] or "N/A"
            })
            
            preview_data["caption"] = UIManager.create_movie_caption(**preview_data["movie_data"])
            await message.reply("**Details Updated!**")

        # Clean up and refresh preview
        del ADMIN_STATES[admin_id]
        update_msg = await message.reply("Updating...")
        await send_preview(client, admin_id, preview_id, delete_previous=True)
        await update_msg.delete()
        
    except Exception as e:
        await message.reply(f"**Update Failed**\n\n{str(e)}")

# Link Handler
@Client.on_message(filters.command("start"), group=1)
async def handle_permanent_link(client, message):
    """Handle permanent link access."""
    if len(message.command) > 1 and message.command[1].startswith(LINK_ID_PREFIX):
        link_id = message.command[1]
        
        processing_msg = await message.reply("Processing...")
        
        try:
            link_data = await LinkDatabase.get_link(link_id)
            if link_data:
                search_query = link_data.get("search_query")
                if search_query:
                    mock_message = message
                    mock_message.text = search_query
                    
                    await processing_msg.delete()
                    await auto_filter(client, mock_message)
                    return
            
            await processing_msg.edit_text("**Invalid Link**\n\nLink has expired or is invalid")
            
        except Exception as e:
            await processing_msg.edit_text("**Access Error**\n\nFailed to access files")
        return
    
    raise ContinuePropagation

# Admin Commands
@Client.on_message(filters.command("linkstats") & filters.user(ADMINS))
async def show_link_stats(client, message):
    """Show link statistics."""
    try:
        stats = await LinkDatabase.get_stats()
        
        stats_msg = f"""📊 **Link System Status**

**Database Statistics:**
• Total Links: `{stats['total_links']}`
• Today's Links: `{stats['today_links']}`
• Database: {stats['database_status']}

**Current Session:**
• Active Previews: `{len(PREVIEW_CACHE)}`
• Edit Sessions: `{len(ADMIN_STATES)}`
• API Endpoint: {'✅ Configured' if IMDB_API_URL else '❌ Missing'}
        """
        
        await message.reply(stats_msg.strip())
        
    except Exception as e:
        await message.reply(f"❌ **Stats Error**\n\n{str(e)}")

@Client.on_message(filters.command("searchlinks") & filters.user(ADMINS))
async def search_links(client, message):
    """Search for specific links in database."""
    if len(message.command) < 2:
        return await message.reply("""🔍 **Search Links**

**Usage:** `/searchlinks <search term>`

**Examples:**
• `/searchlinks avengers`
• `/searchlinks 2023`
• `/searchlinks hdcnm_abc123`""")
    
    search_term = message.text.split(" ", 1)[1].strip()
    
    try:
        # Search in database
        query = {
            "$or": [
                {"search_query": {"$regex": search_term, "$options": "i"}},
                {"link_id": {"$regex": search_term, "$options": "i"}},
                {"movie_data.title": {"$regex": search_term, "$options": "i"}}
            ]
        }
        
        cursor = links_collection.find(query).limit(10)
        results = await cursor.to_list(length=10)
        
        if not results:
            return await message.reply(f"🔍 **No Results**\n\nNo links found for: **{search_term}**")
        
        # Format results
        results_text = f"🔍 **Search Results for:** `{search_term}`\n\n"
        
        for i, link in enumerate(results, 1):
            title = link.get('movie_data', {}).get('title', link.get('search_query', 'Unknown'))
            link_id = link.get('link_id', 'N/A')
            status = link.get('status', 'unknown')
            created = link.get('created_at', datetime.utcnow())
            channel_link = link.get('channel_post_link', 'N/A')
            
            if isinstance(created, str):
                created = datetime.fromisoformat(created)
            
            results_text += f"**{i}.** {title}\n"
            results_text += f"   🔗 `{link_id}`\n"
            results_text += f"   📅 {created.strftime('%Y-%m-%d')}\n"
            results_text += f"   📊 Status: {status}\n"
            if channel_link != 'N/A':
                results_text += f"   📺 [View Post]({channel_link})\n"
            results_text += "\n"
        
        if len(results) == 10:
            results_text += "⚠️ *Showing first 10 results only*"
        
        await message.reply(results_text)
        
    except Exception as e:
        await message.reply(f"❌ **Search Failed**\n\n{str(e)}")

@Client.on_message(filters.command("linkhelp") & filters.user(ADMINS))
async def show_link_help(client, message):
    """Show comprehensive help for link system."""
    help_text = f"""🎬 **Permanent Link System**

**📋 Core Commands:**
• `/createlink <movie>` - Create new permanent link
• `/linkstats` - Show system statistics
• `/searchlinks <term>` - Search existing links
• `/linkhelp` - Show this help

**🔗 Link Format:**
• **Prefix:** `{LINK_ID_PREFIX}`
• **URL:** `{REDIRECT_URL}?id=<link_id>`
    """
    
    await message.reply(help_text)

# Automatic Cleanup Task
async def periodic_cleanup():
    """Periodic cleanup of expired data."""
    while True:
        try:
            await asyncio.sleep(1800)  # 30 minutes
            
            current_time = time.time()
            
            # Clean expired previews (1 hour old)
            expired_previews = [
                pid for pid, data in PREVIEW_CACHE.items()
                if current_time - data.get("created_at", 0) > 3600
            ]
            
            for pid in expired_previews:
                del PREVIEW_CACHE[pid]
            
            # Clean expired admin states (10 minutes)
            expired_states = [
                aid for aid, state in ADMIN_STATES.items()
                if current_time - state.get("started_at", 0) > 600
            ]
            
            for aid in expired_states:
                del ADMIN_STATES[aid]
            
            if expired_previews or expired_states:
                print(f"Periodic cleanup: {len(expired_previews)} previews, {len(expired_states)} states")
                
        except Exception as e:
            print(f"Cleanup error: {e}")

# Database Initialization
async def initialize_database():
    """Initialize MongoDB database and indexes."""
    try:
        await LinkDatabase.create_indexes()
        
        # Test connection
        await db.command("ping")
        print("MongoDB connection successful")
        
        # Get initial stats
        stats = await LinkDatabase.get_stats()
        print(f"Database initialized - Total links: {stats['total_links']}")
        
    except Exception as e:
        print(f"MongoDB initialization failed: {e}")
        print("Bot will continue but permanent links may not work")

# Startup Tasks
print(f"Link Prefix: {LINK_ID_PREFIX}")
print(f"Redirect URL: {REDIRECT_URL}")
print(f"Database: MongoDB ({MONGO_DB_NAME})")
asyncio.create_task(initialize_database())
asyncio.create_task(periodic_cleanup())