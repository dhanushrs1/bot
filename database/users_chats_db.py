import datetime
import pytz
from motor.motor_asyncio import AsyncIOMotorClient

# from info import SETTINGS, IS_PM_SEARCH, IS_SEND_MOVIE_UPDATE, PREMIUM_POINT,REF_PREMIUM,IS_VERIFY, SHORTENER_WEBSITE3, SHORTENER_API3, THREE_VERIFY_GAP, LINK_MODE, FILE_CAPTION, TUTORIAL, DATABASE_NAME, DATABASE_URI, IMDB, IMDB_TEMPLATE, PROTECT_CONTENT, AUTO_DELETE, SPELL_CHECK, AUTO_FILTER, LOG_VR_CHANNEL, SHORTENER_WEBSITE, SHORTENER_API, SHORTENER_WEBSITE2, SHORTENER_API2, TWO_VERIFY_GAP
# from utils import get_seconds
from info import *

client = AsyncIOMotorClient(DATABASE_URI)
mydb = client[DATABASE_NAME]


class Database:
    def __init__(self):
        self.col = mydb.users
        self.grp = mydb.groups
        self.misc = mydb.misc
        self.verify_id = mydb.verify_id
        self.users = mydb.uersz
        self.req = mydb.requests
        self.mGrp = mydb.mGrp
        self.pmMode = mydb.pmMode
        self.jisshu_ads_link = mydb.jisshu_ads_link
        self.movies_update_channel = mydb.movies_update_channel
        self.botcol = mydb.botcol

    default = {
        "spell_check": SPELL_CHECK,
        "auto_filter": AUTO_FILTER,
        "file_secure": PROTECT_CONTENT,
        "auto_delete": AUTO_DELETE,
        "template": IMDB_TEMPLATE,
        "caption": FILE_CAPTION,
        "tutorial": TUTORIAL,
        "tutorial_2": TUTORIAL_2,
        "tutorial_3": TUTORIAL_3,
        "shortner": SHORTENER_WEBSITE,
        "api": SHORTENER_API,
        "shortner_two": SHORTENER_WEBSITE2,
        "api_two": SHORTENER_API2,
        "log": LOG_VR_CHANNEL,
        "imdb": IMDB,
        "fsub_id": AUTH_CHANNEL,
        "link": LINK_MODE,
        "is_verify": IS_VERIFY,
        "verify_time": TWO_VERIFY_GAP,
        "shortner_three": SHORTENER_WEBSITE3,
        "api_three": SHORTENER_API3,
        "third_verify_time": THREE_VERIFY_GAP,
        "stream_mode_user": STREAM_MODE_USER,
    }

    def new_user(self, id, name):
        return dict(
            id=id,
            name=name,
            join_date=datetime.now(),
            point=0,
            ban_status=dict(is_banned=False, ban_reason="")
        )

    async def get_settings(self, group_id):
        chat = await self.grp.find_one({"id": int(group_id)})
        if chat and "settings" in chat:
            return chat["settings"]
        else:
            return self.default.copy()

    async def find_join_req(self, id):
        return bool(await self.req.find_one({"id": id}))

    async def add_join_req(self, id):
        await self.req.insert_one({"id": id})

    async def del_join_req(self):
        await self.req.drop()

    def new_group(self, id, title):
        return dict(
            id=id,
            title=title,
            join_date=datetime.now(),
            chat_status=dict(is_disabled=False, reason="")
        )

    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)

    async def update_point(self, id):
        await self.col.update_one({"id": id}, {"$inc": {"point": 100}})
        point = (await self.col.find_one({"id": id}))["point"]
        if point >= PREMIUM_POINT:
            seconds = REF_PREMIUM * 24 * 60 * 60
            oldEx = await self.users.find_one({"id": id})
            if oldEx:
                expiry_time = oldEx["expiry_time"] + datetime.timedelta(seconds=seconds)
            else:
                expiry_time = datetime.datetime.now() + datetime.timedelta(
                    seconds=seconds
                )
            user_data = {"id": id, "expiry_time": expiry_time}
            await db.update_user(user_data)
            await self.col.update_one({"id": id}, {"$set": {"point": 0}})

    async def get_point(self, id):
        newPoint = await self.col.find_one({"id": id})
        return newPoint["point"] if newPoint else None

    async def is_user_exist(self, id):
        user = await self.col.find_one({"id": int(id)})
        return bool(user)

    async def total_users_count(self):
        """Returns the total number of users in the database."""
        count = await self.col.count_documents({})
        return count

    async def get_users_slice(self, start, limit):
        """Fetches a slice of users for pagination using an asynchronous cursor."""
        cursor = self.col.find({}, {"_id": 0, "id": 1, "name": 1}).skip(start).limit(limit)
        # Convert the async cursor to a list
        users_list = await cursor.to_list(length=limit)
        return users_list

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({"id": int(user_id)})

    async def delete_chat(self, id):
        await self.grp.delete_many({"id": int(id)})

    async def get_banned(self):
        users = self.col.find({"ban_status.is_banned": True})
        chats = self.grp.find({"chat_status.is_disabled": True})
        b_chats = [chat["id"] async for chat in chats]
        b_users = [user["id"] async for user in users]
        return b_users, b_chats

    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)

    async def get_chat(self, chat):
        chat = await self.grp.find_one({"id": int(chat)})
        return False if not chat else chat.get("chat_status")

    async def update_settings(self, id, settings):
        await self.grp.update_one({"id": int(id)}, {"$set": {"settings": settings}})

    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count

    async def get_all_chats(self):
        return self.grp.find({})

    async def get_db_size(self):
        return (await mydb.command("dbstats"))["dataSize"]

    async def get_notcopy_user(self, user_id):
        user_id = int(user_id)
        user = await self.misc.find_one({"user_id": user_id})
        ist_timezone = pytz.timezone("Asia/Kolkata")
        if not user:
            res = {
                "user_id": user_id,
                "last_verified": datetime.datetime(
                    2020, 5, 17, 0, 0, 0, tzinfo=ist_timezone
                ),
                "second_time_verified": datetime.datetime(
                    2019, 5, 17, 0, 0, 0, tzinfo=ist_timezone
                ),
            }
            user = await self.misc.insert_one(res)
        return user

    async def update_notcopy_user(self, user_id, value: dict):
        user_id = int(user_id)
        myquery = {"user_id": user_id}
        newvalues = {"$set": value}
        return await self.misc.update_one(myquery, newvalues)

    async def is_user_verified(self, user_id):
        user = await self.get_notcopy_user(user_id)
        try:
            pastDate = user["last_verified"]
        except Exception:
            user = await self.get_notcopy_user(user_id)
            pastDate = user["last_verified"]
        ist_timezone = pytz.timezone("Asia/Kolkata")
        pastDate = pastDate.astimezone(ist_timezone)
        current_time = datetime.datetime.now(tz=ist_timezone)
        seconds_since_midnight = (
            current_time
            - datetime.datetime(
                current_time.year,
                current_time.month,
                current_time.day,
                0,
                0,
                0,
                tzinfo=ist_timezone,
            )
        ).total_seconds()
        time_diff = current_time - pastDate
        total_seconds = time_diff.total_seconds()
        return total_seconds <= seconds_since_midnight

    async def user_verified(self, user_id):
        user = await self.get_notcopy_user(user_id)
        try:
            pastDate = user["second_time_verified"]
        except Exception:
            user = await self.get_notcopy_user(user_id)
            pastDate = user["second_time_verified"]
        ist_timezone = pytz.timezone("Asia/Kolkata")
        pastDate = pastDate.astimezone(ist_timezone)
        current_time = datetime.datetime.now(tz=ist_timezone)
        seconds_since_midnight = (
            current_time
            - datetime.datetime(
                current_time.year,
                current_time.month,
                current_time.day,
                0,
                0,
                0,
                tzinfo=ist_timezone,
            )
        ).total_seconds()
        time_diff = current_time - pastDate
        total_seconds = time_diff.total_seconds()
        return total_seconds <= seconds_since_midnight

    async def use_second_shortener(self, user_id, time):
        user = await self.get_notcopy_user(user_id)
        if not user.get("second_time_verified"):
            ist_timezone = pytz.timezone("Asia/Kolkata")
            await self.update_notcopy_user(
                user_id,
                {
                    "second_time_verified": datetime.datetime(
                        2019, 5, 17, 0, 0, 0, tzinfo=ist_timezone
                    )
                },
            )
            user = await self.get_notcopy_user(user_id)
        if await self.is_user_verified(user_id):
            try:
                pastDate = user["last_verified"]
            except Exception:
                user = await self.get_notcopy_user(user_id)
                pastDate = user["last_verified"]
            ist_timezone = pytz.timezone("Asia/Kolkata")
            pastDate = pastDate.astimezone(ist_timezone)
            current_time = datetime.datetime.now(tz=ist_timezone)
            time_difference = current_time - pastDate
            if time_difference > datetime.timedelta(seconds=time):
                pastDate = user["last_verified"].astimezone(ist_timezone)
                second_time = user["second_time_verified"].astimezone(ist_timezone)
                return second_time < pastDate
        return False

    async def use_third_shortener(self, user_id, time):
        user = await self.get_notcopy_user(user_id)
        if not user.get("third_time_verified"):
            ist_timezone = pytz.timezone("Asia/Kolkata")
            await self.update_notcopy_user(
                user_id,
                {
                    "third_time_verified": datetime.datetime(
                        2018, 5, 17, 0, 0, 0, tzinfo=ist_timezone
                    )
                },
            )
            user = await self.get_notcopy_user(user_id)
        if await self.user_verified(user_id):
            try:
                pastDate = user["second_time_verified"]
            except Exception:
                user = await self.get_notcopy_user(user_id)
                pastDate = user["second_time_verified"]
            ist_timezone = pytz.timezone("Asia/Kolkata")
            pastDate = pastDate.astimezone(ist_timezone)
            current_time = datetime.datetime.now(tz=ist_timezone)
            time_difference = current_time - pastDate
            if time_difference > datetime.timedelta(seconds=time):
                pastDate = user["second_time_verified"].astimezone(ist_timezone)
                second_time = user["third_time_verified"].astimezone(ist_timezone)
                return second_time < pastDate
        return False

    async def create_verify_id(self, user_id: int, hash):
        res = {"user_id": user_id, "hash": hash, "verified": False}
        return await self.verify_id.insert_one(res)

    async def get_verify_id_info(self, user_id: int, hash):
        return await self.verify_id.find_one({"user_id": user_id, "hash": hash})

    async def update_verify_id_info(self, user_id, hash, value: dict):
        myquery = {"user_id": user_id, "hash": hash}
        newvalues = {"$set": value}
        return await self.verify_id.update_one(myquery, newvalues)

    async def get_user(self, user_id):
        user_data = await self.users.find_one({"id": user_id})
        return user_data

    async def remove_ban(self, id):
        ban_status = dict(is_banned=False, ban_reason="")
        await self.col.update_one({"id": id}, {"$set": {"ban_status": ban_status}})

    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(is_banned=True, ban_reason=ban_reason)
        await self.col.update_one({"id": user_id}, {"$set": {"ban_status": ban_status}})

    async def get_ban_status(self, id):
        default = dict(is_banned=False, ban_reason="")
        user = await self.col.find_one({"id": int(id)})
        if not user:
            return default
        return user.get("ban_status", default)

    async def update_user(self, user_data):
        await self.users.update_one(
            {"id": user_data["id"]}, {"$set": user_data}, upsert=True
        )

    async def get_expired(self, current_time):
        expired_users = []
        if data := self.users.find({"expiry_time": {"$lt": current_time}}):
            async for user in data:
                expired_users.append(user)
        return expired_users

    async def has_premium_access(self, user_id):
        user_data = await self.get_user(user_id)
        if user_data:
            expiry_time = user_data.get("expiry_time")
            if expiry_time is None:
                # User previously used the free trial, but it has ended.
                return False
            elif (
                isinstance(expiry_time, datetime.datetime)
                and datetime.datetime.now() <= expiry_time
            ):
                return True
            else:
                await self.users.update_one(
                    {"id": user_id}, {"$set": {"expiry_time": None}}
                )
        return False

    async def check_remaining_uasge(self, user_id):
        user_id = user_id
        user_data = await self.get_user(user_id)
        expiry_time = user_data.get("expiry_time")
        # Calculate remaining time
        remaining_time = expiry_time - datetime.datetime.now()
        return remaining_time

    async def all_premium_users(self):
        count = await self.users.count_documents(
            {"expiry_time": {"$gt": datetime.datetime.now()}}
        )
        return count

    async def update_one(self, filter_query, update_data):
        try:
            # Assuming self.client and self.users are set up properly
            result = await self.users.update_one(filter_query, update_data)
            return result.matched_count == 1
        except Exception as e:
            print(f"Error updating document: {e}")
            return False

    async def remove_premium_access(self, user_id):
        return await self.update_one({"id": user_id}, {"$set": {"expiry_time": None}})

    async def check_trial_status(self, user_id):
        user_data = await self.get_user(user_id)
        if user_data:
            return user_data.get("has_free_trial", False)
        return False

    # Free Trail Remove Logic
    async def reset_free_trial(self, user_id=None):
        if user_id is None:
            # Reset for all users
            update_data = {"$set": {"has_free_trial": False}}
            result = await self.users.update_many(
                {}, update_data
            )  # Empty query to match all users
            return result.modified_count
        else:
            # Reset for a specific user
            update_data = {"$set": {"has_free_trial": False}}
            result = await self.users.update_one({"id": user_id}, update_data)
            return (
                1 if result.modified_count > 0 else 0
            )  # Return 1 if updated, 0 if not

    async def give_free_trial(self, user_id):
        # await set_free_trial_status(user_id)
        user_id = user_id
        seconds = 5 * 60
        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        user_data = {"id": user_id, "expiry_time": expiry_time, "has_free_trial": True}
        await self.users.update_one({"id": user_id}, {"$set": user_data}, upsert=True)

    # JISSHU BOTS
    async def jisshu_set_ads_link(self, link):
        await self.jisshu_ads_link.update_one({}, {"$set": {"link": link}}, upsert=True)

    async def jisshu_get_ads_link(self):
        link = await self.jisshu_ads_link.find_one({})
        if link is not None:
            return link.get("link")
        else:
            return None

    async def jisshu_del_ads_link(self):
        try:
            isDeleted = await self.jisshu_ads_link.delete_one({})
            if isDeleted.deleted_count > 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Got err in db set : {e}")
            return False

    async def get_send_movie_update_status(self, bot_id):
        bot = await self.botcol.find_one({"id": bot_id})
        if bot and bot.get("movie_update_feature"):
            return bot["movie_update_feature"]
        else:
            return IS_SEND_MOVIE_UPDATE

    async def update_send_movie_update_status(self, bot_id, enable):
        bot = await self.botcol.find_one({"id": int(bot_id)})
        if bot:
            await self.botcol.update_one(
                {"id": int(bot_id)}, {"$set": {"movie_update_feature": enable}}
            )
        else:
            await self.botcol.insert_one(
                {"id": int(bot_id), "movie_update_feature": enable}
            )

    async def get_pm_search_status(self, bot_id):
        bot = await self.botcol.find_one({"id": bot_id})
        if bot and bot.get("bot_pm_search"):
            return bot["bot_pm_search"]
        else:
            return IS_PM_SEARCH

    async def update_pm_search_status(self, bot_id, enable):
        bot = await self.botcol.find_one({"id": int(bot_id)})
        if bot:
            await self.botcol.update_one(
                {"id": int(bot_id)}, {"$set": {"bot_pm_search": enable}}
            )
        else:
            await self.botcol.insert_one({"id": int(bot_id), "bot_pm_search": enable})

    async def movies_update_channel_id(self, id=None):
        if id is None:
            myLinks = await self.movies_update_channel.find_one({})
            if myLinks is not None:
                return myLinks.get("id")
            else:
                return None
        return await self.movies_update_channel.update_one(
            {}, {"$set": {"id": id}}, upsert=True
        )

    async def reset_group_settings(self, id):
        await self.grp.update_one({"id": int(id)}, {"$set": {"settings": self.default}})
    
    async def get_stream_mode_global(self):
        bot_config = await self.botcol.find_one({'_id': 'bot_config'})
        if bot_config and 'stream_mode_user' in bot_config:
            return bot_config['stream_mode_user']
        return STREAM_MODE_USER # Return the default from info.py

    async def update_stream_mode_global(self, is_enabled):
        await self.botcol.update_one(
            {'_id': 'bot_config'},
            {"$set": {'stream_mode_user': is_enabled}},
            upsert=True
    )
        
    async def get_new_users_today(self):
        """Gets the count of users who joined today."""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return await self.col.count_documents({"join_date": {"$gte": today}})

    async def get_new_groups_today(self):
        """Gets the count of groups added today."""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return await self.grp.count_documents({"join_date": {"$gte": today}})

db = Database()