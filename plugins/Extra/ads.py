from pyrogram import Client, filters
from datetime import datetime, timedelta
from database.config_db import mdb
from database.users_chats_db import db
from info import ADMINS
import asyncio
import re
import logging
from typing import Optional, Tuple, Union

# Configure logging
logger = logging.getLogger(__name__)

class AdsError(Exception):
    """Custom exception for advertisement-related errors"""
    pass

class AdsValidator:
    """Validator class for advertisement data"""
    
    @staticmethod
    def validate_ads_name(name: str) -> bool:
        """Validate advertisement name"""
        if not name or not name.strip():
            raise AdsError("Advertisement name cannot be empty.")
        if len(name.strip()) > 35:
            raise AdsError("Advertisement name should not exceed 35 characters.")
        return True
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        if not url or not url.strip():
            raise AdsError("URL cannot be empty.")
        
        # More comprehensive URL validation
        url_pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
        if not re.match(url_pattern, url.strip()):
            raise AdsError("Invalid URL format. Please provide a valid HTTP/HTTPS URL.")
        return True
    
    @staticmethod
    def validate_duration_or_impression(value: str) -> Tuple[Optional[datetime], Optional[int]]:
        """Validate and parse duration or impression count"""
        if not value or len(value) < 2:
            raise AdsError("Duration or impression format is invalid.")
        
        prefix = value[0].lower()
        number_part = value[1:]
        
        if not number_part.isdigit():
            raise AdsError(f"{'Duration' if prefix == 'd' else 'Impression count'} must be a number.")
        
        number = int(number_part)
        if number <= 0:
            raise AdsError(f"{'Duration' if prefix == 'd' else 'Impression count'} must be greater than 0.")
        
        if prefix == "d":
            if number > 365:  # Reasonable limit
                raise AdsError("Duration cannot exceed 365 days.")
            expiry_date = datetime.now() + timedelta(days=number)
            return expiry_date, None
        elif prefix == "i":
            if number > 1000000:  # Reasonable limit
                raise AdsError("Impression count cannot exceed 1,000,000.")
            return None, number
        else:
            raise AdsError("Invalid prefix. Use 'd' for duration (days) and 'i' for impression count.")

class AdsManager:
    """Manager class for advertisement operations"""
    
    @staticmethod
    async def set_advertisement(ads_text: str, ads_name: str, expiry_date: Optional[datetime], 
                              impression_count: Optional[int], url: str) -> bool:
        """Set advertisement with proper error handling"""
        try:
            await mdb.update_advirtisment(ads_text, ads_name.strip(), expiry_date, impression_count)
            await db.jisshu_set_ads_link(url.strip())
            return True
        except Exception as e:
            logger.error(f"Failed to set advertisement: {str(e)}")
            raise AdsError(f"Failed to save advertisement: {str(e)}")
    
    @staticmethod
    async def get_advertisement_info() -> Tuple[Optional[str], Optional[str], Optional[int]]:
        """Get advertisement information with error handling"""
        try:
            return await mdb.get_advirtisment()
        except Exception as e:
            logger.error(f"Failed to get advertisement info: {str(e)}")
            raise AdsError(f"Failed to retrieve advertisement information: {str(e)}")
    
    @staticmethod
    async def delete_advertisement() -> Tuple[bool, Optional[str]]:
        """Delete advertisement and return success status and old link"""
        try:
            # Get current link before deletion
            current_link = await db.jisshu_get_ads_link()
            
            # Reset advertisement
            await mdb.update_advirtisment()
            
            # Delete ads link if exists
            link_deleted = False
            if current_link:
                link_deleted = await db.jisshu_del_ads_link()
            
            return link_deleted, current_link
        except Exception as e:
            logger.error(f"Failed to delete advertisement: {str(e)}")
            raise AdsError(f"Failed to delete advertisement: {str(e)}")

@Client.on_message(filters.private & filters.command("set_ads") & filters.user(ADMINS))
async def set_ads(client, message):
    """Set advertisement command handler with improved error handling"""
    try:
        # Check if command has arguments
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            await message.reply_text(
                "❌ **Usage:** `/set_ads {ads name}#{time}#{photo URL}`\n\n"
                "**Examples:**\n"
                "• `/set_ads My Ad#d7#https://example.com/image.jpg` (7 days)\n"
                "• `/set_ads My Ad#i1000#https://example.com/image.jpg` (1000 impressions)\n\n"
                "<a href='https://t.me/c/1867416281/2009'>📖 Detailed Explanation</a>"
            )
            return
        
        command_args = command_parts[1]
        
        # Validate command format
        if command_args.count("#") != 2:
            await message.reply_text(
                "❌ **Invalid format!** Please use: `{ads name}#{time}#{photo URL}`\n\n"
                "The command must contain exactly 2 '#' separators."
            )
            return
        
        # Parse command arguments
        ads_name, duration_or_impression, url = command_args.split("#", 2)
        
        # Validate inputs using validator
        AdsValidator.validate_ads_name(ads_name)
        AdsValidator.validate_url(url)
        expiry_date, impression_count = AdsValidator.validate_duration_or_impression(duration_or_impression)
        
        # Check if replying to a message
        reply = message.reply_to_message
        if not reply:
            await message.reply_text(
                "❌ **No message selected!**\n\n"
                "Please reply to a text message that you want to set as your advertisement."
            )
            return
        
        if not reply.text:
            await message.reply_text(
                "❌ **Invalid message type!**\n\n"
                "Only text messages are supported for advertisements."
            )
            return
        
        if len(reply.text) > 4000:  # Telegram message limit consideration
            await message.reply_text(
                "❌ **Message too long!**\n\n"
                "Advertisement text should not exceed 4000 characters."
            )
            return
        
        # Show processing message
        processing_msg = await message.reply_text("⏳ **Setting up advertisement...**")
        
        # Set advertisement
        success = await AdsManager.set_advertisement(
            reply.text, ads_name.strip(), expiry_date, impression_count, url.strip()
        )
        
        if success:
            # Small delay for database consistency
            await asyncio.sleep(1)
            
            # Verify the advertisement was set
            try:
                _, name, remaining = await AdsManager.get_advertisement_info()
                
                duration_text = ""
                if expiry_date:
                    duration_text = f"📅 **Expires:** {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}"
                elif impression_count:
                    duration_text = f"👁️ **Impressions:** {remaining} remaining"
                
                await processing_msg.edit_text(
                    f"✅ **Advertisement Set Successfully!**\n\n"
                    f"📝 **Name:** `{name}`\n"
                    f"🔗 **Stream Link:** `{url.strip()}`\n"
                    f"{duration_text}\n\n"
                    f"Your advertisement is now active! 🎉"
                )
            except Exception as e:
                await processing_msg.edit_text(
                    f"⚠️ **Advertisement set but verification failed**\n\n"
                    f"The advertisement might have been set successfully, but we couldn't verify it.\n"
                    f"Use `/ads` to check the current status."
                )
        
    except AdsError as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in set_ads: {str(e)}")
        await message.reply_text(
            f"❌ **Unexpected error occurred**\n\n"
            f"Please try again later or contact support if the issue persists.\n"
            f"Error: `{str(e)[:100]}...`"
        )

@Client.on_message(filters.private & filters.command("ads"))
async def ads(_, message):
    """Get current advertisement information"""
    try:
        _, name, impression = await AdsManager.get_advertisement_info()
        
        if not name:
            await message.reply_text(
                "📭 **No Active Advertisement**\n\n"
                "There are currently no advertisements set.\n"
                "Use `/set_ads` to create one!"
            )
            return
        
        if impression is not None and impression <= 0:
            await message.reply_text(
                f"⏰ **Advertisement Expired**\n\n"
                f"📝 **Name:** `{name}`\n"
                f"👁️ **Status:** Expired (0 impressions remaining)\n\n"
                f"Use `/set_ads` to create a new advertisement."
            )
            return
        
        # Determine status message
        status_text = ""
        if impression is not None:
            status_text = f"👁️ **Impressions Remaining:** {impression:,}"
        else:
            status_text = "📅 **Duration-based advertisement**"
        
        await message.reply_text(
            f"📢 **Current Advertisement**\n\n"
            f"📝 **Name:** `{name}`\n"
            f"{status_text}\n\n"
            f"✅ **Status:** Active"
        )
        
    except AdsError as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in ads: {str(e)}")
        await message.reply_text(
            "❌ **Failed to retrieve advertisement information**\n\n"
            "Please try again later."
        )

@Client.on_message(filters.private & filters.command("del_ads") & filters.user(ADMINS))
async def del_ads(client, message):
    """Delete advertisement command handler"""
    try:
        # Show processing message
        processing_msg = await message.reply_text("⏳ **Deleting advertisement...**")
        
        # Delete advertisement
        link_deleted, current_link = await AdsManager.delete_advertisement()
        
        # Prepare response message
        if current_link:
            if link_deleted:
                response = (
                    f"✅ **Advertisement Deleted Successfully!**\n\n"
                    f"📝 **Action:** Advertisement and stream link removed\n"
                    f"🔗 **Deleted Link:** `{current_link}`\n\n"
                    f"All advertisement data has been cleared! 🎉"
                )
            else:
                response = (
                    f"⚠️ **Partial Success**\n\n"
                    f"📝 **Advertisement:** ✅ Deleted successfully\n"
                    f"🔗 **Stream Link:** ❌ Deletion failed\n"
                    f"**Link:** `{current_link}`\n\n"
                    f"Please check logs for details or try again."
                )
        else:
            response = (
                f"✅ **Advertisement Reset**\n\n"
                f"📝 **Status:** Advertisement data cleared\n"
                f"🔗 **Note:** No stream link was found to delete\n\n"
                f"Ready for new advertisements! 🚀"
            )
        
        await processing_msg.edit_text(response)
        
    except AdsError as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in del_ads: {str(e)}")
        await message.reply_text(
            "❌ **Failed to delete advertisement**\n\n"
            "An unexpected error occurred. Please check logs and try again."
        )

def is_valid_url(url: str) -> bool:
    """
    Enhanced URL validation function
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    url = url.strip()
    if not url:
        return False
    
    # Comprehensive URL pattern
    url_pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
    return bool(re.match(url_pattern, url))

# Additional utility functions for future enhancements
async def get_ads_statistics():
    """Get advertisement statistics (for future implementation)"""
    try:
        # This could be implemented to show stats like:
        # - Total impressions served
        # - Click-through rates
        # - Active/expired ads count
        pass
    except Exception as e:
        logger.error(f"Error getting ads statistics: {str(e)}")
        return None

async def schedule_ads_cleanup():
    """Schedule cleanup of expired advertisements (for future implementation)"""
    try:
        # This could be implemented as a background task to:
        # - Remove expired ads automatically
        # - Clean up unused media files
        # - Generate usage reports
        pass
    except Exception as e:
        logger.error(f"Error in ads cleanup: {str(e)}")